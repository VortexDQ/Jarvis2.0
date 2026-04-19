from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Iterable

from .settings_manager import JarvisSettings
from .paths import PROFILE_SUMMARY_PATH, ROOT_DIR, ensure_directories
from .safety import is_path_within


IDENTITY_HINTS = (
    "resume",
    "cv",
    "profile",
    "about",
    "bio",
    "contact",
    "linkedin",
    "github",
    "portfolio",
)
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "AppData",
    ".cache",
}


@dataclass(slots=True)
class ProfileFinding:
    path: Path


SENSITIVE_HINTS = (
    "recovery",
    "backup",
    "secret",
    "token",
    "password",
    "credential",
    "wallet",
    "seed",
    "2fa",
    "auth",
    "private",
    "ssh",
    "key",
)


def _iter_candidate_files(roots: Iterable[Path], extensions: set[str], limit: int) -> list[Path]:
    candidates: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if len(candidates) >= limit * 4:
                break
            if not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if is_path_within(path, ROOT_DIR):
                continue
            if path.suffix.lower() not in extensions:
                continue
            lowered = path.name.lower()
            if any(hint in lowered for hint in SENSITIVE_HINTS):
                continue
            if any(hint in lowered for hint in IDENTITY_HINTS):
                candidates.append(path)
    candidates.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return candidates[:limit]


def build_profile_summary(settings: JarvisSettings) -> str:
    ensure_directories()
    findings: list[ProfileFinding] = []
    extensions = set(settings.access.text_extensions)
    for path in _iter_candidate_files(
        [_expand_path(root) for root in settings.access.profile_scan_roots],
        extensions,
        settings.access.max_profile_files,
    ):
        findings.append(ProfileFinding(path=path))

    lines = [
        f"# {settings.assistant_name} User Context",
        "",
        "## Configured Identity",
        f"- Full name: {settings.user.full_name or 'Unknown'}",
        f"- Preferred name: {settings.user.preferred_name or 'Unknown'}",
        f"- Pronouns: {settings.user.pronouns or 'Not specified'}",
        f"- Role: {settings.user.role or 'Not specified'}",
    ]

    if settings.user.notes:
        lines.append("- Notes:")
        for note in settings.user.notes:
            lines.append(f"  - {note}")

    lines.extend(["", "## Local Profile Clues"])
    if not findings:
        lines.append("- No safe identity-style files were found in the configured scan roots.")
    else:
        for finding in findings:
            lines.append(f"- {finding.path}")

    summary = "\n".join(lines).strip() + "\n"
    PROFILE_SUMMARY_PATH.write_text(summary, encoding="utf-8")
    return summary


def _expand_path(raw_path: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(raw_path))
    path = Path(expanded)
    if not path.is_absolute():
        path = ROOT_DIR / path
    return path.resolve()
