from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from sv import tutorial


def test_bump_tutorial_version_updates_version_file(tmp_path: Path, monkeypatch) -> None:
    version_path = tmp_path / "VERSION"
    version_path.write_text("1.2.3.dev4\n", encoding="utf-8")

    new_version = tutorial.bump_tutorial_version(is_dev=True, version_path=version_path)

    assert new_version == "1.2.3.dev5"
    assert version_path.read_text(encoding="utf-8") == "1.2.3.dev5\n"


def test_bump_tutorial_version_release_bump(tmp_path: Path) -> None:
    version_path = tmp_path / "VERSION"
    version_path.write_text("1.2.3.dev4\n", encoding="utf-8")

    new_version = tutorial.bump_tutorial_version(
        bump_type="minor",
        is_dev=False,
        version_path=version_path,
    )

    assert new_version == "1.3.0"
    assert version_path.read_text(encoding="utf-8") == "1.3.0\n"


def test_set_version_writes_explicit_value(tmp_path: Path) -> None:
    version_path = tmp_path / "VERSION"
    version_path.write_text("0.1.0.dev0\n", encoding="utf-8")

    tutorial.get_semver_logic().parse("2.0.0")
    version_path.write_text("2.0.0\n", encoding="utf-8")

    assert version_path.read_text(encoding="utf-8") == "2.0.0\n"
