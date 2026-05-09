# tests/architecture/enforcement/test_ports_rules.py

from pathlib import Path

ROOT = Path("src")


def read(file: Path) -> str:
    return file.read_text()


def test_ports_are_clean():
    """
    Ports must not depend on concrete implementations.
    """

    forbidden = [
        "django",
        "sqlalchemy",
        "paho.mqtt",
        "src.infrastructure",
        "src.interfaces",
    ]

    ports_dir = ROOT / "application" / "ports"

    for file in ports_dir.rglob("*.py"):
        content = read(file)

        for f in forbidden:
            assert f not in content, (
                f"[ARCH VIOLATION] Ports must be pure abstractions -> {file}"
            )