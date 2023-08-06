from logging import getLogger
from pathlib import Path

from yaml import safe_load as yaml_safe_load

from mailz.exceptions import MailzException
from mailz.paths import Paths


_logger = getLogger(__name__)


class Target:
    def __init__(self, path: Path, paths: Paths):
        if not path.is_file():
            raise MailzException(f"Could not find the mailing config {path}.")
        with path.open(encoding="utf8") as fh:
            self.config = yaml_safe_load(fh)
        self.template_name = self.config.pop("template_name")
        self.template_path = paths.jinja2_dir / self.template_name
        if not self.template_path.is_file():
            raise MailzException(
                f"Could not find the template to use {self.template_path}."
            )
