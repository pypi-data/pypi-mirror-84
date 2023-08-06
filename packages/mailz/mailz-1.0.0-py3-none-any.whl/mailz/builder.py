from collections.abc import Mapping as ABCMapping, Sequence as ABCSequence
from logging import getLogger
from os.path import join as path_join
from typing import Any, Dict, Iterator, Tuple

from jinja2 import Environment, FileSystemLoader
from yaml import safe_load as yaml_safe_load

from mailz.exceptions import MailzException
from mailz.mail import Mail
from mailz.paths import Paths
from mailz.target import Target


class Builder:
    def __init__(self, target: Target, config: Dict[str, Any], paths: Paths):
        self._target = target
        self._config = config
        self._paths = paths
        self._logger = getLogger(__name__)

    def generate_emails(self) -> Iterator[Mail]:
        broadcast_config = self._target.config.pop("broadcast", {})
        iterated_config = self._target.config.pop("iterated", {})
        if isinstance(iterated_config, ABCMapping):
            iterated_config = [
                dict(zip(iterated_config, t)) for t in zip(*iterated_config.values())
            ]
        elif not isinstance(iterated_config, ABCSequence):
            raise MailzException("iterated section was neither a mapping nor a listing")
        for item_config in iterated_config:
            to_add = {}
            to_add.update(broadcast_config)
            to_add.update(item_config)
            unrendered_config, to_render_config = self._split_config(to_add)
            rendered_config = self._render(to_render_config)
            yield Mail(**unrendered_config, **rendered_config)  # type: ignore

    def _render(self, template_params: Dict[str, Any]) -> Dict[str, Any]:
        template = self._env.get_template(
            str(self._target.template_path.relative_to(self._paths.jinja2_dir))
        )
        return yaml_safe_load(template.render(template_params))

    @property
    def _env(self) -> Environment:
        if not hasattr(self, "__env"):
            self.__env = Environment(
                loader=FileSystemLoader(searchpath=self._paths.jinja2_dir),
                trim_blocks=True,
                autoescape=False,
            )
            self.__env.filters["path_join"] = lambda paths: path_join(*paths)
        return self.__env

    @staticmethod
    def _split_config(config: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        unrendered_config = dict(
            to=config.pop("to"),
            cc=config.pop("cc", []),
            bcc=config.pop("bcc", []),
            headers=config.pop("headers", {}),
        )
        return unrendered_config, config
