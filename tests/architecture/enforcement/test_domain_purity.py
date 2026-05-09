# tests/architecture/enforcement/test_domain_purity.py

from pathlib import Path

ROOT = Path("src/domain")


def read(file: Path) -> str:
    return file.read_text()


def test_domain_is_isolated():
    forbidden = [
        "src.application",
        "src.infrastructure",
        "src.interfaces",
        "django",
        "fastapi",
        "flask",
    ]

    for file in ROOT.rglob("*.py"):
        content = read(file)

        for f in forbidden:
            assert f not in content, (
                f"[ARCH VIOLATION] Domain layer must not import {f} -> {file}"
            )