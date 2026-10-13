# XLIFF output

This page describes the exact XML that version 1.3 writes and reads. It differs from the XLIFF 2.1 standard in ways that matter if you send the files to a CAT tool or translation management system.

## Document shape

`XLIFFDocument.to_xml()` builds the tree with `lxml` and serializes it with `pretty_print=True`. There is no `<?xml …?>` declaration.

```xml
<xliff version="2.1" xmlns="urn:oasis:names:tc:xliff:document:2.1">
  <file id="file_1" source-language="en" target-language="fr">
    <trans-unit id="unit_1" state="new">
      <source>Hello</source>
    </trans-unit>
    <trans-unit id="unit_2" state="new">
      <source>This is</source>
    </trans-unit>
    <trans-unit id="unit_3" state="new">
      <source>bold</source>
    </trans-unit>
    <trans-unit id="unit_4" state="new">
      <source>text. Second sentence.</source>
    </trans-unit>
  </file>
</xliff>
```

That output comes from this Markdown:

```markdown
# Hello

This is **bold** text. Second sentence.
```

| Element or attribute | Value |
|---|---|
| `xliff/@version` | Always `2.1` |
| `xliff/@xmlns` | `urn:oasis:names:tc:xliff:document:2.1` |
| `file/@id` | Always `file_1` (one file per document) |
| `file/@source-language`, `file/@target-language` | The language codes you passed |
| `trans-unit/@id` | `unit_1`, `unit_2`, … in document order |
| `trans-unit/@state` | `new` for freshly extracted units |
| `source` | One text node from the input, whitespace collapsed |
| `target` | Written only when a unit has non-empty target text |

## How units are cut

The extractor walks the HTML tree depth first. For each element it emits the element's leading text, then recurses into each child, then emits the child's tail text. Every non-empty piece becomes its own unit.

Consequences:

- A paragraph with inline markup becomes several units. `This is **bold** text.` gives `This is`, `bold` and `text.`.
- A paragraph without inline markup stays one unit, however many sentences it has. No sentence splitting is done.
- Markup is dropped. Link targets, image `alt` text and all other attributes are not extracted.
- Code blocks and `<script>` or `<style>` contents are extracted like any other text.

## Differences from XLIFF 2.1

The XLIFF 2.1 core uses the namespace `urn:oasis:names:tc:xliff:document:2.0` with `version="2.1"`, the attributes `srcLang`/`trgLang` on `<xliff>`, and the elements `<unit>` and `<segment>`. Version 1.3 of `vexy-markliff` instead writes:

- XLIFF 1.2 element and attribute names: `<trans-unit>`, `source-language`, `target-language`.
- `state` on `<trans-unit>`; in XLIFF 2.1 `state` belongs on `<segment>`.
- A namespace URI ending in `2.1`.

A tool that validates against the XLIFF 2.1 schema will reject these files. The [design notes](design/xliff-primer.md) describe the standard structure that the project is meant to produce.

## Reading XLIFF back

`XLIFFDocument.from_xml()` parses the XML with `lxml` and looks for:

- `//xliff:file` and `.//xliff:trans-unit`, with `xliff` bound to `urn:oasis:names:tc:xliff:document:2.1`;
- the `source-language`, `target-language`, `id` and `state` attributes;
- the text of the first `<source>` and `<target>` child.

Anything else is ignored. A file in another namespace, or one that uses `<unit>`/`<segment>`, parses without error but yields zero units.

`xliff_to_markdown` and `xliff_to_html` then write one line per unit:

```html
<p>Hello</p>
<p>This is</p>
<p>bold</p>
<p>text. Second sentence.</p>
```

The `<source>` text is used even when a `<target>` exists, so filling in translations and converting back returns the original language. Only the text of `<source>` itself is read; text inside child elements of `<source>` is lost.

## Sample files

The documentation site carries a short passage in four localization formats (XLIFF 2.1, PO, Qt TS and RESX) for comparison. See [Sample files](design/samples.md).
