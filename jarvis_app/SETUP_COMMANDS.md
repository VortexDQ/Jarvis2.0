# Jarvis Setup - Exact Commands Reference

This document lists exactly what commands will be run during setup. Use this if you prefer manual setup.

## Platform Detection

The setup system automatically detects your OS:
- **Windows**: Runs `.bat` scripts
- **Linux/macOS**: Runs `.sh` scripts

## Windows Setup (`setup_jarvis.bat`)

### Step 1: Verification
```batch
python --version
```
Checks if Python 3.9+ is installed and in PATH.

### Step 2: Create Virtual Environment
```batch
python -m venv .venv
```
Creates an isolated Python environment in `.venv/` directory to avoid conflicts.

### Step 3: Activate Environment
```batch
.venv\Scripts\activate.bat
```
Activates the virtual environment for this session.

### Step 4: Upgrade Package Manager
```batch
python -m pip install --upgrade pip
```
Ensures pip is up-to-date for reliability.

### Step 5: Install Dependencies
```batch
pip install -q slint vosk sounddevice pyttsx3 requests pyyaml
```

Each package:
- **slint** (0.5.0): Modern UI framework
- **vosk** (0.3.45): Local voice recognition (no cloud required)
- **sounddevice** (0.4.6): Audio input device handling
- **pyttsx3** (2.90): Text-to-speech engine
- **requests** (2.31.0): HTTP requests library
- **pyyaml** (6.0): Configuration file parsing

### Step 6: Create Desktop Shortcut (Optional)
```batch
cscript create_shortcut.vbs
```
Creates a desktop shortcut that runs `run_jarvis.vbs`.

---

## Linux/macOS Setup (`setup.sh`)

### Step 1: Verification
```bash
python3 --version
```
Checks if Python 3.9+ is installed.

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```
Creates an isolated Python environment in `venv/` directory.

### Step 3: Activate Environment
```bash
source venv/bin/activate
```
Activates the virtual environment for this session.

### Step 4: Upgrade Package Manager
```bash
pip install --upgrade pip
```
Ensures pip is up-to-date.

### Step 5: Install Dependencies
```bash
pip install -q slint vosk sounddevice pyttsx3 requests pyyaml
```
Same packages as Windows setup.

### Step 6: Make Launcher Executable
```bash
chmod +x run_jarvis.sh
```
Makes the launcher script executable (automatic in setup.sh).

---

## Manual Setup (If Preferred)

If you want complete control, follow these steps:

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis/jarvis_app
```

### 2. Create Virtual Environment
**Windows:**
```batch
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install slint==0.5.0
pip install vosk==0.3.45
pip install sounddevice==0.4.6
pip install pyttsx3==2.90
pip install requests==2.31.0
pip install pyyaml==6.0
```

### 4. Download Voice Model (Optional but Recommended)
Vosk requires a speech recognition model. Get one:

**Automatic (if setup.sh/bat handles it):**
```bash
python -m vosk download
```

**Manual:**
1. Visit: https://github.com/alphacep/vosk-models/releases
2. Download a model (e.g., `vosk-model-en-us-0.42-gigaspeech`)
3. Extract to: `./voice_model`

### 5. Configure Ollama Backend (Optional)
If using Ollama for AI:

```bash
# Download Ollama from https://ollama.ai
ollama pull qwen2.5:7b-instruct

# Start Ollama server (in separate terminal)
ollama serve

# In Jarvis settings.json, ensure:
# "api_base": "http://127.0.0.1:11434"
```

### 6. First Launch
```bash
python -m jarvis_app
```

---

## What Each Launcher Does

### `run_jarvis.vbs` (Windows - Double-click)
- Runs `run_jarvis.bat` silently (hidden window)
- Best for: Everyday use

```vbs
Set objShell = CreateObject("WScript.Shell")
objShell.Run "run_jarvis.bat", 0, False
```

### `run_jarvis.bat` (Windows - Terminal visible)
```batch
@echo off
.venv\Scripts\activate.bat
python -m jarvis_app
pause
```

### `run_jarvis.sh` (Linux/macOS)
```bash
#!/bin/bash
source venv/bin/activate
python -m jarvis_app
```

### `check_dependencies.bat` (Windows - Verify packages)
Tests each package:
```batch
python -c "import slint; print('slint OK')"
python -c "import vosk; print('vosk OK')"
python -c "import sounddevice; print('sounddevice OK')"
python -c "import pyttsx3; print('pyttsx3 OK')"
python -c "import requests; print('requests OK')"
python -c "import yaml; print('pyyaml OK')"
```

---

## Environment Variables (Advanced)

If needed, you can set these before running:

**Windows:**
```batch
set JARVIS_HOME=C:\path\to\jarvis
set JARVIS_CONFIG=C:\custom\settings.json
set OLLAMA_HOST=http://localhost:11434
python -m jarvis_app
```

**Linux/macOS:**
```bash
export JARVIS_HOME=/path/to/jarvis
export JARVIS_CONFIG=/custom/settings.json
export OLLAMA_HOST=http://localhost:11434
python -m jarvis_app
```

---

## Troubleshooting Setup

### Python Not Found
```
Error: Python 3 is not installed or not in PATH
```
**Solution**: 
- Download Python from https://www.python.org
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Restart terminal and try again

### Virtual Environment Failed
```
Error: Failed to create virtual environment
```
**Solution**:
```bash
# Windows
pip install virtualenv
python -m virtualenv .venv

# Linux/macOS
sudo apt-get install python3-venv  # Ubuntu/Debian
brew install python3                # macOS
```

### Package Installation Failed
```
ERROR: Could not install packages due to an EnvironmentError
```
**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Try installing again
pip install -r requirements.txt --no-cache-dir
```

### Voice Model Not Found
```
RuntimeError: Vosk model not found in ./voice_model
```
**Solution**:
```bash
# Download model
cd voice_model
wget https://github.com/alphacep/vosk-models/releases/download/0.42/vosk-model-en-us-0.42-gigaspeech.zip
unzip vosk-model-en-us-0.42-gigaspeech.zip
```

---

## Clean Installation from Scratch

If you want to completely reset:

**Windows:**
```batch
REM Remove virtual environment
rmdir /s /q .venv

REM Remove cache
rmdir /s /q __pycache__

REM Re-run setup
setup_jarvis.bat
```

**Linux/macOS:**
```bash
# Remove virtual environment
rm -rf venv

# Remove cache
find . -type d -name __pycache__ -exec rm -r {} +

# Re-run setup
chmod +x setup.sh
./setup.sh
```

---

## Continuous Integration / Docker

For CI/CD or Docker deployment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "jarvis_app"]
```

---

## FAQ

**Q: Do I need to run setup every time?**
A: No, only once. The environment is saved in `venv/` or `.venv/`.

**Q: Can I use a different Python version?**
A: Python 3.9+ is required. Check with `python --version`.

**Q: What if I have multiple Python versions?**
A: Use `python3` on Linux/macOS, `py -3.11` on Windows.

**Q: Do I need admin/sudo?**
A: No, setup installs to user's home directory. Only needed for system packages.

**Q: Can I use conda instead?**
A: Yes, create environment with `conda create -n jarvis python=3.11` then `pip install -r requirements.txt`.

---

## Support

For issues during setup:
1. Check `logs/jarvis_errors.log` for details
2. Read `TROUBLESHOOTING.md` 
3. Open an issue on GitHub with the error output
4. Include your OS, Python version, and error traceback
