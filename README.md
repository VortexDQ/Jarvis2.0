# Jarvis2.0
This is an opensource project about jarvis. It's an premade model of Jarvis where it listens to you're microphone and complete your unique requests on a daily basis,

# Jarvis Local

Jarvis Local is a cross-platform desktop assistant that wraps [Open Interpreter](https://docs.openinterpreter.com/) with a local Ollama model, offline voice input, a `jarvis` wake word, user-profile context, and explicit PC-access safety controls.

## What it does

- Uses Open Interpreter for local code-driven computer actions
- Uses Ollama for local model inference only, with no cloud API keys
- Listens for the wake word `jarvis`
- Builds a local identity/profile summary from settings plus user-approved files
- Can search files, read and write text files, capture the screen, and automate mouse/keyboard input
- Includes a master PC-access toggle and an emergency stop
- Includes Windows and Linux startup installers

## Safety model

The assistant is intentionally wired so that direct computer control is not always on:

- The GUI has an `Enable PC Access` button
- `Emergency Stop` immediately disables PC access
- Runtime helper functions check the toggle state before moving the mouse, pressing keys, reading/writing files, or capturing the screen
- File access is limited to configured allowlisted roots
- `pyautogui` failsafe remains enabled, so moving the mouse to the top-left corner aborts active mouse automation

## Requirements

- Python `3.11`
- Ollama running locally
- A pulled Ollama model, for example `qwen2.5:7b-instruct`
- A local Vosk speech model placed under `models/`

Open Interpreter's current docs recommend Python `3.10` or `3.11`, so this project pins to `3.11`.

## Quick start on Windows

```powershell
.\scripts\bootstrap_windows.ps1
ollama pull qwen2.5:7b-instruct
.\.venv\Scripts\python -m jarvis_app.doctor
.\.venv\Scripts\python -m jarvis_app
```

## Quick start on Linux

```bash
chmod +x ./scripts/bootstrap_linux.sh
./scripts/bootstrap_linux.sh
ollama pull qwen2.5:7b-instruct
./.venv/bin/python -m jarvis_app.doctor
./.venv/bin/python -m jarvis_app
```

## Configure your identity and permissions

Edit [`config/settings.yaml`](config/settings.yaml) after first launch:

- Fill in your name and notes
- Set your preferred Ollama model
- Adjust allowlisted file roots
- Point `voice.vosk_model_path` at your downloaded Vosk model
- Adjust the folders Jarvis can scan for personal context

## Boot startup

Install autostart:

- Windows: `.\scripts\install_startup_windows.ps1`
- Linux: `./scripts/install_startup_linux.sh`

Remove autostart:

- Windows: `.\scripts\uninstall_startup_windows.ps1`
- Linux: `./scripts/uninstall_startup_linux.sh`

## Download the offline speech model

Use the included helper scripts to fetch the default Vosk English model into `models/`:

- Windows: `.\scripts\download_vosk_model_windows.ps1`
- Linux: `./scripts/download_vosk_model_linux.sh`

## Linux note

Mouse and keyboard automation is most reliable on Windows and Linux X11. Some Wayland desktops restrict synthetic input and screen capture; in those environments Jarvis may still chat, search files, and run commands, but GUI automation can be limited by the OS.
