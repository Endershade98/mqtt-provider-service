# tests/architecture/enforcement/test_application_purity.py

from pathlib import Path

ROOT = Path("src/application")


def read(file: Path) -> str:
    return file.read_text()


def test_application_is_isolated():
    forbidden = [
        "django",
        "flask",
        "fastapi",
        "src.infrastructure.persistence.django.models",
        "src.interfaces",
    ]

    for file in ROOT.rglob("*.py"):
        content = read(file)

        for f in forbidden:
            assert f not in content, (
                f"[ARCH VIOLATION] Application layer must not depend on {f} -> {file}"
            )