# tests/architecture/test_clean_imports.py

from pathlib import Path

ROOT = Path("src")


def python_files():
    return [
        p for p in ROOT.rglob("*.py")
        if "__pycache__" not in str(p)
    ]


def read(file):
    return file.read_text()


def test_domain_must_not_import_django():
    for file in ROOT.joinpath("domain").rglob("*.py"):
        content = read(file)
        assert "django." not in content
        assert "from django" not in content


def test_domain_must_not_import_application():
    for file in ROOT.joinpath("domain").rglob("*.py"):
        content = read(file)
        assert "src.application" not in content


def test_domain_must_not_import_infrastructure():
    for file in ROOT.joinpath("domain").rglob("*.py"):
        content = read(file)
        assert "src.infrastructure" not in content


def test_application_must_not_import_django():
    for file in ROOT.joinpath("application").rglob("*.py"):
        content = read(file)
        assert "django." not in content
        assert "from django" not in content
