from logging import getLogger
from pathlib import Path

from appdirs import user_config_dir
from git import Repo
from git.exc import InvalidGitRepositoryError

from mailz import app_name
from mailz.exceptions import MailzException


_logger = getLogger(__name__)


class Paths:
    def __init__(self, working_dir: Path) -> None:
        self.working_dir = working_dir.resolve()
        self.templates_dir = self.git_dir / "templates"
        self.yml_templates_dir = self.templates_dir / "yml"
        self.template_user_config = self.yml_templates_dir / "user-config.yml"
        self.template_mailing_config = self.yml_templates_dir / "mailing.yml"
        self.jinja2_dir = self.templates_dir / "jinja2"
        self.user_config_dir = Path(user_config_dir(app_name))
        self.user_config = self.user_config_dir / "user-config.yml"
        self.user_config_dir.mkdir(parents=True, exist_ok=True)

    @property
    def git_dir(self) -> Path:
        if not hasattr(self, "_git_dir"):
            try:
                repository = Repo(str(self.working_dir), search_parent_directories=True)
            except InvalidGitRepositoryError as e:
                raise MailzException(
                    "Could not find the path of the current git working directory. "
                    "Are you in one?"
                ) from e
            self._git_dir = Path(repository.git.rev_parse("--show-toplevel")).resolve()
        return self._git_dir
