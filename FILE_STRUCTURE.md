# Jarvis Project Structure & Files Guide

## 📂 Directory Overview

```
jarvis_app/
├── 🚀 LAUNCHER SCRIPTS (Main Entry Points)
│   ├── setup_jarvis.bat          ← First time setup
│   ├── run_jarvis.bat            ← Launch with console
│   ├── run_jarvis.vbs            ← Launch silently (recommended)
│   ├── check_dependencies.bat    ← Fix missing packages
│   └── uninstall_jarvis.bat      ← Clean remove
│
├── 📖 DOCUMENTATION
│   ├── README.md                 ← Full documentation
│   ├── QUICK_START.md            ← 30-second setup
│   └── FILE_STRUCTURE.md         ← This file
│
├── ⚙️ CONFIGURATION
│   ├── jarvis_config.json        ← User preferences (UI mode, voice, etc)
│   ├── settings.yaml             ← Voice recognition & AI settings
│   ├── requirements.txt          ← Python dependencies list
│   └── .gitignore                ← Git ignore patterns
│
├── 🐍 PYTHON SOURCE CODE
│   ├── __main__.py               ← Main entry point
│   ├── __init__.py               ← Package initialization
│   ├── slint_ui.py               ← Modern Slint UI integration
│   ├── ui.py                     ← Classic Tkinter UI (fallback)
│   ├── assistant.py              ← Core AI assistant logic
│   ├── voice.py                  ← Voice recognition & TTS
│   ├── error_handler.py          ← Error handling & backups
│   ├── config.py                 ← Configuration management
│   ├── runtime.py                ← Runtime execution engine
│   ├── interpreter_bridge.py     ← Code interpreter interface
│   ├── safety.py                 ← Safety & access control
│   ├── profile.py                ← User profile management
│   ├── paths.py                  ← Path utilities
│   └── doctor.py                 ← System diagnostics
│
├── 🎨 UI DEFINITION
│   └── UI/ui/
│       └── jarvis.slint          ← Slint UI component definition
│
├── 📁 RUNTIME DIRECTORIES (Auto-created)
│   ├── .venv/                    ← Python virtual environment
│   ├── logs/                     ← Error logs
│   ├── backups/                  ← Configuration backups
│   └── __pycache__/              ← Python cache
│
└── 🦀 RUST SLINT PROJECT (Optional)
    └── rust_ui/                  ← Standalone Rust Slint launcher
        ├── Cargo.toml
        ├── src/main.rs
        └── src/jarvis.slint
```

## 🚀 Launcher Scripts

### `setup_jarvis.bat`
**Purpose:** First-time installation setup
**When to run:** First time only, or to reinstall
**What it does:**
- Creates Python virtual environment
- Installs all dependencies
- Creates desktop shortcut
- Launches Jarvis for testing

### `run_jarvis.bat`
**Purpose:** Standard launch with console window
**When to run:** Troubleshooting or development
**What it does:**
- Activates Python environment
- Shows console output
- Runs Jarvis application

### `run_jarvis.vbs`
**Purpose:** Silent launcher for regular use
**When to run:** Every day (recommended)
**What it does:**
- Runs Jarvis without console window
- No command prompt appears
- Perfect for always-running assistant

### `check_dependencies.bat`
**Purpose:** Fix missing or broken packages
**When to run:** If you get module not found errors
**What it does:**
- Checks each required package
- Reinstalls missing packages
- Verifies installation

### `uninstall_jarvis.bat`
**Purpose:** Clean removal of Jarvis
**When to run:** Before reinstalling or when removing
**What it does:**
- Removes virtual environment
- Preserves user settings & backups
- Keeps configuration files

## ⚙️ Configuration Files

### `jarvis_config.json`
**User Preferences**
```json
{
  "ui_enabled_on_startup": false,      // true = Slint UI, false = Tkinter
  "auto_enable_voice": true,           // Start listening on launch
  "always_on_top": true,               // Keep window on top
  "window_opacity": 1.0,               // 0.0-1.0 transparency
  "backup_enabled": true               // Auto-backup configs
}
```

### `settings.yaml`
**Voice & AI Configuration**
```yaml
voice:
  enabled: true
  wake_word: "jarvis"               # Wake word to trigger listening
  sample_rate: 16000
  vosk_model_path: ./voice_model
  tts_enabled: true
  tts_voice_name: ""                # Leave empty for default

ollama:
  api_base: http://127.0.0.1:11434  # Ollama server address
  model: qwen2.5:7b-instruct        # Model to use
```

### `requirements.txt`
**Python Dependencies**
- `slint==0.5.0` - Modern UI framework
- `vosk==0.3.45` - Voice recognition
- `sounddevice==0.4.6` - Audio input
- `pyttsx3==2.90` - Text-to-speech
- `requests==2.31.0` - HTTP requests
- `pyyaml==6.0` - YAML parsing

## 🐍 Python Modules

### `__main__.py`
**Entry Point & UI Selection**
- Detects first launch
- Shows UI selection dialog
- Routes to Slint or Tkinter UI
- Handles errors gracefully

### `slint_ui.py`
**Modern Slint UI Integration**
- Loads and compiles Slint components
- Handles callbacks (mute, PC access)
- Manages speaker animation
- Provides fallback to Tkinter

### `ui.py`
**Classic Tkinter UI (Fallback)**
- Traditional Python GUI
- Used if Slint fails
- All core functionality available
- Less modern appearance

### `assistant.py`
**Core AI Assistant**
- Manages voice loop
- Handles commands
- Coordinates with Ollama backend
- Safety control

### `voice.py`
**Voice Recognition & TTS**
- Vosk speech-to-text
- pyttsx3 text-to-speech
- Wake word detection
- Audio streaming

### `error_handler.py`
**Error Handling & Backups**
- Centralized error logging
- Automatic backups
- Dependency checking
- Recovery mechanisms

### `config.py`
**Configuration Management**
- Loads YAML settings
- Configuration validation
- Path expansion

### Other Modules
- `runtime.py` - Command execution
- `interpreter_bridge.py` - Code execution interface
- `safety.py` - PC access control
- `profile.py` - User profile management
- `paths.py` - Path utilities
- `doctor.py` - System health checks

## 🎨 UI Definition

### `UI/ui/jarvis.slint`
**Slint Component**
- Modern neon glass design
- Responsive layout
- Speaker animation
- Status indicators
- Always-on-top support
- Button callbacks

**Key Features:**
- Dynamic speaker waves when Jarvis speaks
- PC access status indicator
- Mute toggle
- CSS-inspired gradient backgrounds
- 640x720 window size

## 📁 Runtime Directories

### `.venv/`
**Python Virtual Environment**
- Auto-created by setup_jarvis.bat
- Contains Python interpreter and packages
- Isolated from system Python
- ~500MB size

### `logs/`
**Error Logs**
- `jarvis_errors.log` - Error history
- JSON formatted entries
- Timestamp, type, traceback
- Auto-created when needed

### `backups/`
**Configuration Backups**
- Auto-backup of settings.yaml
- Auto-backup of jarvis_config.json
- Timestamped filenames
- Up to 5 recent backups kept

### `__pycache__/`
**Python Cache**
- Auto-created by Python
- Compiled bytecode (.pyc files)
- Safe to delete (recreated on run)

## 🆘 Quick Reference

| Need | Run | Purpose |
|------|-----|---------|
| First setup | `setup_jarvis.bat` | Install everything |
| Launch normally | `run_jarvis.vbs` | Start Jarvis |
| Troubleshoot | `run_jarvis.bat` | Show console |
| Fix packages | `check_dependencies.bat` | Reinstall dependencies |
| Remove completely | `uninstall_jarvis.bat` | Clean uninstall |

## 🔐 Important Notes

**User Data Locations:**
- Settings: `settings.yaml` (version controlled safe)
- Config: `jarvis_config.json` (user preferences)
- Backups: `backups/` (automatic)
- Logs: `logs/` (error history)

**Never Delete:**
- `setup_jarvis.bat` - Needed for updates
- `settings.yaml` - User configuration
- `jarvis_config.json` - User preferences
- `backups/` folder - Your recovery point

**Safe to Delete:**
- `.venv/` - Can reinstall with setup
- `__pycache__/` - Recreated automatically
- `logs/` - Can recreate

---

**Need more help?** Check `README.md` for detailed documentation or `QUICK_START.md` for fast setup.
