# tests/architecture/enforcement/test_dto_isolation.py

from pathlib import Path

ROOT = Path("src/application/use_cases/dto")


def read(file: Path) -> str:
    return file.read_text()


def test_dto_are_framework_free():
    forbidden = [
        "django",
        "pydantic.BaseModel",
        "sqlalchemy",
        "src.infrastructure",
        "src.interfaces",
    ]

    for file in ROOT.rglob("*.py"):
        content = read(file)

        for f in forbidden:
            assert f not in content, (
                f"[ARCH VIOLATION] DTO must be framework-free -> {file}"
            )