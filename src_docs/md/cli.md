# Command line

The `vexy-markliff` command is a [Fire](https://github.com/google/python-fire) front end to the `VexyMarkliffCLI` class in `vexy_markliff/cli.py`. It has four commands. Each reads one file and writes one file.

```text
vexy-markliff md2xliff   INPUT_FILE OUTPUT_FILE [--source_lang=en] [--target_lang=es]
vexy-markliff html2xliff INPUT_FILE OUTPUT_FILE [--source_lang=en] [--target_lang=es]
vexy-markliff xliff2md   INPUT_FILE OUTPUT_FILE
vexy-markliff xliff2html INPUT_FILE OUTPUT_FILE
```

## Common behaviour

- Input files are read as UTF-8. Output files are written as UTF-8.
- The parent directory of `OUTPUT_FILE` is created if it does not exist. An existing output file is overwritten.
- On success the command prints nothing and exits with status `0`.
- On any failure the command exits with status `1`. A missing input file, empty input or an invalid language code produces no message at all. A parse or conversion error produces one or two log lines on standard error (from Python's `logging` fallback handler) before the exit. See [Troubleshooting](troubleshooting.md#the-cli-exits-with-status-1-and-prints-nothing).

## `md2xliff`

Convert a Markdown file to XLIFF.

| Argument or flag | Short form | Default | Meaning |
|---|---|---|---|
| `INPUT_FILE` | | required | Path to the Markdown file. |
| `OUTPUT_FILE` | | required | Path to the XLIFF file to write. |
| `--source_lang` | `-s` | `en` | Source language code. |
| `--target_lang` | `-t` | `es` | Target language code. |

Language codes must be two lowercase ASCII letters (`en`, `de`, `fr`). Codes such as `EN`, `en-US` or `pt_BR` are rejected.

```bash
vexy-markliff md2xliff README.md build/README.de.xlf -s en -t de
```

Fire also accepts the hyphenated spellings `--source-lang` and `--target-lang`.

## `html2xliff`

Convert an HTML file to XLIFF. Arguments and flags are the same as for `md2xliff`.

```bash
vexy-markliff html2xliff index.html index.xlf --source_lang=en --target_lang=fr
```

HTML fragments work as well as full documents; `lxml.html.fromstring` accepts both.

## `xliff2md`

Convert an XLIFF file produced by `md2xliff` or `html2xliff` back to text.

```bash
vexy-markliff xliff2md index.xlf index.md
```

The output is one `<p>…</p>` line per `<trans-unit>`, built from the `<source>` text. The current implementation does not emit Markdown syntax, so `xliff2md` and `xliff2html` produce the same output.

## `xliff2html`

Convert an XLIFF file back to HTML.

```bash
vexy-markliff xliff2html index.xlf index.html
```

The output has the same shape as for `xliff2md`. The text is written as-is; characters such as `&` and `<` are not re-escaped for HTML.

## Getting help

Fire generates help from the docstrings:

```bash
vexy-markliff --help
vexy-markliff md2xliff --help
```

## Exit status

| Status | Meaning |
|---|---|
| `0` | The output file was written. |
| `1` | The conversion failed. Validation failures print nothing; parse errors log to standard error. |

!!! note "Reading other XLIFF files"
    `xliff2md` and `xliff2html` look for `<trans-unit>` elements in the `urn:oasis:names:tc:xliff:document:2.1` namespace. A standard XLIFF 2.1 file that uses `<unit>` and `<segment>` yields no units, and the command writes an empty output file with status `0`. See [XLIFF output](output-format.md).
