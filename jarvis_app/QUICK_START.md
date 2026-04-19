# Jarvis AI - Quick Start Guide

## ⚡ 30-Second Setup

1. **Double-click** → `setup_jarvis.bat`
2. Follow prompts → Install packages
3. Done! Launch with **`Jarvis`** shortcut on desktop

## 🚀 Running Jarvis

### Easiest Way
- **Double-click** `run_jarvis.vbs` (silent, no console)
- Or **right-click** → Open desktop `Jarvis` shortcut

### From Command Line
```powershell
.\run_jarvis.bat
```

## 🎙️ Using Voice Commands

**Say:** "Jarvis" (wake word)

**Example commands:**
- "What time is it?"
- "Open file explorer"
- "Tell me a joke"
- "Close Jarvis"

## 🎮 UI Controls

| Button | Action |
|--------|--------|
| **MUTE SYSTEM** | Silence audio output |
| **ACCESS PC** | Enable/disable system control |
| **Status Circle** | Shows system state + speaker animation |

## ⚙️ First Launch

A dialog will ask: **"Use modern Slint UI or classic Tkinter?"**
- **Yes** = Beautiful modern UI (recommended)
- **No** = Classic interface

Change anytime in `jarvis_config.json`:
```json
{
  "ui_enabled_on_startup": true
}
```

## ❌ Troubleshooting

**"Module not found" error**
→ Run `check_dependencies.bat` to reinstall packages

**Voice not working**
→ Check microphone in Windows Settings
→ Make sure to say "Jarvis" first

**UI looks weird**
→ Switch to classic UI in config
→ Update your graphics drivers

**Permission denied**
→ Run PowerShell as Administrator
→ Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 📁 File Guide

| File | Purpose |
|------|---------|
| `setup_jarvis.bat` | **First time setup** |
| `run_jarvis.bat` | Run with console |
| `run_jarvis.vbs` | Run silently (recommended) |
| `check_dependencies.bat` | Fix missing packages |
| `jarvis_config.json` | User preferences |
| `settings.yaml` | Voice & AI settings |

## 💡 Pro Tips

1. **Always-on-top** → UI stays visible over other windows
2. **Drag UI** → Click title bar to move window
3. **Quick disable** → Button in UI to stop listening
4. **Backup configs** → Automatic backups in `backups/` folder

## 🆘 Need Help?

- Check `README.md` for full documentation
- Review `logs/jarvis_errors.log` for errors
- Try switching UI modes in `jarvis_config.json`

---

**Ready?** Double-click `setup_jarvis.bat` to get started! 🚀
