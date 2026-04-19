from __future__ import annotations

from dataclasses import dataclass
import threading
from typing import Callable

from .settings_manager import get_settings, JarvisSettings
from .interpreter_bridge import AssistantResult, OpenInterpreterBridge
from .profile import build_profile_summary
from .runtime import jarvis
from .safety import SafetyController
from .voice import LocalSpeaker, VoiceEventHandlers, VoiceLoop


LogCallback = Callable[[str], None]


@dataclass(slots=True)
class CommandOutcome:
    reply: str
    raw_events: list[str]
    blocked: bool = False


class JarvisAssistant:
    def __init__(self, on_log: LogCallback) -> None:
        self._on_log = on_log
        self._lock = threading.Lock()
        self.settings: JarvisSettings = get_settings()
        self.safety = SafetyController(default_pc_control=self.settings.pc_access.enabled_on_startup)
        self.profile_summary = build_profile_summary(self.settings)
        self.bridge = OpenInterpreterBridge(self.settings, self.profile_summary)
        self.speaker = LocalSpeaker(self.settings.voice)
        self.voice_loop = VoiceLoop(
            self.settings.voice,
            VoiceEventHandlers(on_log=self._on_log, on_command=self._handle_voice_command),
        )

    def refresh_profile(self) -> str:
        """Reload settings and rebuild profile summary."""
        self.voice_loop.stop()
        self.settings = get_settings()
        self.profile_summary = build_profile_summary(self.settings)
        self.bridge.update_profile_summary(self.profile_summary)
        self.speaker = LocalSpeaker(self.settings.voice)
        self.voice_loop = VoiceLoop(
            self.settings.voice,
            VoiceEventHandlers(on_log=self._on_log, on_command=self._handle_voice_command),
        )
        self._on_log("Refreshed user profile and settings.")
        return self.profile_summary

    def start_listening(self) -> None:
        """Start voice recognition loop."""
        if not self.settings.voice.enabled:
            self._on_log("Voice recognition disabled in settings")
            return
        self.voice_loop.start()
        self.safety.set_listening(True)
        self._on_log(f"Voice listening started (wake word: '{self.settings.voice.wake_word}')")

    def stop_listening(self) -> None:
        """Stop voice recognition loop."""
        self.voice_loop.stop()
        self.safety.set_listening(False)
        self._on_log("Voice listening stopped")

    def enable_pc_access(self) -> None:
        """Enable PC system access."""
        self.safety.enable_pc_control()
        self._on_log("PC access enabled.")

    def disable_pc_access(self) -> None:
        """Disable PC system access."""
        self.safety.disable_pc_control()
        self._on_log("PC access disabled.")

    def emergency_stop(self) -> None:
        """Trigger emergency stop (disable all PC access immediately)."""
        self.safety.trigger_emergency_stop()
        self._on_log("Emergency stop activated. PC access disabled.")

    def clear_emergency_stop(self) -> None:
        """Clear emergency stop state."""
        self.safety.clear_emergency_stop()
        self._on_log("Emergency stop cleared.")

    def shutdown(self) -> None:
        """Gracefully shutdown the assistant."""
        self.stop_listening()
        self._on_log("Jarvis assistant shutdown")

    def _handle_voice_command(self, command: str) -> None:
        """Handle voice command in background thread."""
        # Check blocklist before processing
        if self.settings.is_blocked_command(command):
            self._on_log(f"Command blocked by security policy: {command}")
            return

        worker = threading.Thread(
            target=self.run_command,
            args=(command, "voice"),
            daemon=True,
        )
        worker.start()

    def run_command(self, command: str, source: str = "text") -> CommandOutcome:
        """Execute a command with safety checks."""
        # Check blocklist
        if self.settings.is_blocked_command(command):
            self._on_log(f"BLOCKED: Command matches security blocklist: {command}")
            return CommandOutcome(
                reply="I cannot execute that command due to security settings.",
                raw_events=[],
                blocked=True
            )

        with self._lock:
            self.safety.set_busy(True, last_command=command)
            try:
                state = self.safety.get_state()
                screen_context = ""

                # Capture screen context if PC control is enabled
                if (
                    state.pc_control_enabled
                    and not state.emergency_stop
                    and self.settings.screen.auto_capture_context
                ):
                    try:
                        capture = jarvis.capture_screen()
                        screen_context = capture.ocr_text[: self.settings.screen.include_ocr_text_chars]
                        if screen_context:
                            self._on_log("Captured current screen context.")
                    except Exception as e:
                        self._on_log(f"Note: Could not capture screen: {e}")

                self._on_log(f"{source.title()} command: {command}")

                # Run the command through the bridge
                result: AssistantResult = self.bridge.run(command, screen_context=screen_context, log=self._on_log)

                if result.text:
                    self._on_log(f"Jarvis: {result.text}")
                    # Speak response if voice is enabled
                    if source == "voice" and self.settings.voice.tts_enabled:
                        self.speaker.speak(result.text)

                return CommandOutcome(reply=result.text, raw_events=result.raw_events, blocked=False)

            except Exception as e:
                self._on_log(f"Error executing command: {e}")
                return CommandOutcome(reply=f"Error: {e}", raw_events=[], blocked=False)
            finally:
                self.safety.set_busy(False)
