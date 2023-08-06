[![Build Status](https://travis-ci.org/danie1k/python-black-configparser.svg?branch=master)](https://travis-ci.org/danie1k/python-black-configparser)
[![Code Coverage](https://codecov.io/gh/danie1k/python-black-configparser/branch/master/graph/badge.svg?token=A496BD37Qj)](https://codecov.io/gh/danie1k/python-black-configparser)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/black-configparser)](https://pypi.org/project/black-configparser/)
[![PyPI](https://img.shields.io/pypi/v/black-configparser)](https://pypi.org/project/black-configparser/)
[![MIT License](https://img.shields.io/github/license/danie1k/python-black-configparser)](https://github.com/danie1k/python-black-configparser/blob/master/LICENSE)
[![Automatic PyPI Release](https://github.com/danie1k/python-black-configparser/workflows/PyPi%20Release/badge.svg)](https://github.com/danie1k/python-black-configparser/actions)

# black-configparser

Seamless proxy CLI for [black](https://pypi.org/project/black/) *("The uncompromising code formatter")*
with support for non-`pyproject.toml` config files.


## Table of Contents

1. [About the Project](#about-the-project)
    - [Why it is different?](#why-it-is-different)
1. [Installation](#installation)
1. [Usage](#usage)
    - [Example configuration](#)
1. [Known issues](#known-issues)
1. [License](#license)


## About the Project

The `black-configparser` is yet another tool *(next to [brunette](https://pypi.org/project/brunette/),
[white](https://pypi.org/project/white/), and maybe a few more out there)*,
which tries to fill [the gap of missing `setup.cfg`](https://github.com/psf/black/issues/688)
(or just [any other non-`pyproject.toml`](https://github.com/psf/black/issues/683)) config file.


### Why it is different?

Unlike other tools, tries to stay **dumb simple** and add only minimum needed overhead to `black` usage.

1. It is **seamless** - it works on the same CLI command - `black` - just passing logic through some extra code!
1. There is no complex argument processing, if config file is present, the values set there are passed directly to `black`.
1. Code of this tool is independent from `black` insides and will work properly
   as long as `black` won't make any braking changes in its command line options.


## Installation

```
$ pip install black-configparser
```


## Usage

- Supported configuration files: `setup.cfg`, `tox.ini`.
- Configuration file section: `[black]` or `[tools:black]`.

**Important!** :warning:  
- When you `black-configparser` finds black configuration in any of supported file(s),
    most black's built-in command line arguments become unavailable.  
    Exceptions:
    - `--check`
    - `--code`
    - `--diff`
    - `--help`
    - `--verbose`
    - `--version`
- The `black-configparser` can be temporarily disabled, by adding `--no-config-file` flag to `black` command,
    for example:
    ```
    $ black --no-config-file --check ./path/to/file.py
    ```

### Example configuration

```ini
[black]
line-length = 120
target-version =
  py27
  py33
  py34
  py35
  py36
  py37
  py38
pyi = True
skip-string-normalization = True
color = True
include = \.pyi?$
exclude = /(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist)/
force-exclude = lorem ipsum
quiet = True
verbose = True
```

- Almost any option available for black (`black --help`) can be put onto config file.
- Values for multi-value arguments must be one per line (separated by `\n` char).
- Flags *(arguments without values)* must be set in config file as `= True`.


## Known issues

- Undefined behavior, when running with one of allowed CLI arguments which is also set in the config file.
- After `black-configparser` package is uninstalled, the `black` command does not work anymore
    and [black](https://pypi.org/project/black/) package must be reinstalled.


## License

MIT
