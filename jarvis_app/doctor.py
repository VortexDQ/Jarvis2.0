from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from .settings_manager import get_settings


def main() -> None:
    settings = get_settings()
    voice_model_path = Path(settings.voice.vosk_model_path).expanduser()
    if not voice_model_path.is_absolute():
        voice_model_path = Path(__file__).resolve().parent.parent / voice_model_path
    voice_model_path = voice_model_path.resolve()

    print("Jarvis Local doctor")
    print("===================")

    print(f"Python target: 3.11")
    print(f"Ollama endpoint: {settings.ai.api_base}")
    print(f"Ollama model: {settings.ai.model}")
    print(f"Vosk model path: {voice_model_path}")

    try:
        from interpreter import interpreter  # noqa: F401

        print("Open Interpreter import: OK")
    except Exception as exc:
        print(f"Open Interpreter import: FAILED ({exc})")

    if voice_model_path.exists():
        print("Vosk model: OK")
    else:
        print("Vosk model: MISSING")

    try:
        with urlopen(f"{settings.ai.api_base}/api/tags", timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
        model_names = [item.get("name", "") for item in payload.get("models", [])]
        if any(settings.ai.model == name for name in model_names):
            print("Ollama model availability: OK")
        elif model_names:
            print(f"Ollama model availability: server reachable, model missing. Found: {', '.join(model_names)}")
        else:
            print("Ollama model availability: server reachable, no models returned")
    except URLError as exc:
        print(f"Ollama reachability: FAILED ({exc})")


if __name__ == "__main__":
    main()
