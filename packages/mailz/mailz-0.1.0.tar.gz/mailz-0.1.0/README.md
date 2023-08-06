# `mailz`

[![CI Status](https://img.shields.io/github/workflow/status/m09/mailz/CI?label=CI&style=for-the-badge)](https://github.com/m09/mailz/actions?query=workflow%3ACI)
[![CD Status](https://img.shields.io/github/workflow/status/m09/mailz/CD?label=CD&style=for-the-badge)](https://github.com/m09/mailz/actions?query=workflow%3ACD)
[![Test Coverage](https://img.shields.io/codecov/c/github/m09/mailz?style=for-the-badge)](https://codecov.io/gh/m09/mailz)
[![PyPI Project](https://img.shields.io/pypi/v/mailz?style=for-the-badge)](https://pypi.org/project/mailz/)

Basic mailing tool.

## Installation

With `pip`:

```shell
pip install mailz
```

### Shell completion installation

Depending on your shell:

- For Bash:

    ```shell
    _MAILZ_COMPLETE=source_bash mailz > deckz-complete.sh
    ```

- For Zsh:

    ```shell
    _MAILZ_COMPLETE=source_zsh mailz > deckz-complete.sh
    ```

- For Fish:

    ```shell
    _MAILZ_COMPLETE=source_fish mailz > deckz-complete.sh
    ```

And then source/activate the resulting file in your shell config.

## Directory Structure

`mailz` works with assumptions on the directory structure of your mailing directory. Among those assumptions:

- your directory should be a git repository
- it should contain jinja2 mail templates in the `templates/jinja2` directory
- it should contain YAML templates in the `templates/yml` directory, with specific names (listed below)
- a config file should exist in the mailz config dir (depends on platform, on GNU/Linux it'll commonly be `$HOME/.config/mailz`), containing your sendgrid credentials and sending email

```text
root (git repository)
├── templates
│   ├── jinja2
│   │   ├── signup.txt
│   │   └── event.txt
│   └── yml
│       ├── mailing-config.yml
│       └── user-config.yml
└── mailing-signup-september.yml
```

## Usage

See the `--help` flag of the `mailz` command line tool.
