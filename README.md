# Jarvis AI Assistant - Modern Slint UI Edition

A powerful, modern AI assistant with a beautiful always-on-top UI built with Rust's Slint framework and Python.

## Features

✨ **Modern UI**
- Neon glass design with CSS-inspired styling
- Always-on-top, draggable window
- Real-time speaker animation when Jarvis speaks
- Responsive status indicators

🎤 **Smart Voice Activation**
- Only listens when you say "jarvis"
- Full PC system access (with user control)
- Silent Ollama backend integration
- Works on launch (user-controllable)

🛡️ **Safety & Reliability**
- Automatic error handling and recovery
- Backup system for configurations
- Emergency stop functionality
- User-friendly enable/disable on startup

## Quick Start

### Option 1: Automatic Setup (Recommended)

1. **Double-click** `setup_jarvis.bat`
2. Follow the on-screen prompts
3. Choose to enable/disable the modern Slint UI
4. Desktop shortcut will be created automatically

### Option 2: Manual Setup

1. Open PowerShell in the `jarvis_app` directory
2. Run: `python -m venv .venv`
3. Run: `.venv\Scripts\activate.ps1`
4. Run: `pip install slint vosk sounddevice pyttsx3 requests pyyaml`
5. Run: `python -m jarvis_app`

### Running Jarvis

**Easy (Double-Click)**
- `run_jarvis.vbs` - Runs silently in background
- `Jarvis` desktop shortcut (created by setup)

**From Command Line**
- `run_jarvis.bat` - Shows console window

## Configuration

Edit `jarvis_config.json` to customize:
```json
{
  "ui_enabled_on_startup": false,      // Enable Slint UI on launch
  "auto_enable_voice": true,           // Auto-start voice listening
  "always_on_top": true,               // Keep UI on top
  "window_opacity": 1.0,               // Window transparency (0.0-1.0)
  "backup_enabled": true               // Enable config backups
}
```

### Voice Settings

Edit `settings.yaml` to configure:
- Wake word: `jarvis` (customize as needed)
- Voice model path
- TTS voice and rate
- Ollama API endpoint and model

## UI Controls

**MUTE SYSTEM** - Toggle audio output (visual only in current version)

**ACCESS PC** / **DISABLE PC ACCESS** - Toggle PC system control permissions

**Status Circle**
- 🔵 **READY** - System idle, waiting for commands
- 🟢 **🔊 SPEAKING** - Animated speaker waves when Jarvis responds
- 🔴 **SILENCED** - Audio muted

## Troubleshooting

### "Slint not available" error
1. Ensure you ran setup_jarvis.bat
2. Run: `pip install slint` in your Python environment
3. Falls back to classic Tkinter UI automatically

### Voice not recognizing "jarvis"
1. Speak clearly into your microphone
2. Check `settings.yaml` for correct wake word
3. Verify Vosk model is installed in the voice model directory

### UI doesn't appear
1. Check if Slint is installed: `pip show slint`
2. Try the classic Tkinter UI: modify `jarvis_config.json` and set `ui_enabled_on_startup: false`
3. Check error logs in `logs/jarvis_errors.log`

### Permission denied errors
1. Run PowerShell as Administrator
2. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## System Requirements

- **Python**: 3.9 or higher
- **OS**: Windows 10/11
- **RAM**: 2GB minimum (4GB+ recommended)
- **Audio**: Working microphone and speakers
- **Disk**: ~500MB for dependencies

## Advanced Usage

### Enable Slint UI by Default

Edit `jarvis_config.json`:
```json
{
  "ui_enabled_on_startup": true
}
```

### Backup and Restore

Backups are automatically created in the `backups/` directory:
- Configuration backups
- Settings snapshots
- Maximum 5 recent backups kept

To manually restore: Use `error_handler.py` RestoreBackup function

### View Error Logs

Check `logs/jarvis_errors.log` for detailed error information

## Architecture

```
jarvis_app/
├── __main__.py           # Entry point with UI selection
├── slint_ui.py          # Modern Slint Python integration
├── ui.py                # Classic Tkinter UI (fallback)
├── assistant.py         # Core AI assistant logic
├── voice.py             # Voice recognition and TTS
├── error_handler.py     # Error handling and backups
├── UI/ui/jarvis.slint   # Modern UI definition
├── run_jarvis.bat       # Batch launcher
├── run_jarvis.vbs       # Silent launcher
├── setup_jarvis.bat     # Installation setup
├── jarvis_config.json   # User preferences
└── settings.yaml        # Voice and AI settings
```

## Tips & Tricks

1. **Always-on-top UI** - Slint UI stays visible over other windows
2. **Drag to reposition** - Click and drag the window title to move it
3. **Quick enable/disable** - Buttons in the UI for instant control
4. **Silent operation** - Double-click `run_jarvis.vbs` for no console window
5. **Emergency stop** - Press CTRL+C in console to emergency stop

## Privacy & Security

- All voice processing is local (Vosk)
- Ollama runs on your machine (no cloud)
- Settings stored locally in `settings.yaml`
- Full PC access only when explicitly enabled
- User controls all safety features

## Performance

- Responsive UI with 60FPS animations
- Lightweight Python + Slint combination
- Minimal CPU usage at idle
- Fast voice response times (< 2 seconds typical)

## Support

For issues or questions:
1. Check error logs: `logs/jarvis_errors.log`
2. Review troubleshooting section above
3. Ensure all dependencies are installed
4. Try the classic UI as fallback

## License

[MIT License

Copyright (c) 2026 V0rtex

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.]

## Acknowledgments

- Built with [Slint](https://slint.dev/) - Modern UI framework
- Voice recognition via [Vosk](https://alphacephei.com/vosk/)
- Text-to-speech via [pyttsx3](https://pyttsx3.readthedocs.io/)
- AI powered by [Ollama](https://ollama.ai/)

---

**Enjoy your modern Jarvis AI Assistant!** 🚀
