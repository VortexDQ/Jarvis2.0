from __future__ import annotations

import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"
RUNTIME_DIR = ROOT_DIR / "runtime"
LOG_DIR = RUNTIME_DIR / "logs"
MEMORY_DIR = RUNTIME_DIR / "memory"
SCREEN_DIR = RUNTIME_DIR / "screen"
CONVERSATIONS_DIR = RUNTIME_DIR / "conversations"
MPL_CONFIG_DIR = RUNTIME_DIR / "mplconfig"
IPYTHON_DIR = RUNTIME_DIR / "ipython"
JUPYTER_CONFIG_DIR = RUNTIME_DIR / "jupyter_config"
JUPYTER_DATA_DIR = RUNTIME_DIR / "jupyter_data"
JUPYTER_RUNTIME_DIR = RUNTIME_DIR / "jupyter_runtime"

SETTINGS_PATH = CONFIG_DIR / "settings.yaml"
SETTINGS_EXAMPLE_PATH = CONFIG_DIR / "settings.example.yaml"
STATE_PATH = RUNTIME_DIR / "state.json"
PROFILE_SUMMARY_PATH = MEMORY_DIR / "profile_summary.md"
LAST_SCREENSHOT_PATH = SCREEN_DIR / "last_screen.png"
LAST_SCREEN_OCR_PATH = SCREEN_DIR / "last_screen_ocr.txt"

os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))
os.environ.setdefault("DISABLE_TELEMETRY", "true")
os.environ.setdefault("IPYTHONDIR", str(IPYTHON_DIR))
os.environ.setdefault("JUPYTER_CONFIG_DIR", str(JUPYTER_CONFIG_DIR))
os.environ.setdefault("JUPYTER_DATA_DIR", str(JUPYTER_DATA_DIR))
os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(JUPYTER_RUNTIME_DIR))
os.environ.setdefault("JUPYTER_ALLOW_INSECURE_WRITES", "true")


def ensure_directories() -> None:
    for path in (
        CONFIG_DIR,
        RUNTIME_DIR,
        LOG_DIR,
        MEMORY_DIR,
        SCREEN_DIR,
        CONVERSATIONS_DIR,
        MPL_CONFIG_DIR,
        IPYTHON_DIR,
        JUPYTER_CONFIG_DIR,
        JUPYTER_DATA_DIR,
        JUPYTER_RUNTIME_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)
