# tests/architecture/test_layer_dependencies.py

from pathlib import Path

ROOT = Path("src")


def read(file):
    return file.read_text()


def test_interfaces_must_not_import_django_models():
    for file in ROOT.joinpath("interfaces").rglob("*.py"):
        content = read(file)

        assert ".models" not in content
        assert "django.db" not in content


def test_interfaces_should_not_import_repositories():
    for file in ROOT.joinpath("interfaces").rglob("*.py"):
        content = read(file)

        assert "repositories" not in content


def test_infrastructure_must_not_import_interfaces():
    for file in ROOT.joinpath("infrastructure").rglob("*.py"):
        content = read(file)

        assert "src.interfaces" not in content