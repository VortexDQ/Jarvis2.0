# Contributing to Jarvis

Thank you for your interest in contributing to Jarvis! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and constructive
- Help others learn and grow
- Report issues responsibly
- Focus on the code, not the person

## Ways to Contribute

### 1. Report Bugs
Found a bug? Help us fix it!

1. Check [existing issues](../../issues) first
2. Create a new issue with:
   - **Title**: Clear, descriptive title
   - **Environment**: OS, Python version, setup method
   - **Steps to reproduce**: Exact steps to trigger the bug
   - **Expected vs Actual**: What should happen vs what happened
   - **Logs**: Include relevant error logs from `logs/jarvis_errors.log`

### 2. Suggest Features
Have an idea for improvement?

1. Check [discussions](../../discussions) for similar ideas
2. Create a discussion or issue with:
   - **Problem**: What problem does this solve?
   - **Solution**: How would you implement it?
   - **Alternatives**: Other solutions considered?
   - **Examples**: Use cases and examples

### 3. Improve Documentation
Documentation is never finished!

- Fix typos and clarifications
- Add missing sections
- Improve examples
- Add diagrams or flowcharts

### 4. Write Code
Help us improve Jarvis with new features or fixes!

## Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/jarvis.git
cd jarvis/jarvis_app
```

### 2. Create Development Branch
```bash
git checkout -b feature/your-feature-name
# or for fixes:
git checkout -b fix/your-bug-fix-name
```

### 3. Set Up Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate.bat

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Development Dependencies
```bash
pip install -r requirements.txt
pip install pytest black flake8 mypy  # Dev tools
```

### 5. Make Your Changes
- Follow Python [PEP 8](https://pep8.org) style guide
- Add type hints where possible
- Write docstrings for functions/classes
- Keep functions focused and testable

### 6. Test Your Changes
```bash
# Run tests
pytest

# Format code
black jarvis_app/

# Check for issues
flake8 jarvis_app/
mypy jarvis_app/

# Manual testing
python -m jarvis_app
```

### 7. Commit Your Changes
```bash
git add .
git commit -m "Brief description of changes"
```

**Commit message guidelines:**
- Use imperative mood ("Add feature" not "Added feature")
- First line should be clear and concise
- Add details in body if needed
- Reference issues: "Fixes #123"

Example:
```
Add blocklist validation to security settings

- Add method to validate blocklist entries
- Add unit tests for validation
- Update settings documentation

Fixes #456
```

### 8. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request with:
- **Title**: Clear, descriptive
- **Description**: What changes, why, how to test
- **Related issues**: Links to related issues
- **Testing**: How you tested it
- **Screenshots**: If UI changes

## Code Style Guidelines

### Python Style
```python
# Use type hints
def get_settings() -> JarvisSettings:
    """Load and return the Jarvis settings."""
    pass

# Use docstrings
class JarvisAssistant:
    """Main AI assistant class.
    
    Handles voice recognition, command execution,
    and response generation.
    """

# Follow PEP 8
# - Max line length: 100 characters
# - Use double quotes for strings
# - 4 spaces for indentation
# - One blank line between functions
# - Two blank lines between classes
```

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `JarvisAssistant`)
- **Functions/methods**: `snake_case` (e.g., `get_settings()`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_BACKUPS`)
- **Private methods**: `_leading_underscore` (e.g., `_internal_method()`)

### Comments
```python
# Good: Explains WHY, not WHAT
if response_length > MAX_TOKENS:
    # Truncate response to fit within model limits
    response = response[:MAX_TOKENS]

# Bad: Obvious from the code
response = response[:MAX_TOKENS]  # Truncate response
```

## Testing Guidelines

### Write Tests
```python
# tests/test_settings.py
import pytest
from jarvis_app.settings_manager import JarvisSettings

def test_settings_validation():
    """Test settings validation."""
    settings = JarvisSettings()
    valid, msg = settings.validate()
    assert valid is True

def test_blocked_command_detection():
    """Test blocklist detection."""
    settings = JarvisSettings()
    assert settings.is_blocked_command("delete all") is True
    assert settings.is_blocked_command("hello world") is False
```

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_settings.py

# Run with coverage
pytest --cov=jarvis_app
```

## Pull Request Process

1. **Update tests** - Add tests for new features
2. **Update docs** - Update relevant documentation
3. **Check CI** - Ensure all checks pass
4. **Request review** - Ask maintainers to review
5. **Address feedback** - Make requested changes
6. **Merge** - Maintainer will merge when ready

## Project Structure

```
jarvis_app/
├── assistant.py         # Main AI logic
├── settings_manager.py  # Settings management
├── voice.py            # Voice recognition/TTS
├── safety.py           # PC access controls
├── error_handler.py    # Error handling
├── ui.py               # Tkinter UI
├── slint_ui.py         # Slint UI
├── UI/                 # Slint UI definition
├── settings.json       # Configuration template
└── tests/              # Unit tests
```

## Architecture Overview

```
┌─ Voice Recognition (Vosk)
│  └─ Wake Word Detection
│     └─ Command Parsing
│        └─ Safety Check
│           └─ Blocklist Filter
│              └─ Execute Command
│                 └─ AI Backend (Ollama)
│                    └─ Response
│                       └─ Text-to-Speech
└─ UI (Slint or Tkinter)
```

## Common Tasks

### Add a New Setting
1. Update `JarvisSettings` dataclass in `settings_manager.py`
2. Add default value to `settings.json`
3. Update `SETTINGS_GUIDE.md`
4. Add validation in `JarvisSettings.validate()`
5. Add tests in `tests/test_settings.py`

### Add a New Safety Feature
1. Update `SafetyController` in `safety.py`
2. Add validation logic in `assistant.py`
3. Log actions in `error_handler.py`
4. Update `SETTINGS_GUIDE.md`
5. Add tests and documentation

### Update UI
1. Modify `UI/ui/jarvis.slint` for Slint UI
2. Or modify `ui.py` for Tkinter UI
3. Update `slint_ui.py` or `ui.py` bindings
4. Test on multiple screen resolutions
5. Document changes in `README.md`

## Debugging Tips

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Settings
```python
from settings_manager import get_settings
settings = get_settings()
print(settings.to_dict())
```

### Test Voice Recognition
```bash
python -c "
from voice import VoiceLoop
from settings_manager import get_settings
settings = get_settings()
loop = VoiceLoop(settings)
print('Listening... (say your wake word)')
loop.start()
import time
time.sleep(30)
loop.stop()
"
```

### View Error Logs
```bash
# Windows
type logs\jarvis_errors.log

# Linux/macOS
cat logs/jarvis_errors.log
```

## Documentation Guidelines

### Markdown Files
- Use clear headers (H1, H2, H3)
- Include examples and code blocks
- Add table of contents for long docs
- Link related files
- Keep line length under 100 characters

### Docstrings
```python
def run_command(self, command: str, source: str = "text") -> CommandOutcome:
    """Execute a command with safety checks.
    
    Args:
        command: The command to execute
        source: Source of command (text or voice)
        
    Returns:
        CommandOutcome with response text and metadata
        
    Raises:
        SecurityException: If command is blocked
        
    Example:
        >>> outcome = assistant.run_command("what time is it")
        >>> print(outcome.reply)
    """
```

## Release Process

Maintainers use this process for releases:

1. Update version in code
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.2.3`
4. Create GitHub Release
5. Announce in discussions

## Getting Help

- **Questions?** Ask in [Discussions](../../discussions)
- **Need info?** Check the [documentation files](.)
- **Something unclear?** Create an issue describing the confusion
- **Just want to chat?** Start a discussion!

## License

By contributing, you agree your contributions are licensed under the MIT License.

## Thank You! 🎉

We appreciate all contributions, from bug reports to code to documentation. You're helping make Jarvis better for everyone!

---

Happy contributing! 🚀
