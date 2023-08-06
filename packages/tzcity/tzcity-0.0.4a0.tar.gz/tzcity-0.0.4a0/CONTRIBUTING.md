# Contributing

Pull requests are welcome!

Regarding data, see [DATA.md](https://github.com/ju-sh/tzcity/blob/master/DATA.md)

This package uses the following for development:

| Package         | Purpose              |
| -------         | -------              |
| pytest          | Testing              |
| vulture         | Dead code detection  |
| mypy            | Static type checking |
| pylint & flake8 | Linting              |
| coverage        | Test coverage        |
| tox             | Test automation      |
| flit            | Packaging            |

To install flit, use

    pip install flit

To install the dev dependencies, run the following from the project root directory

    flit install --symlink

## Tests (pytest)

Make sure to add tests in the tests/ directory for any new piece of code using pytest.

    pytest

## Test coverage (coverage)

Ensure proper test coverage with coverage.py

    tox -e coverage

## Static type checking (mypy)

Use type annotations for every function definition and apply mypy for static type checking.

    tox -e mypy

## Linting (pylint and flake8)

Use both pylint and flake8 for linting.

    tox -e pylint,flake8

## Dead code detection (vulture)

Vulture to check for dead code.

    tox -e vulture

## All checks

Run all checks with

    tox
