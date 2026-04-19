from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import time
from typing import Iterable

from .settings_manager import get_settings
from .paths import LAST_SCREENSHOT_PATH, LAST_SCREEN_OCR_PATH, SCREEN_DIR, ensure_directories
from .safety import PCAccessError, SafetyController, is_path_within


SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".cache",
}


@dataclass(slots=True)
class ScreenCaptureResult:
    image_path: Path
    ocr_text: str


class JarvisRuntime:
    def __init__(self) -> None:
        self._safety = SafetyController()

    def _settings(self):
        ensure_directories()
        return get_settings()

    def _state_check(self, action: str) -> None:
        self._safety.require_pc_control(action)

    def _allowed_roots(self) -> list[Path]:
        return [self._resolve_config_path(path) for path in self._settings().access.allowed_roots]

    def _resolve_user_path(self, raw_path: str | Path) -> Path:
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
        return path.resolve()

    def _resolve_config_path(self, raw_path: str | Path) -> Path:
        expanded = os.path.expandvars(os.path.expanduser(str(raw_path)))
        path = Path(expanded)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent.parent / path
        return path.resolve()

    def _assert_allowed_path(self, path: Path, action: str) -> None:
        for root in self._allowed_roots():
            if is_path_within(path, root):
                return
        raise PCAccessError(f"{action} blocked because {path} is outside allowed roots.")

    def list_allowed_roots(self) -> list[str]:
        return [str(path) for path in self._allowed_roots()]

    def search_files(self, query: str, limit: int | None = None, roots: Iterable[str] | None = None) -> list[str]:
        self._state_check("search files")
        settings = self._settings()
        max_results = limit or settings.access.max_search_results
        normalized_query = query.casefold()
        results: list[str] = []

        search_roots = [self._resolve_user_path(item) for item in roots] if roots else self._allowed_roots()
        for root in search_roots:
            self._assert_allowed_path(root, "search")
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if len(results) >= max_results:
                    return results
                if any(part in SKIP_DIRS for part in path.parts):
                    continue
                if normalized_query in path.name.casefold():
                    results.append(str(path))
        return results

    def search_text(self, query: str, limit: int | None = None) -> list[dict[str, str]]:
        self._state_check("search file contents")
        settings = self._settings()
        max_results = limit or settings.access.max_search_results
        normalized_query = query.casefold()
        results: list[dict[str, str]] = []

        for root in self._allowed_roots():
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if len(results) >= max_results:
                    return results
                if not path.is_file():
                    continue
                if any(part in SKIP_DIRS for part in path.parts):
                    continue
                if path.suffix.lower() not in settings.access.text_extensions:
                    continue
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                if normalized_query in content.casefold():
                    excerpt = content[: settings.access.max_file_read_chars]
                    results.append({"path": str(path), "excerpt": excerpt})
        return results

    def read_text_file(self, raw_path: str | Path) -> str:
        self._state_check("read files")
        settings = self._settings()
        path = self._resolve_user_path(raw_path)
        self._assert_allowed_path(path, "read")
        content = path.read_text(encoding="utf-8", errors="ignore")
        return content[: settings.access.max_file_read_chars]

    def write_text_file(self, raw_path: str | Path, content: str, append: bool = False) -> str:
        self._state_check("write files")
        settings = self._settings()
        path = self._resolve_user_path(raw_path)
        self._assert_allowed_path(path, "write")
        if len(content) > settings.access.max_file_write_chars:
            raise PCAccessError("Write blocked because content exceeded the configured safety limit.")
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        with path.open(mode, encoding="utf-8") as handle:
            handle.write(content)
        return str(path)

    def capture_screen(self) -> ScreenCaptureResult:
        self._state_check("capture the screen")
        ensure_directories()

        import mss
        import mss.tools

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            capture = sct.grab(monitor)
            mss.tools.to_png(capture.rgb, capture.size, output=str(LAST_SCREENSHOT_PATH))

        ocr_text = ""
        try:
            from rapidocr_onnxruntime import RapidOCR

            engine = RapidOCR()
            result, _ = engine(str(LAST_SCREENSHOT_PATH))
            if result:
                ocr_text = "\n".join(item[1] for item in result if len(item) > 1)
        except Exception:
            ocr_text = ""

        LAST_SCREEN_OCR_PATH.write_text(ocr_text, encoding="utf-8")
        return ScreenCaptureResult(image_path=LAST_SCREENSHOT_PATH, ocr_text=ocr_text)

    def move_mouse(self, x: int, y: int, duration: float = 0.2) -> str:
        self._state_check("move the mouse")
        import pyautogui

        pyautogui.FAILSAFE = True
        pyautogui.moveTo(x, y, duration=duration)
        return f"Moved mouse to ({x}, {y})."

    def click(self, x: int | None = None, y: int | None = None, button: str = "left", clicks: int = 1) -> str:
        self._state_check("click the mouse")
        import pyautogui

        pyautogui.FAILSAFE = True
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
        else:
            pyautogui.click(button=button, clicks=clicks)
        return f"Clicked the {button} mouse button."

    def type_text(self, text: str, interval: float = 0.01) -> str:
        self._state_check("type on the keyboard")
        import pyautogui

        pyautogui.FAILSAFE = True
        pyautogui.write(text, interval=interval)
        return "Typed text into the active window."

    def press(self, key: str) -> str:
        self._state_check("press keys")
        import pyautogui

        pyautogui.FAILSAFE = True
        pyautogui.press(key)
        return f"Pressed {key}."

    def hotkey(self, *keys: str) -> str:
        self._state_check("press hotkeys")
        import pyautogui

        pyautogui.FAILSAFE = True
        pyautogui.hotkey(*keys)
        return f"Pressed hotkey: {' + '.join(keys)}."

    def scroll(self, amount: int) -> str:
        self._state_check("scroll")
        import pyautogui

        pyautogui.FAILSAFE = True
        pyautogui.scroll(amount)
        return f"Scrolled by {amount}."

    def sleep(self, seconds: float) -> str:
        self._state_check("sleep")
        time.sleep(seconds)
        return f"Slept for {seconds} seconds."


jarvis = JarvisRuntime()
