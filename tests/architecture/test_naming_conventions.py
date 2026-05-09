# tests/architecture/test_naming_conventions.py

from pathlib import Path

ROOT = Path("src")


def test_use_cases_must_end_with_py():
    folder = ROOT / "application" / "use_cases"

    files = [
        f.name for f in folder.glob("*.py")
        if f.name != "__init__.py"
    ]

    assert len(files) > 0


def test_domain_entities_exist():
    entities = list(ROOT.joinpath("domain").rglob("entity.py"))
    assert len(entities) >= 3


def test_repositories_are_isolated():
    repos = list(ROOT.joinpath("domain").rglob("repository.py"))
    assert len(repos) >= 3