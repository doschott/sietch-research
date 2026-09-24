"""Source text must not grow a game-client integration."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "sietch"

DENYLIST = (
    "ReadProcessMemory",
    "OpenProcess",
    "pyautogui",
    "pydirectinput",
    "frida",
    "scapy",
    "win32api",
    "ctypes.windll",
    "unreal",
    ".pak",
    "packet interception",
    "import socket",
)


def test_package_source_has_no_game_client_hooks() -> None:
    offenders: list[str] = []
    for path in PACKAGE.rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for token in DENYLIST:
            if token.lower() in text:
                offenders.append(f"{path.name}: {token}")
    assert offenders == []


def test_guard_module_documents_the_disabled_connection() -> None:
    text = (PACKAGE / "guard.py").read_text(encoding="utf-8")
    assert "Real-game connection is disabled" in text
    assert "REAL_GAME_CONNECTION_ENABLED = False" in text
