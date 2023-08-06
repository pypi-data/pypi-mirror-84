# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailz', 'mailz.cli']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.11,<4.0.0',
 'Jinja2>=2.11.1,<3.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'coloredlogs>=14.0,<15.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'pytest>=6.1.2,<7.0.0',
 'sendgrid>=6.4.7,<7.0.0',
 'tqdm>=4.50.2,<5.0.0']

entry_points = \
{'console_scripts': ['mailz = mailz.cli:cli']}

setup_kwargs = {
    'name': 'mailz',
    'version': '0.1.0',
    'description': 'Basic mailing tool.',
    'long_description': "# `mailz`\n\n[![CI Status](https://img.shields.io/github/workflow/status/m09/mailz/CI?label=CI&style=for-the-badge)](https://github.com/m09/mailz/actions?query=workflow%3ACI)\n[![CD Status](https://img.shields.io/github/workflow/status/m09/mailz/CD?label=CD&style=for-the-badge)](https://github.com/m09/mailz/actions?query=workflow%3ACD)\n[![Test Coverage](https://img.shields.io/codecov/c/github/m09/mailz?style=for-the-badge)](https://codecov.io/gh/m09/mailz)\n[![PyPI Project](https://img.shields.io/pypi/v/mailz?style=for-the-badge)](https://pypi.org/project/mailz/)\n\nBasic mailing tool.\n\n## Installation\n\nWith `pip`:\n\n```shell\npip install mailz\n```\n\n### Shell completion installation\n\nDepending on your shell:\n\n- For Bash:\n\n    ```shell\n    _MAILZ_COMPLETE=source_bash mailz > deckz-complete.sh\n    ```\n\n- For Zsh:\n\n    ```shell\n    _MAILZ_COMPLETE=source_zsh mailz > deckz-complete.sh\n    ```\n\n- For Fish:\n\n    ```shell\n    _MAILZ_COMPLETE=source_fish mailz > deckz-complete.sh\n    ```\n\nAnd then source/activate the resulting file in your shell config.\n\n## Directory Structure\n\n`mailz` works with assumptions on the directory structure of your mailing directory. Among those assumptions:\n\n- your directory should be a git repository\n- it should contain jinja2 mail templates in the `templates/jinja2` directory\n- it should contain YAML templates in the `templates/yml` directory, with specific names (listed below)\n- a config file should exist in the mailz config dir (depends on platform, on GNU/Linux it'll commonly be `$HOME/.config/mailz`), containing your sendgrid credentials and sending email\n\n```text\nroot (git repository)\n├── templates\n│\xa0\xa0 ├── jinja2\n│   │   ├── signup.txt\n│   │   └── event.txt\n│\xa0\xa0 └── yml\n│       ├── mailing-config.yml\n│       └── user-config.yml\n└── mailing-signup-september.yml\n```\n\n## Usage\n\nSee the `--help` flag of the `mailz` command line tool.\n",
    'author': 'm09',
    'author_email': '142691+m09@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m09/mailz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
