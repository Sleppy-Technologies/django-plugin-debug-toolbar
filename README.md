# django-plugin-debug-toolbar

[![PyPI](https://img.shields.io/pypi/v/django-plugin-debug-toolbar.svg)](https://pypi.org/project/django-plugin-debug-toolbar/)
[![Changelog](https://img.shields.io/github/v/release/Sleppy-Technologies/django-plugin-debug-toolbar?include_prereleases&label=changelog)](https://github.com/Sleppy-Technologies/django-plugin-debug-toolbar/releases)
[![Tests](https://github.com/Sleppy-Technologies/django-plugin-debug-toolbar/workflows/Test/badge.svg)](https://github.com/Sleppy-Technologies/django-plugin-debug-toolbar/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Sleppy-Technologies/django-plugin-debug-toolbar/blob/main/LICENSE)

Django plugin wrapping django-debug-toolbar

## Installation

First configure your Django project [to use DJP](https://djp.readthedocs.io/en/latest/installing_plugins.html).

Then install this plugin in the same environment as your Django application.

```bash
pip install django-plugin-debug-toolbar
```

## Usage

The toolbar will only display when `DEBUG = True`.

No further configuration is needed, refer to [`django-debug-toolbar` documentation](https://django-debug-toolbar.readthedocs.io/en/latest/index.html) to learn about your new capabilities.

## Development

Install `uv` following [`uv`'s install documentation](https://docs.astral.sh/uv/getting-started/installation/). Install [`just`](https://just.systems/man/en/introduction.html) with `uv tool install rust-just`.

### Testing

`just test`

### Linting

`just lint`
