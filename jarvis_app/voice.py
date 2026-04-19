from __future__ import annotations

from dataclasses import dataclass
import json
import os
import queue
import re
import threading
import time
from pathlib import Path
from typing import Callable

from .settings_manager import VoiceSettings


LogCallback = Callable[[str], None]
CommandCallback = Callable[[str], None]


@dataclass(slots=True)
class VoiceEventHandlers:
    on_log: LogCallback
    on_command: CommandCallback


class LocalSpeaker:
    def __init__(self, settings: VoiceSettings) -> None:
        self._settings = settings
        self._lock = threading.Lock()
        self._engine = None

    def _ensure_engine(self):
        if self._engine is not None:
            return self._engine

        import pyttsx3

        engine = pyttsx3.init()
        preferred_name = self._settings.tts_voice_name.strip().lower()
        if preferred_name:
            for voice in engine.getProperty("voices"):
                voice_name = getattr(voice, "name", "").lower()
                if preferred_name in voice_name:
                    engine.setProperty("voice", voice.id)
                    break
        self._engine = engine
        return engine

    def speak(self, text: str) -> None:
        if not self._settings.tts_enabled or not text.strip():
            return
        with self._lock:
            engine = self._ensure_engine()
            engine.say(text)
            engine.runAndWait()


class VoiceLoop:
    def __init__(self, settings: VoiceSettings, handlers: VoiceEventHandlers) -> None:
        self._settings = settings
        self._handlers = handlers
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    @property
    def running(self) -> bool:
        return bool(self._thread and self._thread.is_alive())

    def start(self) -> None:
        if self.running or not self._settings.enabled:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def _run(self) -> None:
        try:
            self._listen()
        except Exception as exc:
            self._handlers.on_log(f"Voice loop stopped: {exc}")

    def _listen(self) -> None:
        import sounddevice as sd
        from vosk import KaldiRecognizer, Model

        model_path = self._resolve_model_path()
        if not model_path.exists():
            self._handlers.on_log(
                f"Voice model missing. Put a Vosk model in {model_path}."
            )
            return

        model = Model(str(model_path))
        recognizer = KaldiRecognizer(model, self._settings.sample_rate)
        transcripts: queue.Queue[str] = queue.Queue()
        wake_pattern = re.compile(rf"\b{re.escape(self._settings.wake_word)}\b", re.IGNORECASE)
        waiting_until = 0.0

        def callback(indata, frames, time_info, status) -> None:
            del frames, time_info
            if status:
                self._handlers.on_log(f"Microphone status: {status}")
            if recognizer.AcceptWaveform(bytes(indata)):
                payload = json.loads(recognizer.Result())
                text = str(payload.get("text", "")).strip()
                if text:
                    transcripts.put(text)

        with sd.RawInputStream(
            samplerate=self._settings.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback,
        ):
            self._handlers.on_log(f"Listening for wake word '{self._settings.wake_word}'.")
            while not self._stop_event.is_set():
                try:
                    transcript = transcripts.get(timeout=0.25)
                except queue.Empty:
                    continue

                normalized = transcript.strip()
                now = time.time()

                if waiting_until and now <= waiting_until:
                    waiting_until = 0.0
                    self._handlers.on_log(f"Voice command: {normalized}")
                    self._handlers.on_command(normalized)
                    continue

                match = wake_pattern.search(normalized)
                if not match:
                    continue

                remainder = normalized[match.end() :].strip(" ,.!?")
                if remainder:
                    self._handlers.on_log(f"Wake word matched with inline command: {remainder}")
                    self._handlers.on_command(remainder)
                    continue

                waiting_until = now + self._settings.command_timeout_seconds
                self._handlers.on_log("Wake word heard. Listening for a command.")

    def _resolve_model_path(self) -> Path:
        path = Path(os.path.expandvars(os.path.expanduser(self._settings.vosk_model_path)))
        if not path.is_absolute():
            path = Path(__file__).resolve().parent.parent / path
        return path.resolve()
