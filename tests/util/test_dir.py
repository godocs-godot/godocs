from pathlib import Path
from godocs.util import dir


def test_get_subitems_finds_files_and_folders(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "script.py"
    item2 = tmp_path / "dir"
    item3 = tmp_path / "data.json"

    item1.touch()
    item2.touch()
    item3.touch()

    # Act
    subitems = dir.get_subitems(tmp_path)

    # Assert
    assert len(subitems) == 3
    assert item1 in subitems
    assert item2 in subitems
    assert item3 in subitems


def test_get_subitems_excludes_passed_items(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "script.py"
    item2 = tmp_path / "dir"
    item3 = tmp_path / "data.json"

    item1.touch()
    item2.touch()
    item3.touch()

    # Act
    subitems = dir.get_subitems(tmp_path, exclude=["script.py"])

    # Assert
    assert len(subitems) == 2
    assert item2 in subitems
    assert item3 in subitems


def test_get_subitems_includes_passed_items(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "script.py"
    item2 = tmp_path / "dir"
    item3 = tmp_path / "data.json"

    item1.touch()
    item2.touch()
    item3.touch()

    # Act
    subitems = dir.get_subitems(tmp_path, include=["dir"])

    # Assert
    assert len(subitems) == 1
    assert item2 in subitems


def test_get_subitems_excludes_and_includes_passed_items(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "script.py"
    item2 = tmp_path / "dir"
    item3 = tmp_path / "data.json"

    item1.touch()
    item2.touch()
    item3.touch()

    # Act
    subitems = dir.get_subitems(
        tmp_path, exclude=["data.json"], include=["dir", "data.json"])

    # Assert
    assert len(subitems) == 1
    assert item2 in subitems


def test_get_subitems_filters_with_predicate(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "script.py"
    item2 = tmp_path / "dir"
    item3 = tmp_path / "data.json"

    item1.touch()
    item2.touch()
    item3.touch()

    # Act
    subitems = dir.get_subitems(
        tmp_path, predicate=lambda p: p.stem != "dir")

    # Assert
    assert len(subitems) == 2
    assert item1 in subitems
    assert item3 in subitems


def test_get_subitems_uses_all_filters(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "script.py"
    item2 = tmp_path / "dir"
    item3 = tmp_path / "data.json"

    item1.touch()
    item2.touch()
    item3.touch()

    # Act
    subitems = dir.get_subitems(
        tmp_path,
        exclude=["dir"],
        include=["script.py", "dir"],
        predicate=lambda p: p.stem != "script"
    )

    # Assert
    assert len(subitems) == 0


def test_get_subdirs_ignores_files(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "dist"
    item2 = tmp_path / "public"
    item3 = tmp_path / "src"
    item4 = tmp_path / "script.py"

    item1.mkdir()
    item2.mkdir()
    item3.mkdir()
    item4.touch()

    # Act
    subdirs = dir.get_subdirs(tmp_path)

    # Assert
    assert len(subdirs) == 3
    assert item1 in subdirs
    assert item2 in subdirs
    assert item3 in subdirs


def test_get_subdirs_excludes_passed_dirs(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "dist"
    item2 = tmp_path / "public"
    item3 = tmp_path / "src"
    item4 = tmp_path / "script.py"

    item1.mkdir()
    item2.mkdir()
    item3.mkdir()
    item4.touch()

    # Act
    subdirs = dir.get_subdirs(tmp_path, exclude=["dist"])

    # Assert
    assert len(subdirs) == 2
    assert item2 in subdirs
    assert item3 in subdirs


def test_get_subdirs_includes_passed_dirs(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "dist"
    item2 = tmp_path / "public"
    item3 = tmp_path / "src"
    item4 = tmp_path / "script.py"

    item1.mkdir()
    item2.mkdir()
    item3.mkdir()
    item4.touch()

    # Act
    subdirs = dir.get_subdirs(tmp_path, include=["public"])

    # Assert
    assert len(subdirs) == 1
    assert item2 in subdirs


def test_get_subdirs_excludes_and_includes_passed_dirs(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "dist"
    item2 = tmp_path / "public"
    item3 = tmp_path / "src"
    item4 = tmp_path / "script.py"

    item1.mkdir()
    item2.mkdir()
    item3.mkdir()
    item4.touch()

    # Act
    subitems = dir.get_subdirs(
        tmp_path, exclude=["src"], include=["public", "src"])

    # Assert
    assert len(subitems) == 1
    assert item2 in subitems


def test_get_subdirs_filters_with_predicate(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "dist"
    item2 = tmp_path / "public"
    item3 = tmp_path / "src"
    item4 = tmp_path / "script.py"

    item1.mkdir()
    item2.mkdir()
    item3.mkdir()
    item4.touch()

    # Act
    subitems = dir.get_subdirs(
        tmp_path, predicate=lambda p: p.stem != "public")

    # Assert
    assert len(subitems) == 2
    assert item1 in subitems
    assert item3 in subitems


def test_get_subdirs_uses_all_filters(tmp_path: Path):
    # Arrange
    item1 = tmp_path / "dist"
    item2 = tmp_path / "public"
    item3 = tmp_path / "src"
    item4 = tmp_path / "script.py"

    item1.mkdir()
    item2.mkdir()
    item3.mkdir()
    item4.touch()

    # Act
    subitems = dir.get_subdirs(
        tmp_path,
        exclude=["dist"],
        include=["src", "dist"],
        predicate=lambda p: p.stem != "src"
    )

    # Assert
    assert len(subitems) == 0
