# tests/architecture/enforcement/test_infrastructure_boundary.py

from pathlib import Path

ROOT = Path("src/infrastructure")


def read(file: Path) -> str:
    return file.read_text()


def test_infrastructure_isolation():
    forbidden = [
        "src.interfaces",  # già trovato da te
    ]

    for file in ROOT.rglob("*.py"):
        content = read(file)

        for f in forbidden:
            assert f not in content, (
                f"[ARCH VIOLATION] Infrastructure must not import interfaces -> {file}"
            )