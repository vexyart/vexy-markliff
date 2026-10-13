# Installation

## Requirements

- Python 3.10 or newer.
- The runtime dependencies are installed automatically: `fire`, `lxml`, `markdown-it-py`, `pydantic`, `pyyaml` and `rich`.

`lxml` ships binary wheels for the common platforms. If your platform has no wheel, `pip` compiles it and needs the `libxml2` and `libxslt` development headers.

## Install from PyPI

The PyPI package name is `vexy-markliff`; the import name is `vexy_markliff`.

=== "uv"

    ```bash
    uv pip install vexy-markliff
    ```

=== "uv project"

    ```bash
    uv add vexy-markliff
    ```

=== "pip"

    ```bash
    python -m pip install vexy-markliff
    ```

To run the CLI once without installing it into an environment:

```bash
uvx vexy-markliff --help
```

## Install from source

1. Clone the repository:

    ```bash
    git clone https://github.com/vexyart/vexy-markliff.git
    cd vexy-markliff
    ```

2. Install the package in editable mode with the test extras:

    ```bash
    uv pip install -e ".[test]"
    ```

The version number comes from the latest Git tag through `hatch-vcs`. A commit after the `v1.3.1` tag builds as a development version such as `1.3.2.dev0+g1831c684d`; a tagged commit builds as the plain tag version.

## Check the installation

1. Print the package version:

    ```bash
    python -c "import vexy_markliff; print(vexy_markliff.__version__)"
    ```

    If the version file has not been generated (for example, when you run from a source tree that was never built or installed), this prints `unknown`.

2. List the CLI commands:

    ```bash
    vexy-markliff --help
    ```

    Fire prints the command group with `md2xliff`, `html2xliff`, `xliff2md` and `xliff2html`.

## Uninstall

```bash
uv pip uninstall vexy-markliff
```
