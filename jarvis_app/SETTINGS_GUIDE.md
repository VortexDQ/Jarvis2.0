# Jarvis Settings Configuration Guide

The `settings.json` file controls all aspects of Jarvis behavior. Edit it to customize Jarvis for your needs.

## Settings Structure

### UI Settings
```json
"ui": {
  "enabled_on_startup": false,    // Auto-launch modern Slint UI (vs classic Tkinter)
  "theme": "dark",                // UI theme: dark, light, system
  "always_on_top": true,          // Keep Jarvis window above all others
  "window_opacity": 1.0           // Transparency: 0.0 (transparent) to 1.0 (opaque)
}
```

### Voice Settings
```json
"voice": {
  "enabled": true,                        // Enable voice recognition
  "wake_word": "jarvis",                  // Word to activate listening (case-insensitive)
  "sample_rate": 16000,                   // Audio quality in Hz (16000 recommended)
  "tts_enabled": true,                    // Enable text-to-speech responses
  "tts_voice_name": "",                   // TTS voice (empty = system default)
  "auto_start_on_launch": true,           // Start listening immediately on launch
  "vosk_model_path": "./voice_model"      // Path to voice recognition model
}
```

### PC Access Settings
```json
"pc_access": {
  "enabled_on_startup": false,            // Allow system commands (disabled by default for safety)
  "allow_file_operations": false,         // Allow file read/write/delete
  "allow_shell_commands": false,          // Allow shell command execution
  "allow_system_info": true,              // Allow reading system information
  "allowed_commands": [],                 // Whitelist of allowed commands
  "blocked_commands": [                   // Commands that will always be blocked
    "format", "del /s", "rm -rf", "shutdown /s", "poweroff", "reboot", "halt", "kill -9", "sudo"
  ]
}
```

### AI Settings
```json
"ai": {
  "provider": "ollama",                   // AI backend: ollama, openai
  "model": "qwen2.5:7b-instruct",        // Model name to use
  "api_base": "http://127.0.0.1:11434",  // API endpoint (Ollama default)
  "api_key": "",                          // API key (for OpenAI, etc)
  "temperature": 0.7,                     // Response creativity (0.0-2.0)
  "max_tokens": 2048,                     // Maximum response length
  "timeout": 30                           // Request timeout in seconds
}
```

### Security Settings
```json
"security": {
  "enable_blocklist": true,                       // Enable content filtering
  "enable_auto_backups": true,                    // Auto-backup settings
  "max_backup_count": 5,                          // Keep last N backups
  "log_all_commands": true,                       // Log all voice commands
  "require_confirmation_for_system_access": true, // Ask before PC access
  "blocklist": [
    "delete all", "format disk", "hack", "malware", "password", ...
  ]
}
```

### User Settings
```json
"user": {
  "full_name": "",                        // Your name
  "preferred_name": "",                   // How Jarvis should address you
  "pronouns": "",                         // Your pronouns (he/she/they/etc)
  "role": "",                             // Your role (developer, student, etc)
  "timezone": "UTC",                      // Your timezone
  "language": "en"                        // Language code
}
```

## Common Configuration Scenarios

### Scenario 1: Privacy-Focused Setup
```json
{
  "pc_access": {
    "enabled_on_startup": false,
    "allow_file_operations": false,
    "allow_shell_commands": false,
    "allow_system_info": false
  },
  "security": {
    "log_all_commands": false,
    "enable_auto_backups": true
  }
}
```

### Scenario 2: Power User with Full Access
```json
{
  "pc_access": {
    "enabled_on_startup": true,
    "allow_file_operations": true,
    "allow_shell_commands": true,
    "allow_system_info": true
  },
  "ai": {
    "temperature": 0.9,
    "max_tokens": 4096
  }
}
```

### Scenario 3: Linux Developer
```json
{
  "voice": {
    "wake_word": "jarvis"
  },
  "ai": {
    "model": "llama2:7b"
  },
  "security": {
    "blocked_commands": [
      "rm -rf /", "sudo rm", "apt-get purge", "pacman -R"
    ]
  }
}
```

### Scenario 4: Minimal/Headless Setup
```json
{
  "ui": {
    "enabled_on_startup": false
  },
  "voice": {
    "tts_enabled": false,
    "auto_start_on_launch": true
  }
}
```

## Safety & Blocklist

The `blocklist` array contains keywords/phrases that Jarvis will refuse to execute. This protects against:

- **Destructive Operations**: "format disk", "wipe drive", "destroy"
- **Security Threats**: "hack", "exploit", "malware"
- **Sensitive Data**: "password", "credit card", "social security"
- **System Compromise**: "disable antivirus", "disable firewall"
- **Network Attacks**: "ddos", "flood", "scan networks"

To add custom blocked phrases:
1. Open `settings.json`
2. Find the `security.blocklist` array
3. Add new phrases in lowercase
4. Save and restart Jarvis

Example:
```json
"blocklist": [
  "...existing items...",
  "my private phrase",
  "custom blocked command"
]
```

## How to Edit Settings

### Method 1: Direct Edit (Recommended)
1. Open `settings.json` in any text editor
2. Modify the values
3. Save the file
4. Restart Jarvis to apply changes

### Method 2: Command Line (Linux/macOS)
```bash
# Edit settings in your editor
nano settings.json

# Or use sed to modify values
sed -i 's/"enabled_on_startup": false/"enabled_on_startup": true/' settings.json
```

### Method 3: Reset to Defaults
Delete `settings.json` and Jarvis will create a fresh copy on next launch.

## Important Notes

- **JSON Syntax**: Settings must be valid JSON. Use a JSON validator if unsure.
- **Restart Required**: Changes take effect after restarting Jarvis
- **Backups**: Auto-backups preserve previous settings versions
- **Reset**: Delete `settings.json` to restore factory defaults
- **Validation**: Jarvis validates settings on startup and logs any issues

## Troubleshooting

**Q: Jarvis won't recognize my voice commands**
- Check `voice.wake_word` is set correctly
- Ensure `voice.enabled` is `true`
- Check microphone permissions in system settings

**Q: Jarvis is too chatty or too brief**
- Adjust `ai.temperature` (lower = consistent, higher = creative)
- Modify `ai.max_tokens` for response length

**Q: Commands are being blocked**
- Check `security.blocklist` for matching keywords
- Disable blocklist temporarily: `"enable_blocklist": false` (not recommended)
- Add phrase to `allowed_commands` whitelist

**Q: PC access commands not working**
- Ensure `pc_access.enabled_on_startup` is `true`
- Check specific permissions like `allow_shell_commands`
- Verify command is not in `blocked_commands`

## Default Settings

A fresh `settings.json` file is created on first launch with these defaults:

- **UI**: Modern Slint UI disabled, Dark theme, Always-on-top, Full opacity
- **Voice**: Enabled, "jarvis" wake word, Auto-start on launch
- **PC Access**: Disabled for safety (user must opt-in)
- **AI**: Ollama backend with qwen2.5:7b-instruct model
- **Security**: Blocklist enabled, Auto-backups enabled, Command logging enabled
- **User**: All fields empty (optional personalization)

## More Information

- For file structure: See `FILE_STRUCTURE.md`
- For quick start: See `QUICK_START.md`
- For technical details: See `IMPLEMENTATION_SUMMARY.md`
- For full docs: See `README.md`
