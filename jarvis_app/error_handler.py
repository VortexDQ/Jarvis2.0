from __future__ import annotations

import json
import shutil
import threading
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


class ErrorHandler:
    """Centralized error handling and logging for Jarvis."""

    def __init__(self, log_callback: Callable[[str], None] | None = None) -> None:
        self._log_callback = log_callback or print
        self._error_log_path = Path(__file__).parent / "logs" / "jarvis_errors.log"
        self._error_log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log_error(self, error_type: str, message: str, exc_info: Exception | None = None) -> None:
        """Log an error with timestamp and traceback if available."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "type": error_type,
            "message": message,
        }

        if exc_info:
            log_entry["exception"] = str(exc_info)
            log_entry["traceback"] = traceback.format_exc()

        with self._lock:
            try:
                self._error_log_path.write_text(
                    json.dumps(log_entry, indent=2),
                    mode="a"
                )
            except Exception as e:
                self._log_callback(f"Failed to write error log: {e}")

        # Also log to console/callback
        self._log_callback(f"[ERROR] {error_type}: {message}")

    def check_dependencies(self) -> dict[str, bool]:
        """Check if all required dependencies are available."""
        dependencies = {
            "slint": False,
            "vosk": False,
            "sounddevice": False,
            "pyttsx3": False,
            "requests": False,
            "yaml": False,
        }

        for dep in dependencies:
            try:
                __import__(dep)
                dependencies[dep] = True
            except ImportError:
                dependencies[dep] = False

        return dependencies

    def verify_voice_model(self, model_path: Path) -> bool:
        """Verify that Vosk voice model exists and is valid."""
        if not model_path.exists():
            self.log_error(
                "MISSING_MODEL",
                f"Voice model not found at: {model_path}"
            )
            return False

        # Check for essential Vosk model files
        required_files = ["am/final.mdl", "conf/model.conf"]
        for required in required_files:
            if not (model_path / required).exists():
                self.log_error(
                    "INVALID_MODEL",
                    f"Voice model missing file: {required}"
                )
                return False

        return True


class BackupManager:
    """Manage backups of configuration and important files."""

    def __init__(self, backup_dir: Path | None = None) -> None:
        self.backup_dir = backup_dir or Path(__file__).parent / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self._max_backups = 5
        self._lock = threading.Lock()

    def create_backup(self, file_path: Path, backup_name: str | None = None) -> bool:
        """Create a timestamped backup of a file."""
        if not file_path.exists():
            return False

        try:
            with self._lock:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = backup_name or file_path.stem
                backup_path = self.backup_dir / f"{backup_name}_{timestamp}.bak"

                if file_path.is_file():
                    shutil.copy2(file_path, backup_path)
                elif file_path.is_dir():
                    shutil.copytree(file_path, backup_path)

                # Clean up old backups
                self._cleanup_old_backups(backup_name)
                return True
        except Exception as e:
            print(f"Backup error: {e}")
            return False

    def _cleanup_old_backups(self, backup_name: str) -> None:
        """Keep only the most recent backups."""
        pattern = f"{backup_name}_*.bak"
        backups = sorted(self.backup_dir.glob(pattern))

        while len(backups) > self._max_backups:
            old_backup = backups.pop(0)
            try:
                if old_backup.is_dir():
                    shutil.rmtree(old_backup)
                else:
                    old_backup.unlink()
            except Exception:
                pass

    def restore_backup(self, backup_name: str, target_path: Path) -> bool:
        """Restore a backup to its original location."""
        backups = sorted(self.backup_dir.glob(f"{backup_name}_*.bak"))

        if not backups:
            return False

        latest_backup = backups[-1]

        try:
            with self._lock:
                if latest_backup.is_dir():
                    shutil.rmtree(target_path, ignore_errors=True)
                    shutil.copytree(latest_backup, target_path)
                else:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(latest_backup, target_path)
                return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False
