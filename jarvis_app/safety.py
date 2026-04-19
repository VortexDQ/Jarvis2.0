from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, UTC
import json
from pathlib import Path
import threading

from .paths import STATE_PATH, ensure_directories


class PCAccessError(RuntimeError):
    """Raised when a protected capability is requested while access is disabled."""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class SafetyState:
    pc_control_enabled: bool = False
    emergency_stop: bool = False
    listening_enabled: bool = False
    busy: bool = False
    last_command: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["updated_at"] = _utc_now()
        return payload


class SafetyController:
    def __init__(self, default_pc_control: bool = False) -> None:
        self._lock = threading.Lock()
        ensure_directories()
        if not STATE_PATH.exists():
            state = SafetyState(pc_control_enabled=default_pc_control, updated_at=_utc_now())
            self._write_state(state)

    def _write_state(self, state: SafetyState) -> SafetyState:
        with STATE_PATH.open("w", encoding="utf-8") as handle:
            json.dump(state.to_dict(), handle, indent=2)
        return self.get_state()

    def get_state(self) -> SafetyState:
        ensure_directories()
        if not STATE_PATH.exists():
            return self._write_state(SafetyState())
        with STATE_PATH.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return SafetyState(
            pc_control_enabled=bool(payload.get("pc_control_enabled", False)),
            emergency_stop=bool(payload.get("emergency_stop", False)),
            listening_enabled=bool(payload.get("listening_enabled", False)),
            busy=bool(payload.get("busy", False)),
            last_command=str(payload.get("last_command", "")),
            updated_at=str(payload.get("updated_at", "")),
        )

    def update(self, **changes: object) -> SafetyState:
        with self._lock:
            state = self.get_state()
            for key, value in changes.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            return self._write_state(state)

    def enable_pc_control(self) -> SafetyState:
        return self.update(pc_control_enabled=True, emergency_stop=False)

    def disable_pc_control(self) -> SafetyState:
        return self.update(pc_control_enabled=False)

    def trigger_emergency_stop(self) -> SafetyState:
        return self.update(pc_control_enabled=False, emergency_stop=True, busy=False)

    def clear_emergency_stop(self) -> SafetyState:
        return self.update(emergency_stop=False)

    def set_listening(self, enabled: bool) -> SafetyState:
        return self.update(listening_enabled=enabled)

    def set_busy(self, busy: bool, last_command: str | None = None) -> SafetyState:
        changes: dict[str, object] = {"busy": busy}
        if last_command is not None:
            changes["last_command"] = last_command
        return self.update(**changes)

    def require_pc_control(self, action: str) -> None:
        state = self.get_state()
        if state.emergency_stop:
            raise PCAccessError(f"Emergency stop is active. Cannot {action}.")
        if not state.pc_control_enabled:
            raise PCAccessError(f"PC access is disabled. Cannot {action}.")


def is_path_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False

