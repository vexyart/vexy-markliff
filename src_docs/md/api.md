# Python API

The package exposes a small API. Everything on this page exists in `src/vexy_markliff/` in version 1.3.

## Top-level names

`vexy_markliff.__all__` lists:

| Name | Kind | Defined in |
|---|---|---|
| `VexyMarkliff` | class | `vexy_markliff/__init__.py` (lazy wrapper) |
| `ConversionConfig` | class | `vexy_markliff/config.py` (lazy import) |
| `VexyMarkliffCLI` | class | `vexy_markliff/cli.py` (lazy import) |
| `__version__` | string | `vexy_markliff/__version__.py`, generated at build time |

`ConversionConfig` and `VexyMarkliffCLI` are imported on first access through a module-level `__getattr__`, so `import vexy_markliff` stays fast. If `__version__.py` is missing, `__version__` is `"unknown"`.

## `VexyMarkliff`

```python
from vexy_markliff import VexyMarkliff

converter = VexyMarkliff(config=None)
```

The top-level `VexyMarkliff` is a thin wrapper. On the first method call it imports `vexy_markliff.core.converter.VexyMarkliff` and forwards every call to it. Any attribute that the wrapper does not define is also forwarded.

The `config` argument is stored and passed to the core converter, which keeps it as `self.config`. The 1.3 converter does not read any value from it; language codes come from the method arguments.

### `markdown_to_xliff(content, source_lang="en", target_lang="es") -> str`

Render `content` (a Markdown string) to HTML, extract text nodes and return an XLIFF document as a string.

### `html_to_xliff(content, source_lang="en", target_lang="es") -> str`

Parse `content` (an HTML string or fragment), extract text nodes and return an XLIFF document as a string.

Both `*_to_xliff` methods:

1. Raise `ValidationError("Content cannot be empty")` if `content` is empty or whitespace only.
2. Raise `ValidationError` if `source_lang` or `target_lang` is not two lowercase ASCII letters.
3. Wrap any other failure in `ConversionError`, with the original message appended.

### `xliff_to_markdown(xliff_content) -> str`

### `xliff_to_html(xliff_content) -> str`

Parse an XLIFF string with `XLIFFDocument.from_xml` and return one `<p>…</p>` line per unit, joined with newlines. Both methods return the same text. They raise `ValidationError("XLIFF content cannot be empty")` for empty input and wrap other failures in `ConversionError`.

```python
from vexy_markliff import VexyMarkliff
from vexy_markliff.exceptions import ConversionError, ValidationError

converter = VexyMarkliff()
try:
    xliff = converter.html_to_xliff("<h1>Title</h1><p>Body</p>", "en", "de")
except ValidationError as error:
    print(f"Bad input: {error}")
except ConversionError as error:
    print(f"Conversion failed: {error}")
else:
    print(converter.xliff_to_html(xliff))
```

Output:

```html
<p>Title</p>
<p>Body</p>
```

## `ConversionConfig`

```python
from vexy_markliff import ConversionConfig

config = ConversionConfig(source_language="en", target_language="es", split_sentences=True)
```

A plain class (not a Pydantic model) with three attributes:

| Attribute | Default | Validation |
|---|---|---|
| `source_language` | `"en"` | Two lowercase letters, else `ValueError` |
| `target_language` | `"es"` | Two lowercase letters, else `ValueError` |
| `split_sentences` | `True` | None |

`ConversionConfig.load(config_path=None)` reads a YAML file and passes its top-level keys to the constructor:

```yaml
source_language: en
target_language: de
split_sentences: false
```

If `config_path` is `None`, the file does not exist, or loading fails for any reason (bad YAML, unknown key, invalid code), `load` returns a default `ConversionConfig()` without raising.

!!! note
    The converter accepts a `ConversionConfig` but does not use it in version 1.3. The CLI has no option to load a configuration file.

## Exceptions

All exceptions live in `vexy_markliff.exceptions` and derive from `VexyMarkliffError`, which derives from `Exception`.

| Exception | Raised by the 1.3 code |
|---|---|
| `VexyMarkliffError` | Base class only |
| `ValidationError` | Empty content, invalid language code, malformed XLIFF in `XLIFFDocument.from_xml`, serialization failure in `to_xml` |
| `ConversionError` | Any failure inside a converter method, wrapping the original error |
| `ParsingError` | `MarkdownParser` and `HTMLParser` failures |
| `FileOperationError` | Defined, not raised |
| `ConfigurationError` | Defined, not raised |

A `ParsingError` raised inside a converter method reaches the caller as a `ConversionError`.

## Parsers

`vexy_markliff.core` exports `MarkdownParser`, `HTMLParser` and the core `VexyMarkliff`.

### `HTMLParser`

`HTMLParser().parse(content)` returns a dictionary:

```python
from vexy_markliff.core import HTMLParser

HTMLParser().parse('<html><head><title>Hi</title></head><body><p class="x">A <b>B</b> C</p></body></html>')
```

```python
{
    "segments": [
        {"content": "Hi", "translatable": True, "element": "title"},
        {"content": "A", "translatable": True, "element": "p"},
        {"content": "B", "translatable": True, "element": "b"},
        {"content": "C", "translatable": True, "element": "text"},
    ],
    "structure": {"tag": "html", "attributes": {}, "children_count": 2},
}
```

Each element's `.text` becomes a segment tagged with the element name. Each element's `.tail` (text after its closing tag) becomes a segment tagged `"text"`. Whitespace is collapsed to single spaces and trimmed. `structure` describes only the root element.

`HTMLParser().reconstruct(structured)` turns the segment list back into `<p>` lines.

### `MarkdownParser`

`MarkdownParser` creates a `markdown_it.MarkdownIt("commonmark", {"breaks": True, "html": True})` instance and enables the `table` and `strikethrough` rules. `parse(content)` renders HTML and hands it to `HTMLParser.parse`. `reconstruct` delegates to `HTMLParser.reconstruct`.

## Models

`vexy_markliff.models` lazily exports three Pydantic models from `vexy_markliff.models.xliff`:

| Model | Fields |
|---|---|
| `TranslationUnit` | `id: str`, `source: str`, `target: str \| None = None`, `state: str = "new"` |
| `XLIFFFile` | `id: str`, `source_language: str`, `target_language: str`, `units: list[TranslationUnit]` |
| `XLIFFDocument` | `version: str = "2.1"`, `files: list[XLIFFFile]` |

`XLIFFDocument(source_lang="en", target_lang="es", content=None)` builds one file with id `file_1` from a parser result: every segment becomes a `TranslationUnit` with id `unit_<n>`, numbered from 1.

| Method | Purpose |
|---|---|
| `XLIFFDocument.to_xml()` | Serialize to the XML shown in [XLIFF output](output-format.md). Units with a non-empty `target` get a `<target>` element. |
| `XLIFFDocument.from_xml(xml)` | Parse XML back into models; reads `<target>` text and the `state` attribute. |
| `XLIFFDocument.content` | Property returning the parser-style dictionary built from unit `source` text. |

```python
from vexy_markliff.models.xliff import TranslationUnit, XLIFFDocument, XLIFFFile

doc = XLIFFDocument(
    files=[
        XLIFFFile(
            id="file_1",
            source_language="en",
            target_language="de",
            units=[TranslationUnit(id="unit_1", source="Hello", target="Hallo", state="translated")],
        )
    ]
)
print(doc.to_xml())
```

## Utilities

`vexy_markliff.utils` holds helpers used by the core modules:

| Function | Behaviour |
|---|---|
| `normalize_whitespace(text)` | Collapse runs of whitespace to one space and trim. |
| `validate_language_code(code)` | `True` for two lowercase ASCII letters. |
| `validate_file_path(path)` | `True` if the path exists and is a file. |
| `split_sentences_simple(text)` | Split on `.`, `!`, `?`; the punctuation is dropped. Not used by the converter. |
| `get_logger(name)` | Return `logging.getLogger(name)`. |
| `setup_logging(level="INFO")` | Call `logging.basicConfig` with a fixed format. |

`split_sentences_simple("Dr. Who? Yes. New sentence.")` returns `['Dr', 'Who', 'Yes', 'New sentence']`, which shows why it is not wired into the converter.
