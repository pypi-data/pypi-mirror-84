from collections import OrderedDict
from logging import getLogger
from pathlib import Path
from shutil import copy as shutil_copy
from typing import Any, Dict

from yaml import safe_load as yaml_safe_load

from mailz.exceptions import MailzException
from mailz.paths import Paths


_logger = getLogger(__name__)


def get_config(paths: Paths) -> Dict[str, Any]:
    return OrderedDict(
        (k, v)
        for k, v in sorted(
            _get_or_create_config(paths.user_config, paths.template_user_config).items()
        )
    )


def _get_or_create_config(path: Path, template_path: Path) -> Dict[str, Any]:
    if not path.is_file():
        if template_path.is_file():
            shutil_copy(str(template_path), str(path), follow_symlinks=True)
            raise MailzException(
                f"{path} was not found, copied {template_path} there. Please edit "
                "it."
            )
        else:
            raise MailzException(
                f"Neither {path} nor {template_path} were found. " "Please create both."
            )
    with open(path, "r", encoding="utf8") as fh:
        return yaml_safe_load(fh)
