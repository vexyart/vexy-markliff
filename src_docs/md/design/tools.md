# Libraries and tools

The design builds on a few third-party libraries and specifications. This page records what each one contributes and which parts the project uses or plans to use.

## Specifications

| Specification | Relevance |
|---|---|
| OASIS XLIFF Version 2.1 (OASIS Standard, 13 February 2018) | Target format: core elements, inline codes, Format Style module, ITS integration. Core namespace `urn:oasis:names:tc:xliff:document:2.0`. |
| W3C Internationalization Tag Set (ITS) 2.0 | Localization metadata in HTML (`translate`, notes, terminology), mapped into XLIFF 2.1 |
| Unicode Standard Annex #29 | Default sentence boundaries; see [Sentence segmentation](segmentation.md) |
| CommonMark | The Markdown dialect `markdown-it-py` implements |

## markdown-it-py

A Python port of the JavaScript `markdown-it` parser. It is CommonMark compliant, produces a token stream that can be inspected or changed before rendering, and supports presets (`commonmark`, `gfm-like`, `zero`) and plugins.

Version 1.3 uses it as follows (see `core/parser.py`):

```python
import markdown_it

md = markdown_it.MarkdownIt("commonmark", {"breaks": True, "html": True})
md.enable(["table", "strikethrough"])
html = md.render(text)
```

`markdown-it-py` renders to HTML only; it has no Markdown writer. Writing Markdown after translation therefore needs the round-trip metadata described in [Markdown mapping rules](markdown-rules.md#round-trip-metadata).

## mdit-py-plugins

The companion package for `markdown-it-py` extensions. The design plans to use these (not yet a dependency):

| Plugin | Adds |
|---|---|
| Front matter | YAML or TOML metadata block at the start of the document |
| Footnotes | Reference and inline footnotes |
| Definition lists | Pandoc-style term/definition lists |
| Task lists | `[ ]` and `[x]` checkboxes in list items |
| Attributes | `{#id .class}` attributes on elements |
| Containers, colon fences | Custom fenced blocks |
| Heading anchors | `id` attributes on headings |

## lxml

Parses HTML (`lxml.html.fromstring`) and builds and parses XLIFF (`lxml.etree`). Reading units out of a standard XLIFF 2 file with `lxml` looks like this:

```python
from lxml import etree

ns = {"x": "urn:oasis:names:tc:xliff:document:2.0"}
root = etree.fromstring(xliff_bytes)
for unit in root.iterfind(".//x:unit", ns):
    for segment in unit.iterfind("x:segment", ns):
        source = segment.find("x:source", ns)
        target = segment.find("x:target", ns)
        print(unit.get("id"), source.text, target.text if target is not None else None)
```

## Translate Toolkit

A Python toolkit with converters between localization formats and quality checks. It is useful next to `vexy-markliff` when a translation vendor needs a different format:

| Task | Command |
|---|---|
| PO to XLIFF | `po2xliff messages.de.po messages.de.xlf` |
| XLIFF to PO | `xliff2po messages.de.xlf messages.de.po` |
| Markdown to a PO template | `md2po README.md README.pot` |

## Other formats

XLIFF is one of several bilingual formats. Plural forms are not native to XLIFF; the usual practice is to embed ICU MessageFormat inside the segment and let the tooling parse both layers:

```xml
<unit id="file_count">
  <notes><note>Pluralized string (# substituted)</note></notes>
  <segment>
    <source>{count, plural, one {# file} other {# files}}</source>
    <target>{count, plural, one {# plik} few {# pliki} other {# plików}}</target>
  </segment>
</unit>
```

See [Sample files](samples.md) for the same text in XLIFF, PO, Qt TS and RESX.
