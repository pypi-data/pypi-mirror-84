from pathlib import Path
from typing import Any, List

from click import argument, Path as ClickPath

from mailz.cli import command, dir_path_option
from mailz.paths import Paths
from mailz.runner import run as runner_run


def _autocomplete_path(ctx: Any, args: List[str], incomplete: str) -> List[str]:
    try:
        paths = Paths(Path("."))
        return [t.name for t in paths.working_dir.glob("*.yml")]
    except Exception:
        return []


@command
@argument(
    "path",
    type=ClickPath(exists=True, dir_okay=False, readable=True),
    autocompletion=_autocomplete_path,  # type: ignore
)
@dir_path_option
def run(path: str, dir_path: str) -> None:
    """Run the compiler."""
    paths = Paths(Path(dir_path))
    runner_run(Path(path), paths)
