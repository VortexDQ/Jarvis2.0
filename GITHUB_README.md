# 🤖 Jarvis - Cross-Platform AI Assistant

A lightweight, privacy-focused AI assistant for Windows and Linux that runs entirely locally with no cloud dependencies.

**Features:**
- 🎤 Voice activation with "Jarvis" wake word
- 🧠 Local AI backend (Ollama) - no API keys needed  
- 🔒 Security blocklist for sensitive commands
- ⚙️ Comprehensive settings system
- 💻 Modern Slint UI with speaker animation (optional)
- 🛡️ Emergency stop and PC access controls
- 💾 Automatic backups and error handling
- 🔧 Works on both Windows and Linux

## 📋 Quick Start

### 30 Second Setup

**Windows:**
1. Download and extract this repository
2. Double-click `setup_jarvis.bat`
3. Wait for installation to complete
4. Double-click `run_jarvis.vbs` to launch

**Linux/macOS:**
1. Download and extract this repository
2. Open terminal in the folder
3. Run: `chmod +x setup.sh && ./setup.sh`
4. Run: `python -m jarvis_app`

### What Gets Installed

The setup script installs these packages (non-invasive, local to project):
- **slint** - Modern UI framework
- **vosk** - Local voice recognition
- **sounddevice** - Audio input handling
- **pyttsx3** - Text-to-speech engine
- **requests** - HTTP requests library
- **pyyaml** - Configuration parsing

See [SETUP_COMMANDS.md](SETUP_COMMANDS.md) for exact command details.

## 🎯 Usage

### First Launch
On first launch, you'll be asked to choose:
- **Modern Slint UI** (recommended) - Beautiful, responsive interface
- **Classic Tkinter UI** - Simple, lightweight alternative

Your choice is saved in `settings.json` and can be changed anytime.

### Voice Commands
1. Say "Jarvis" to activate
2. Ask your question or give a command
3. Jarvis will respond with audio and text

Examples:
- "Jarvis, what time is it?"
- "Jarvis, tell me a joke"
- "Jarvis, write hello world in Python"
- "Jarvis, show me the weather"

### UI Controls
- **Mute Button** - Toggle audio output
- **PC Access Button** - Enable/disable system command execution (requires permission)
- **Status Indicator** - Shows current state (READY / SPEAKING / MUTED)

## ⚙️ Configuration

Edit `settings.json` to customize Jarvis:

```json
{
  "ui": {
    "enabled_on_startup": true,     // Auto-launch modern UI
    "always_on_top": true,          // Keep window on top
    "window_opacity": 1.0           // Transparency (0.0-1.0)
  },
  "voice": {
    "wake_word": "jarvis",          // Activation word
    "tts_enabled": true,            // Text-to-speech responses
    "auto_start_on_launch": true    // Listen automatically
  },
  "pc_access": {
    "enabled_on_startup": false,    // Allow system commands (disabled by default)
    "allow_file_operations": false,
    "allow_shell_commands": false
  },
  "ai": {
    "model": "qwen2.5:7b-instruct", // Ollama model
    "temperature": 0.7              // Response creativity
  },
  "security": {
    "enable_blocklist": true,       // Prevent sensitive commands
    "blocklist": [...]              // Command blacklist
  }
}
```

For detailed settings documentation, see [SETTINGS_GUIDE.md](SETTINGS_GUIDE.md).

## 🛡️ Security Features

### Blocklist Protection
Jarvis includes a built-in blocklist to prevent execution of dangerous commands:

- Destructive operations: "format disk", "wipe drive"
- Security threats: "hack", "malware", "exploit"  
- Sensitive data: "password", "credit card"
- System compromise: "disable antivirus", "disable firewall"

You can customize this list in `settings.json`.

### PC Access Control
PC system access is **disabled by default**. Users must:
1. Enable it in settings
2. Click the UI button OR say "enable PC access"
3. Each command is logged for audit trail

### Emergency Stop
Press `Ctrl+C` in the terminal to trigger emergency stop:
- Immediately disables all PC access
- Stops voice listening
- Gracefully shuts down

## 🔧 Advanced Configuration

### Change AI Model
To use a different model:

1. Install [Ollama](https://ollama.ai)
2. Pull desired model: `ollama pull llama2:7b`
3. Update `settings.json`:
   ```json
   "ai": {
     "model": "llama2:7b"
   }
   ```

### Use Different Wake Word
Edit `settings.json`:
```json
"voice": {
  "wake_word": "hey assistant"
}
```

### Disable Voice, Text-Only Mode
```json
"voice": {
  "enabled": false,
  "auto_start_on_launch": false
}
```

Then use: `python -m jarvis_app` and type commands directly.

### Run Headless (No UI)
```json
"ui": {
  "enabled_on_startup": false
}
```

## 📁 File Structure

```
jarvis_app/
├── __main__.py              # Entry point
├── assistant.py             # Main AI assistant
├── settings_manager.py      # Settings management
├── error_handler.py         # Error handling & backups
├── voice.py                 # Voice recognition & TTS
├── safety.py                # PC access controls
├── ui.py                    # Classic UI (Tkinter)
├── slint_ui.py             # Modern UI (Slint)
├── settings.json            # Configuration file (edit this!)
├── requirements.txt         # Python dependencies
├── setup_jarvis.bat        # Windows setup
├── setup.sh                # Linux/macOS setup
├── run_jarvis.vbs          # Windows launcher (silent)
├── run_jarvis.bat          # Windows launcher (with terminal)
├── UI/
│   └── ui/
│       └── jarvis.slint    # Slint UI definition
└── logs/                    # Error logs (auto-created)
```

See [FILE_STRUCTURE.md](FILE_STRUCTURE.md) for complete documentation.

## 🐛 Troubleshooting

### "Python not found" Error
- **Windows**: Reinstall Python from https://www.python.org
  - **IMPORTANT**: Check "Add Python to PATH" during installation
- **Linux**: `sudo apt install python3.11` (Ubuntu/Debian)
- **macOS**: `brew install python3`

### Voice recognition not working
1. Check microphone in system settings
2. Test microphone: `python -c "import sounddevice; print(sounddevice.query_devices())"`
3. Vosk model not found? See [SETUP_COMMANDS.md](SETUP_COMMANDS.md#voice-model)

### "Slint not available" - Falls back to Tkinter UI
- Reinstall Slint: `pip install --upgrade slint`
- Or run with classic UI (see [Settings Guide](SETTINGS_GUIDE.md))

### Commands being blocked unexpectedly
- Check `security.blocklist` in `settings.json`
- Check `pc_access` settings (PC access may be disabled)
- Check `logs/jarvis_errors.log` for details

### Ollama not found
- Install Ollama from https://ollama.ai
- Ensure it's running in background: `ollama serve`
- Check settings: `"api_base": "http://127.0.0.1:11434"`

See [FILE_STRUCTURE.md](FILE_STRUCTURE.md) for detailed troubleshooting.

## 🔄 Updates

To update Jarvis:

```bash
# Pull latest changes
git pull

# Activate environment
# Windows: .venv\Scripts\activate.bat
# Linux/macOS: source venv/bin/activate

# Reinstall dependencies in case requirements changed
pip install -r requirements.txt

# Run
python -m jarvis_app
```

## 🗑️ Uninstallation

**Windows:**
```batch
uninstall_jarvis.bat
```

**Linux/macOS:**
```bash
rm -rf venv
rm -rf __pycache__
rm settings.json
rm logs/
```

Note: Your backups remain in `backups/` folder if you need them.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See LICENSE file

## 🔐 Privacy & Security

- **No cloud sync**: All data stays on your machine
- **No tracking**: No telemetry or usage reporting
- **No ads**: Open source, community-supported
- **Transparent**: All code is readable and reviewable
- **Blocklist**: Built-in protection against harmful commands

## 📚 Documentation

- [SETUP_COMMANDS.md](SETUP_COMMANDS.md) - Exact commands run during setup
- [SETTINGS_GUIDE.md](SETTINGS_GUIDE.md) - Complete settings reference
- [FILE_STRUCTURE.md](FILE_STRUCTURE.md) - Project structure & file descriptions
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical architecture
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

## ⭐ Show Support

If you find Jarvis useful:
- ⭐ Star this repository
- 🐛 Report issues on GitHub
- 💡 Suggest features in discussions
- 🔧 Contribute improvements

## 🚀 Roadmap

- [ ] Web dashboard for settings
- [ ] Custom AI model support
- [ ] Multi-language support
- [ ] Android companion app
- [ ] Integration with smart home systems
- [ ] Advanced scheduling
- [ ] Chat history export

## ❓ FAQ

**Q: Is my data sent to the cloud?**  
A: No, everything runs locally. No internet required after setup.

**Q: Can I use my own AI model?**  
A: Yes, any Ollama-compatible model works.

**Q: Can Jarvis access the internet?**  
A: Only if explicitly commanded and your settings allow it.

**Q: What's the performance impact?**  
A: Minimal when idle. Uses ~50MB RAM, ~0% CPU at rest.

**Q: Can I use this commercially?**  
A: Yes, MIT license allows commercial use.

## 📧 Support

- 📖 Check documentation files first
- 🐛 Report bugs: GitHub Issues
- 💬 Ask questions: GitHub Discussions
- 📧 Email: (contact info if applicable)

---

Made with ❤️ for developers who value privacy and simplicity.
