@_:
    just --list

test *args:
    DJANGO_SETTINGS_MODULE=tests.test_project.settings uv run {{ args }} -m django test tests

lint *args:
    uvx ruff check {{ args }}
