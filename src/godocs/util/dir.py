from os import PathLike
from pathlib import Path


def get_subdirs(
    path: str | PathLike[str],
    exclude: list[str] | None = None,
    include: list[str] | None = None,
) -> list[Path]:
    """
    Returns a `list` with the `Paths` of the subdirectories of
    the `path` passed, excluding the ones from the `exclude`
    list and including only the ones from the `include` list
    (if any).
    """

    if exclude is None:
        exclude = []
    if include is None:
        include = []

    path = Path(path)

    subdirs: list[Path] = []

    for p in path.iterdir():
        if not p.is_dir():
            continue
        if p.name in exclude:
            continue
        if not p.name in include:
            continue

        subdirs.append(p)

    return subdirs
