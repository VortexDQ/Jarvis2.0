# Jarvis - Pre-GitHub Cleanup Checklist

Before uploading to GitHub, remove these temporary/duplicate files:

## Files to Remove

### Delete These Files (Not Needed)
```
❌ tmp_inspect.py          - Temporary debugging script
❌ slint_ui_new.py         - Duplicate of slint_ui.py (already merged)
```

### Delete These Folders (Will Recreate on Install)
```
❌ .venv/                  - Python virtual environment
❌ __pycache__/            - Python cache files
❌ logs/                   - Error logs (optional - can keep)
❌ backups/                - Old backups (optional - can keep)
```

### Files to KEEP (All Important!)
```
✅ __init__.py
✅ __main__.py
✅ assistant.py
✅ settings_manager.py     - NEW: Unified settings system
✅ settings.json           - NEW: Main configuration
✅ slint_ui.py
✅ ui.py
✅ voice.py
✅ safety.py
✅ error_handler.py
✅ And all other .py files

✅ setup_jarvis.bat        - Windows installer
✅ setup.sh                - Linux/macOS installer
✅ run_jarvis.vbs          - Windows silent launcher
✅ run_jarvis.bat          - Windows launcher
✅ run_jarvis.sh           - Linux/macOS launcher
✅ requirements.txt        - Dependencies

✅ All .md documentation files
✅ UI/ folder              - Slint UI definition
✅ rust_ui/ folder         - Optional Rust project
✅ .gitignore              - Git ignore patterns
```

## Quick Cleanup Commands

### Windows (PowerShell)
```powershell
cd C:\Users\UgurH\Downloads\Jarvis\jarvis_app

# Remove temporary files
Remove-Item -Path "tmp_inspect.py" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "slint_ui_new.py" -Force -ErrorAction SilentlyContinue

# Remove cache and virtual environment
Remove-Item -Path ".venv" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

# Optional: Remove logs and backups
# Remove-Item -Path "logs" -Recurse -Force -ErrorAction SilentlyContinue
# Remove-Item -Path "backups" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✓ Cleanup complete! Ready for GitHub."
```

### Linux/macOS (Bash)
```bash
cd ~/Downloads/Jarvis/jarvis_app

# Remove temporary files
rm -f tmp_inspect.py slint_ui_new.py

# Remove cache and virtual environment
rm -rf .venv venv __pycache__

# Optional: Remove logs and backups
# rm -rf logs backups

echo "✓ Cleanup complete! Ready for GitHub."
```

## Verify Cleanup

After cleanup, your directory should have:
- ~30 Python/configuration files
- ~9 .md documentation files
- 7 setup/launcher scripts
- 2 folders: UI/ and rust_ui/

Check with:

**Windows**:
```powershell
ls -File | Measure-Object -Property Name | Select Count
```

**Linux/macOS**:
```bash
find . -maxdepth 1 -type f | wc -l
```

## Verify Git Ignore is Working

Before pushing to GitHub, verify .gitignore is working:

```bash
# Show what will be ignored
git status --ignored

# Should NOT show:
# - .venv/ or venv/
# - __pycache__/
# - *.egg-info/
```

## Ready for GitHub!

Once cleanup is complete, follow GITHUB_UPLOAD_GUIDE.md to push to GitHub.

**Quick steps**:
1. `git init`
2. `git add .`
3. `git commit -m "Initial commit: Jarvis v1.0.0"`
4. `git remote add origin https://github.com/YOUR_USERNAME/jarvis.git`
5. `git push -u origin main`

## ✅ Final Checklist Before Push

- [ ] Deleted tmp_inspect.py
- [ ] Deleted slint_ui_new.py
- [ ] Deleted .venv/ or venv/
- [ ] Deleted __pycache__/
- [ ] Verified with `git status` (should only show tracked files)
- [ ] Tested setup on at least one platform
- [ ] All documentation files present
- [ ] settings.json and jarvis_config.json both present
- [ ] requirements.txt has correct packages
- [ ] .gitignore is configured correctly

---

Questions? Check:
- GITHUB_UPLOAD_GUIDE.md - For GitHub setup
- SETUP_COMMANDS.md - For installation help
- FINAL_SUMMARY.md - For overview
