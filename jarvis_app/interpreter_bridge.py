from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import textwrap
from typing import Callable
from urllib.request import Request, urlopen

from .settings_manager import JarvisSettings
from .paths import CONVERSATIONS_DIR, ROOT_DIR, ensure_directories
from .safety import SafetyController


LogCallback = Callable[[str], None]


@dataclass(slots=True)
class AssistantResult:
    text: str
    raw_events: list[str]


class OpenInterpreterBridge:
    def __init__(self, settings: JarvisSettings, profile_summary: str) -> None:
        self._settings = settings
        self._profile_summary = profile_summary
        self._safety = SafetyController(default_pc_control=settings.pc_access.enabled_on_startup)
        self._interpreter = None

    def update_profile_summary(self, profile_summary: str) -> None:
        self._profile_summary = profile_summary

    def _load_interpreter(self):
        if self._interpreter is None:
            from interpreter import interpreter

            self._interpreter = interpreter
        return self._interpreter

    def _build_system_message(self) -> str:
        state = self._safety.get_state()
        pc_access = "enabled" if state.pc_control_enabled and not state.emergency_stop else "disabled"
        allowed_roots = "\n".join(f"- {path}" for path in self._settings.access.allowed_roots)
        helper_import = "from jarvis_app.runtime import jarvis"

        return textwrap.dedent(
            f"""
            You are {self._settings.assistant_name}, a local desktop assistant for {self._settings.user.preferred_name or 'the user'}.
            Think locally and privately. Never ask for cloud API keys. Prefer local Python and shell solutions.

            Strict operating rules:
            - Only act on explicit user instructions.
            - Do not take autonomous initiative beyond the exact request.
            - PC control is currently {pc_access}.
            - If PC control is disabled, do not execute code. Reply conversationally and explain what would be needed.
            - Prefer the helper module below over raw OS automation:
              {helper_import}
            - Use `jarvis.search_files`, `jarvis.search_text`, `jarvis.read_text_file`, `jarvis.write_text_file`,
              `jarvis.capture_screen`, `jarvis.move_mouse`, `jarvis.click`, `jarvis.type_text`, `jarvis.press`,
              `jarvis.hotkey`, and `jarvis.scroll` for computer actions.
            - Respect these allowed roots for file work:
              {allowed_roots}
            - Keep confirmations brief and describe what you actually changed.

            User profile context:
            {self._profile_summary}
            """
        ).strip()

    def _configure(self) -> None:
        ensure_directories()
        interpreter = self._load_interpreter()
        state = self._safety.get_state()

        interpreter.offline = True
        interpreter.auto_run = bool(state.pc_control_enabled and not state.emergency_stop)
        interpreter.verbose = False
        interpreter.disable_telemetry = True
        interpreter.conversation_history = True
        interpreter.conversation_filename = "jarvis_history.json"
        interpreter.conversation_history_path = str(CONVERSATIONS_DIR)
        interpreter.llm.model = f"ollama/{self._settings.ai.model}"
        interpreter.llm.api_base = self._settings.ai.api_base
        interpreter.llm.api_key = "local-only"
        interpreter.llm.supports_functions = False
        interpreter.llm.supports_vision = False
        interpreter.system_message = self._build_system_message()

        if hasattr(interpreter, "safe_mode"):
            interpreter.safe_mode = "auto"

        if hasattr(interpreter, "computer"):
            interpreter.computer.offline = True
            interpreter.computer.verbose = False
            if hasattr(interpreter.computer, "import_computer_api"):
                interpreter.computer.import_computer_api = False

        if state.pc_control_enabled and not state.emergency_stop:
            bootstrap = textwrap.dedent(
                f"""
                import sys
                from pathlib import Path
                project_root = Path(r"{ROOT_DIR}")
                if str(project_root) not in sys.path:
                    sys.path.insert(0, str(project_root))
                from jarvis_app.runtime import jarvis
                """
            ).strip()
            interpreter.computer.run("python", bootstrap)

    def run(self, command: str, screen_context: str = "", log: LogCallback | None = None) -> AssistantResult:
        prompt = command.strip()
        if screen_context:
            prompt = f"{prompt}\n\nCurrent screen OCR context:\n{screen_context}"

        state = self._safety.get_state()
        if not state.pc_control_enabled or state.emergency_stop:
            text = self._run_plain_ollama(prompt)
            if log:
                log(f"[ollama] {text}")
            return AssistantResult(text=text, raw_events=[])

        self._configure()
        interpreter = self._load_interpreter()

        raw_events: list[str] = []
        assistant_chunks: list[str] = []

        for chunk in interpreter.chat(prompt, stream=True, display=False):
            rendered = self._render_chunk(chunk)
            if rendered:
                raw_events.append(rendered)
                if log:
                    log(rendered)
            if chunk.get("role") == "assistant" and chunk.get("type") == "message" and chunk.get("content"):
                assistant_chunks.append(str(chunk["content"]))

        response_text = "".join(assistant_chunks).strip()
        if not response_text:
            response_text = self._extract_last_message()
        return AssistantResult(text=response_text, raw_events=raw_events)

    def _run_plain_ollama(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self._settings.ai.model,
                "system": self._build_system_message(),
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8")
        request = Request(
            url=f"{self._settings.ai.api_base}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
        return str(body.get("response", "")).strip()

    def _extract_last_message(self) -> str:
        interpreter = self._load_interpreter()
        messages = getattr(interpreter, "messages", [])
        for message in reversed(messages):
            if message.get("role") == "assistant" and message.get("message"):
                return str(message["message"]).strip()
        return "I finished, but no assistant text was returned."

    @staticmethod
    def _render_chunk(chunk: dict[str, object]) -> str:
        role = str(chunk.get("role", ""))
        chunk_type = str(chunk.get("type", ""))
        content = chunk.get("content")

        if role == "assistant" and chunk_type == "message" and content:
            return ""
        if role == "assistant" and chunk_type == "code" and content:
            return f"[code:{chunk.get('format', '')}] {content}"
        if role == "computer" and chunk_type == "console" and content:
            return f"[console] {content}"
        if role == "computer" and chunk_type == "confirmation" and content:
            return f"[confirmation] {content}"
        return ""
