from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import scrolledtext

from .assistant import JarvisAssistant


class JarvisWindow:
    def __init__(self) -> None:
        self._events: queue.Queue[tuple[str, str]] = queue.Queue()
        self.assistant = JarvisAssistant(self._log_from_worker)

        self.root = tk.Tk()
        self.root.title(self.assistant.settings.ui.window_title)
        self.root.geometry("980x700")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.status_var = tk.StringVar(value="Starting...")
        self.command_var = tk.StringVar()

        self._build_layout()
        self._refresh_status()
        self.root.after(200, self._pump_events)

        if self.assistant.settings.voice.auto_start_on_launch:
            self.root.after(300, self.start_listening)

    def _build_layout(self) -> None:
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=12, pady=12)

        tk.Button(button_frame, text="Start Listening", command=self.start_listening).pack(side="left", padx=4)
        tk.Button(button_frame, text="Stop Listening", command=self.stop_listening).pack(side="left", padx=4)
        tk.Button(button_frame, text="Enable PC Access", command=self.enable_pc_access).pack(side="left", padx=4)
        tk.Button(button_frame, text="Disable PC Access", command=self.disable_pc_access).pack(side="left", padx=4)
        tk.Button(button_frame, text="Emergency Stop", command=self.emergency_stop).pack(side="left", padx=4)
        tk.Button(button_frame, text="Clear Stop", command=self.clear_stop).pack(side="left", padx=4)
        tk.Button(button_frame, text="Refresh Profile", command=self.refresh_profile).pack(side="left", padx=4)

        status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w", justify="left")
        status_label.pack(fill="x", padx=12)

        self.log_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=28)
        self.log_text.pack(fill="both", expand=True, padx=12, pady=12)
        self.log_text.configure(state="disabled")

        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="x", padx=12, pady=(0, 12))

        entry = tk.Entry(input_frame, textvariable=self.command_var)
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", lambda _event: self.send_command())

        tk.Button(input_frame, text="Send", command=self.send_command).pack(side="left", padx=(8, 0))

    def _on_close(self) -> None:
        self.assistant.shutdown()
        self.root.destroy()

    def _log_from_worker(self, message: str) -> None:
        self._events.put(("log", message))

    def _pump_events(self) -> None:
        while True:
            try:
                event_type, value = self._events.get_nowait()
            except queue.Empty:
                break

            if event_type == "log":
                self._append_log(value)

        self._refresh_status()
        self.root.after(200, self._pump_events)

    def _append_log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def _refresh_status(self) -> None:
        state = self.assistant.safety.get_state()
        parts = [
            f"Listening: {'on' if state.listening_enabled else 'off'}",
            f"PC access: {'on' if state.pc_control_enabled else 'off'}",
            f"Emergency stop: {'active' if state.emergency_stop else 'clear'}",
            f"Busy: {'yes' if state.busy else 'no'}",
        ]
        if state.last_command:
            parts.append(f"Last command: {state.last_command}")
        self.status_var.set(" | ".join(parts))

    def start_listening(self) -> None:
        self.assistant.start_listening()
        self._append_log("Voice listening enabled.")

    def stop_listening(self) -> None:
        self.assistant.stop_listening()
        self._append_log("Voice listening disabled.")

    def enable_pc_access(self) -> None:
        self.assistant.enable_pc_access()

    def disable_pc_access(self) -> None:
        self.assistant.disable_pc_access()

    def emergency_stop(self) -> None:
        self.assistant.emergency_stop()

    def clear_stop(self) -> None:
        self.assistant.clear_emergency_stop()

    def refresh_profile(self) -> None:
        self.assistant.refresh_profile()

    def send_command(self) -> None:
        command = self.command_var.get().strip()
        if not command:
            return
        self.command_var.set("")
        worker = threading.Thread(target=self.assistant.run_command, args=(command, "text"), daemon=True)
        worker.start()

    def run(self) -> None:
        self.root.mainloop()
