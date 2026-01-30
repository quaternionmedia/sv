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

    monkeypatch.setattr(tutorial, "_VERSION_PATH", version_path)
    new_version = tutorial.bump_tutorial_version(is_dev=True)

    assert new_version == "1.2.3.dev5"
    assert version_path.read_text(encoding="utf-8") == "1.2.3.dev5\n"
