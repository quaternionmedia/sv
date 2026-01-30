import pytest
import semver as semver_module


def test_parse_accepts_dev_suffixes() -> None:
    semver_logic = semver_module.get_semver_logic()
    semver_logic.parse("1.2.3.dev4")
    semver_logic.parse("1.2.3-dev.4")


def test_parse_accepts_prerelease_and_build() -> None:
    semver_logic = semver_module.get_semver_logic()
    semver_logic.parse("1.2.3-alpha.1")
    semver_logic.parse("1.2.3+build.7")
    semver_logic.parse("1.2.3-alpha.1+build.7")


def test_bump_strips_dev_suffix() -> None:
    semver_logic = semver_module.get_semver_logic()
    assert semver_logic.bump("1.2.3.dev4", "patch") == "1.2.4"


def test_bump_drops_prerelease_and_build() -> None:
    semver_logic = semver_module.get_semver_logic()
    assert semver_logic.bump("1.2.3-alpha.1", "patch") == "1.2.4"
    assert semver_logic.bump("1.2.3+build.7", "minor") == "1.3.0"


def test_bump_with_dev_increment() -> None:
    semver_logic = semver_module.get_semver_logic()
    result = semver_logic.bump_with_dev("1.2.3.dev4", "dev", is_dev=True)

    assert result.base_version == "1.2.3"
    assert result.new_version == "1.2.3.dev5"
    assert result.npm_version == "1.2.3-dev.5"
    assert result.mod_version == "1.2.3"


def test_bump_with_dev_from_release() -> None:
    semver_logic = semver_module.get_semver_logic()
    result = semver_logic.bump_with_dev("1.2.3", "dev", is_dev=True)

    assert result.new_version == "1.2.3.dev0"


def test_bump_with_dev_release_bump_dev_flag() -> None:
    semver_logic = semver_module.get_semver_logic()
    result = semver_logic.bump_with_dev("1.2.3.dev4", "minor", is_dev=True)

    assert result.new_version == "1.3.0.dev0"


def test_bump_with_dev_is_dev_false_drops_suffix() -> None:
    semver_logic = semver_module.get_semver_logic()
    result = semver_logic.bump_with_dev("1.2.3.dev4", "none", is_dev=False)

    assert result.new_version == "1.2.3"


def test_bump_with_dev_accepts_npm_suffix() -> None:
    semver_logic = semver_module.get_semver_logic()
    result = semver_logic.bump_with_dev("1.2.3-dev.4", "dev", is_dev=True)

    assert result.new_version == "1.2.3.dev5"


def test_bump_with_dev_drops_prerelease_and_build() -> None:
    semver_logic = semver_module.get_semver_logic()
    result = semver_logic.bump_with_dev("1.2.3-alpha.1+build.7", "dev", is_dev=True)

    assert result.base_version == "1.2.3"
    assert result.new_version == "1.2.3.dev0"


@pytest.mark.parametrize(
    "version",
    [
        "1.2",
        "1.2.3.4",
        "01.2.3",
        "1.02.3",
        "1.2.03",
        "1.2.3-",
        "1.2.3+",
        "1.2.3-rc..1",
        "1.2.3+build..1",
        "1.2.3.dev",
        "1.2.3.devx",
        "1.2.3-dev.x",
    ],
)
def test_parse_rejects_invalid_versions(version: str) -> None:
    semver_logic = semver_module.get_semver_logic()
    with pytest.raises(ValueError):
        semver_logic.parse(version)


@pytest.mark.parametrize(
    "version",
    [
        "1.2",
        "1.2.3-",
        "1.2.3+",
        "1.2.3.devx",
        "1.2.3-dev.x",
    ],
)
def test_bump_rejects_invalid_versions(version: str) -> None:
    semver_logic = semver_module.get_semver_logic()
    with pytest.raises(ValueError):
        semver_logic.bump(version, "patch")
