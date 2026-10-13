# Contributing

## Prerequisites

- Python 3.10 or newer.
- [`uv`](https://docs.astral.sh/uv/).
- Git, with tags fetched (`git fetch --tags`), because the version is derived from tags.

## Set up a development environment

1. Clone the repository and enter it:

    ```bash
    git clone https://github.com/vexyart/vexy-markliff.git
    cd vexy-markliff
    ```

2. Install the package in editable mode with the development and test extras:

    ```bash
    uv pip install -e ".[dev,test]"
    ```

    The `dev` extra installs `pre-commit`, `ruff`, `mypy`, `absolufy-imports`, `pyupgrade` and `isort`. The `test` extra installs `pytest`, `pytest-cov` and `coverage`.

3. Optionally install the Git hooks defined in `.pre-commit-config.yaml` (whitespace and YAML/TOML checks, `ruff`, `ruff-format`, `mypy`):

    ```bash
    pre-commit install
    ```

## Run the tests

The test suite is in `tests/` and runs in well under a second.

```bash
uv run --with pytest pytest -q
```

Or through the Hatch environment defined in `pyproject.toml`:

```bash
uvx hatch run test
uvx hatch run test-cov
```

`test-cov` prints a coverage report for `src/vexy_markliff` and `tests`.

## Lint and format

```bash
uvx hatch run lint     # ruff check + ruff format
uvx hatch run fix      # ruff check --fix --unsafe-fixes + ruff format
uvx hatch run type-check
```

## Build

The root `build.sh` builds the documentation, the package, or both:

```bash
./build.sh            # docs and package
./build.sh docs       # src_docs/md → docs/ with ProperDocs
./build.sh package    # uv build into dist/, then twine check
```

## Write documentation

The documentation source is in `src_docs/md/`; the configuration is `src_docs/mkdocs.yml`. `docs/` holds the generated site that GitHub Pages serves, so do not edit it by hand.

1. Edit or add Markdown files in `src_docs/md/`. Add new pages to the `nav` list in `src_docs/mkdocs.yml`.
2. Preview the site:

    ```bash
    src_docs/build.sh serve
    ```

    The site is served at `http://127.0.0.1:8000`.

3. Build it in strict mode, which fails on any warning such as a broken link:

    ```bash
    src_docs/build.sh
    ```

The `Docs` GitHub workflow runs the same build on every push to `main` that touches `src_docs/` and commits the result to `docs/`.

## Release

Releases are tagged `vX.Y.Z`. `publish.sh` runs `gitnextver` to commit and tag the next version, builds the package from that tag and uploads it with `uv publish`. It needs a PyPI token in `UV_PUBLISH_TOKEN`.

The `Release` workflow also builds and uploads to PyPI when a `v*` tag is pushed. It sets `skip-existing: true`, so it does not fail when `publish.sh` already uploaded the same version.

## Guidelines

- Keep the code small. The 1.3 release removed most of the earlier code base; new features should come with tests and a clear user need.
- Every source file carries a `this_file` comment with its path relative to the repository root.
- Check behaviour against the [design notes](design/index.md) when you extend the converter, and update them if the design changes.
