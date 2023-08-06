from logging import getLogger
from pathlib import Path

from tqdm import tqdm

from mailz.builder import Builder
from mailz.config import get_config
from mailz.paths import Paths
from mailz.sender import Sender
from mailz.target import Target


_logger = getLogger(__name__)


def run(path: Path, paths: Paths) -> None:
    config = get_config(paths)
    target = Target(path, paths)
    emails = Builder(target, config, paths).generate_emails()
    for response in tqdm(Sender(config).send(emails)):
        if 100 <= response.status_code < 200:
            status = "info"
        elif 300 <= response.status_code < 400:
            status = "redirection"
        elif 400 <= response.status_code < 500:
            status = "client error"
        elif 500 <= response.status_code < 600:
            status = "server error"
        else:
            continue
        _logger.warning("Received %s response: %s", status, response.to_dict)
