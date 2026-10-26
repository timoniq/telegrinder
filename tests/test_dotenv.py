import pathlib
import sys

import pytest

from telegrinder import modules


@pytest.fixture(autouse=True)
def dotenv_settings(monkeypatch):
    monkeypatch.setattr(modules, "_ENV_FILE_NAME", ".env")
    monkeypatch.setattr(modules, "_ENV_FILE_PATH", None)
    monkeypatch.setattr(modules, "_LOAD_ENV_FILE", False)
    monkeypatch.setattr(modules, "DOTENV", modules._DotenvProvider())


def create_file(path: pathlib.Path, content: str = "") -> pathlib.Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


@pytest.mark.parametrize("venv_location", [".venv", "outside"])
def test_find_env_file_starts_at_working_directory(tmp_path, monkeypatch, venv_location):
    project = tmp_path / "project"
    expected = create_file(project / ".env")
    create_file(project / "pyproject.toml")
    venv = project / ".venv" if venv_location == ".venv" else tmp_path / "external-venv"
    create_file(venv / "pyvenv.cfg")
    create_file(venv / ".env")
    script_dir = tmp_path / "scripts"
    create_file(script_dir / ".env")
    monkeypatch.setattr(sys, "prefix", str(venv))
    monkeypatch.setattr(sys, "path", [str(script_dir), *sys.path[1:]])
    monkeypatch.chdir(project)

    assert modules._find_env_file().unwrap() == expected


@pytest.mark.parametrize("marker", ["pyproject.toml", ".git", ".venv"])
def test_find_env_file_finds_project_root_from_nested_launch(tmp_path, monkeypatch, marker):
    project = tmp_path / "project"
    expected = create_file(project / ".env")
    if marker == ".venv":
        (project / marker).mkdir()
    else:
        create_file(project / marker)
    launch_dir = project / "src" / "bot"
    launch_dir.mkdir(parents=True)
    monkeypatch.chdir(launch_dir)

    assert modules._find_env_file().unwrap() == expected


@pytest.mark.parametrize("env_location", ["src", "src/bot"])
def test_find_env_file_prefers_nearest_ancestor(tmp_path, monkeypatch, env_location):
    project = tmp_path / "project"
    create_file(project / "pyproject.toml")
    create_file(project / ".env", "ROOT=true")
    expected = create_file(project / env_location / ".env")
    launch_dir = project / "src" / "bot"
    launch_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(launch_dir)

    assert modules._find_env_file().unwrap() == expected


@pytest.mark.parametrize("marked_project", [False, True])
def test_find_env_file_searches_project_subdirectories(tmp_path, monkeypatch, marked_project):
    project = tmp_path / "project"
    expected = create_file(project / "config" / ".env")
    if marked_project:
        create_file(project / "pyproject.toml")
        launch_dir = project / "src" / "bot"
        launch_dir.mkdir(parents=True)
    else:
        launch_dir = project
    monkeypatch.chdir(launch_dir)

    assert modules._find_env_file().unwrap() == expected


@pytest.mark.parametrize("marked_project", [False, True])
def test_find_env_file_does_not_escape_project(tmp_path, monkeypatch, marked_project):
    create_file(tmp_path / ".env", "OUTSIDE=true")
    create_file(tmp_path / "other-project" / ".env", "OTHER=true")
    project = tmp_path / "project"
    project.mkdir()
    if marked_project:
        create_file(project / "pyproject.toml")
    monkeypatch.chdir(project)

    assert modules._find_env_file().unwrap_or_none() is None


@pytest.mark.parametrize("excluded", [".git", ".venv", "custom-venv", "nested-project"])
def test_find_env_file_skips_environments_and_nested_projects(tmp_path, monkeypatch, excluded):
    project = tmp_path / "project"
    create_file(project / "pyproject.toml")
    create_file(project / excluded / ".env", "WRONG=true")
    if excluded in {".venv", "custom-venv"}:
        create_file(project / excluded / "pyvenv.cfg")
    elif excluded == "nested-project":
        create_file(project / excluded / "pyproject.toml")
    monkeypatch.chdir(project)

    assert modules._find_env_file().unwrap_or_none() is None


@pytest.mark.parametrize("order", [("z", "a"), ("a", "z")])
def test_find_env_file_recursive_order_is_deterministic(tmp_path, monkeypatch, order):
    project = tmp_path / "project"
    create_file(project / "pyproject.toml")
    for directory in order:
        create_file(project / directory / ".env", f"DIR={directory}")
    monkeypatch.chdir(project)

    assert modules._find_env_file().unwrap() == project / "a" / ".env"


def test_find_env_file_uses_configured_name(tmp_path, monkeypatch):
    create_file(tmp_path / ".env", "WRONG=true")
    expected = create_file(tmp_path / "config" / ".env.local")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(modules, "_ENV_FILE_NAME", ".env.local")

    assert modules._find_env_file().unwrap() == expected


def test_find_env_file_ignores_directories_named_env(tmp_path, monkeypatch):
    (tmp_path / ".env").mkdir()
    expected = create_file(tmp_path / "config" / ".env")
    monkeypatch.chdir(tmp_path)

    assert modules._find_env_file().unwrap() == expected


@pytest.mark.parametrize("explicit_path", [False, True])
def test_take_env_loads_selected_file(tmp_path, monkeypatch, explicit_path):
    project = tmp_path / "project"
    create_file(project / "pyproject.toml")
    create_file(project / ".env", "TELEGRINDER_DOTENV_TEST=project")
    explicit = create_file(tmp_path / "explicit.env", "TELEGRINDER_DOTENV_TEST=explicit")
    monkeypatch.chdir(project)
    monkeypatch.setenv("TELEGRINDER_DOTENV_TEST", "before")
    modules.configure_dotenv(file_path=explicit if explicit_path else None)

    assert modules.take_env("TELEGRINDER_DOTENV_TEST") == ("explicit" if explicit_path else "project")
