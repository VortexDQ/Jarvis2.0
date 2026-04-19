from __future__ import annotations

import queue
import sys
import threading
from pathlib import Path

from .assistant import JarvisAssistant
from .error_handler import BackupManager, ErrorHandler
from .settings_manager import JarvisSettings, get_settings


class JarvisSlintWindow:
    """Modern Slint-based UI for Jarvis with speaker animation and settings integration."""

    def __init__(self, settings: JarvisSettings | None = None) -> None:
        self._events: queue.Queue[tuple[str, str | bool]] = queue.Queue()
        self.settings = settings or get_settings()
        self._on_log = print
        self.assistant = JarvisAssistant(self._log_from_worker)
        self._ui = None
        self._is_speaking = False
        self._error_handler = ErrorHandler(self._on_log)
        self._backup_manager = BackupManager()
        self._speaking_lock = threading.Lock()

    def _load_slint_ui(self):
        """Load and compile the Slint UI from jarvis.slint."""
        try:
            import slint

            ui_path = Path(__file__).parent / "UI" / "ui" / "jarvis.slint"
            if not ui_path.exists():
                raise FileNotFoundError(f"Slint file not found at {ui_path}")

            slint_source = ui_path.read_text(encoding="utf-8")
            jarvis_ui = slint.compile_from_text(
                slint_source,
                component_name="JarvisUI",
                include_paths=[str(ui_path.parent)],
            )

            self._on_log("Slint UI compiled successfully")
            return jarvis_ui
        except Exception as exc:
            self._error_handler.log_error("SLINT_COMPILE_ERROR", str(exc), exc)
            self._on_log(f"ERROR: Failed to load Slint UI: {exc}")
            return None

    def _log_from_worker(self, message: str) -> None:
        self._events.put(("log", message))

    def _pump_events(self) -> None:
        while True:
            try:
                event_type, value = self._events.get_nowait()
            except queue.Empty:
                break

            if event_type == "log":
                self._on_log(f"[Assistant] {value}")
            elif event_type == "speaking" and self._ui:
                try:
                    self._ui.is_speaking = bool(value)
                except Exception as exc:
                    self._on_log(f"Warning: Could not update UI speaking state: {exc}")

    def run(self) -> None:
        try:
            deps = self._error_handler.check_dependencies()
            if not deps.get("slint"):
                raise ImportError("Slint Python package not installed")

            jarvis_ui = self._load_slint_ui()
            if not jarvis_ui:
                raise RuntimeError("Failed to compile Slint UI")

            self._ui = jarvis_ui()
            self._on_log(f"Jarvis Slint UI initialized (v{self.settings.version})")

            if self.settings.ui.always_on_top and hasattr(self._ui, "always_on_top"):
                self._ui.always_on_top = True
            if self.settings.ui.window_opacity < 1.0 and hasattr(self._ui, "opacity"):
                self._ui.opacity = self.settings.ui.window_opacity

            self._setup_callbacks()

            if self.settings.voice.auto_start_on_launch and self.settings.voice.enabled:
                self.assistant.start_listening()
                self._on_log(f"Voice listening enabled on launch (wake word: '{self.settings.voice.wake_word}')")

            def event_pump() -> None:
                import time

                while True:
                    self._pump_events()
                    time.sleep(0.1)

            event_thread = threading.Thread(target=event_pump, daemon=True)
            event_thread.start()

            self._ui.run()
        except Exception as exc:
            self._error_handler.log_error("SLINT_RUNTIME_ERROR", str(exc), exc)
            self._on_log(f"ERROR: Failed to run Slint UI: {exc}")
            self._on_log("Attempting fallback to classic UI...")
            self._fallback_to_tkinter()

    def _setup_callbacks(self) -> None:
        if not self._ui:
            return

        def on_mute_pressed():
            self.toggle_mute()

        def on_access_pc_pressed():
            self.toggle_pc_access()

        try:
            self._ui.on_mute_pressed(on_mute_pressed)
            self._ui.on_access_pc_pressed(on_access_pc_pressed)
            self._on_log("UI callbacks registered successfully")
        except Exception as exc:
            self._error_handler.log_error("CALLBACK_ERROR", str(exc), exc)
            self._on_log(f"Warning: Could not set up all callbacks: {exc}")

    def toggle_mute(self) -> None:
        if self._ui:
            try:
                self._ui.system_muted = not self._ui.system_muted
                state = "muted" if self._ui.system_muted else "unmuted"
                self._on_log(f"System audio {state}")
            except Exception as exc:
                self._on_log(f"Error toggling mute: {exc}")

    def toggle_pc_access(self) -> None:
        try:
            state = self.assistant.safety.get_state()
            if state.pc_control_enabled:
                self.assistant.disable_pc_access()
            else:
                self.assistant.enable_pc_access()

            if self._ui:
                self._ui.pc_access_enabled = self.assistant.safety.get_state().pc_control_enabled
        except Exception as exc:
            self._on_log(f"Error toggling PC access: {exc}")

    def _fallback_to_tkinter(self) -> None:
        try:
            from .ui import JarvisWindow

            self._on_log("Launching fallback Tkinter UI...")
            app = JarvisWindow()
            app.run()
        except Exception as exc:
            self._on_log(f"FATAL: Both UIs failed: {exc}")
            sys.exit(1)

    def shutdown(self) -> None:
        self._on_log("Shutting down Jarvis...")
        self.assistant.shutdown()
