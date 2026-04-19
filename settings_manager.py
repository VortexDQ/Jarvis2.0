from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass
class UISettings:
    """UI and display settings."""
    enabled_on_startup: bool = False
    theme: str = "dark"  # dark, light, system
    always_on_top: bool = True
    window_opacity: float = 1.0
    window_title: str = "Jarvis Local"


@dataclass
class VoiceSettings:
    """Voice recognition and TTS settings."""
    enabled: bool = True
    wake_word: str = "jarvis"
    sample_rate: int = 16000
    tts_enabled: bool = True
    tts_voice_name: str = ""
    auto_start_on_launch: bool = True
    vosk_model_path: str = "./models/vosk-model-small-en-us-0.15"
    command_timeout_seconds: int = 8


@dataclass
class PCAccessSettings:
    """PC system access control settings."""
    enabled_on_startup: bool = False
    allow_file_operations: bool = False
    allow_shell_commands: bool = False
    allow_system_info: bool = True
    allowed_commands: list[str] = field(default_factory=list)
    blocked_commands: list[str] = field(default_factory=lambda: [
        "format",
        "del /s",
        "rm -rf",
        "shutdown /s",
        "poweroff",
        "reboot",
        "halt",
        "kill -9",
        "sudo",
    ])


@dataclass
class AISettings:
    """AI and backend settings."""
    provider: str = "ollama"  # ollama, openai, etc
    model: str = "qwen2.5:7b-instruct"
    api_base: str = "http://127.0.0.1:11434"
    api_key: str = ""
    temperature: float = 0.7
    max_tokens: int = 2048
    timeout: int = 30


@dataclass
class ScreenSettings:
    """Screen capture settings."""
    auto_capture_context: bool = True
    include_ocr_text_chars: int = 1500


@dataclass
class AccessSettings:
    """Filesystem and profile scan settings."""
    allowed_roots: list[str] = field(default_factory=lambda: ["~"])
    profile_scan_roots: list[str] = field(
        default_factory=lambda: ["~/Documents", "~/Desktop", "~/Downloads"]
    )
    text_extensions: list[str] = field(
        default_factory=lambda: [".txt", ".md", ".json", ".yaml", ".yml", ".ini", ".csv", ".py"]
    )
    max_profile_files: int = 30
    max_search_results: int = 50
    max_file_read_chars: int = 4000
    max_file_write_chars: int = 50000


@dataclass
class SecuritySettings:
    """Security and safety settings."""
    enable_blocklist: bool = True
    enable_auto_backups: bool = True
    max_backup_count: int = 5
    log_all_commands: bool = True
    require_confirmation_for_system_access: bool = True
    blocklist: list[str] = field(default_factory=lambda: [
        # Destructive operations
        "delete all",
        "remove all",
        "format disk",
        "wipe drive",
        "destroy",
        "erase everything",
        
        # Dangerous commands
        "hack",
        "crack",
        "malware",
        "virus",
        "exploit",
        
        # Private/sensitive
        "password",
        "credit card",
        "social security",
        "bank account",
        
        # System critical
        "disable antivirus",
        "disable firewall",
        "disable security",
        
        # External harmful
        "scan networks",
        "flood networks",
        "ddos",
        "spam",
    ])


@dataclass
class UserSettings:
    """User profile and preferences."""
    full_name: str = ""
    preferred_name: str = ""
    pronouns: str = ""
    role: str = ""
    timezone: str = "UTC"
    language: str = "en"
    notes: list[str] = field(default_factory=list)


@dataclass
class JarvisSettings:
    """Complete Jarvis configuration."""
    version: str = "1.0.0"
    assistant_name: str = "Jarvis"
    ui: UISettings = field(default_factory=UISettings)
    voice: VoiceSettings = field(default_factory=VoiceSettings)
    pc_access: PCAccessSettings = field(default_factory=PCAccessSettings)
    ai: AISettings = field(default_factory=AISettings)
    screen: ScreenSettings = field(default_factory=ScreenSettings)
    access: AccessSettings = field(default_factory=AccessSettings)
    security: SecuritySettings = field(default_factory=SecuritySettings)
    user: UserSettings = field(default_factory=UserSettings)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JarvisSettings:
        """Create settings from dictionary."""
        voice_data = dict(data.get("voice", {}))
        if voice_data.get("vosk_model_path") in (None, "", "./voice_model"):
            default_model_path = Path(__file__).resolve().parent.parent / "models" / "vosk-model-small-en-us-0.15"
            if default_model_path.exists():
                voice_data["vosk_model_path"] = str(default_model_path)

        return cls(
            version=data.get("version", "1.0.0"),
            assistant_name=data.get("assistant_name", "Jarvis"),
            ui=UISettings(**data.get("ui", {})),
            voice=VoiceSettings(**voice_data),
            pc_access=PCAccessSettings(**data.get("pc_access", {})),
            ai=AISettings(**data.get("ai", {})),
            screen=ScreenSettings(**data.get("screen", {})),
            access=AccessSettings(**data.get("access", {})),
            security=SecuritySettings(**data.get("security", {})),
            user=UserSettings(**data.get("user", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to dictionary."""
        return asdict(self)

    @classmethod
    def load(cls, path: Path | None = None) -> JarvisSettings:
        """Load settings from file."""
        if path is None:
            path = Path(__file__).parent / "settings.json"

        if path.exists():
            try:
                data = json.loads(path.read_text())
                return cls.from_dict(data)
            except Exception as e:
                print(f"Warning: Failed to load settings: {e}, using defaults")

        return cls()

    def save(self, path: Path | None = None) -> bool:
        """Save settings to file."""
        if path is None:
            path = Path(__file__).parent / "settings.json"

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(self.to_dict(), indent=2))
            return True
        except Exception as e:
            print(f"Error: Failed to save settings: {e}")
            return False

    def is_blocked_command(self, command: str) -> bool:
        """Check if a command is in the blocklist."""
        if not self.security.enable_blocklist:
            return False

        command_lower = command.lower()
        for blocked in self.security.blocklist:
            if blocked.lower() in command_lower:
                return True
        return False

    def validate(self) -> tuple[bool, str]:
        """Validate settings for consistency."""
        if not self.ai.model:
            return False, "AI model not specified"
        if self.ai.temperature < 0 or self.ai.temperature > 2:
            return False, "Temperature must be between 0 and 2"
        if not self.voice.wake_word:
            return False, "Wake word cannot be empty"
        return True, "Settings valid"


# Global settings instance
_settings: JarvisSettings | None = None


def get_settings() -> JarvisSettings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = JarvisSettings.load()
    return _settings


def set_settings(settings: JarvisSettings) -> None:
    """Set the global settings instance."""
    global _settings
    _settings = settings


def reset_settings() -> JarvisSettings:
    """Reset settings to defaults."""
    global _settings
    _settings = JarvisSettings()
    return _settings
