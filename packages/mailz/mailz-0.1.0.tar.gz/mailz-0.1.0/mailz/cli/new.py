from logging import getLogger
from pathlib import Path

from mailz.cli import command, dir_path_option
from mailz.paths import Paths


_logger = getLogger(__name__)


@command
@dir_path_option
def new(dir_path: str) -> None:
    """Create a new mailing config."""
    Paths(Path(dir_path))
