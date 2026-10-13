# XLIFF 2.1 primer

XLIFF (XML Localization Interchange File Format) is the OASIS standard for passing translatable text between tools. Version 2.1 became an OASIS Standard on 13 February 2018. It keeps the 2.0 core and adds, among other things, normative support for the W3C Internationalization Tag Set (ITS) 2.0.

This page summarizes the parts of XLIFF 2.1 that the `vexy-markliff` design relies on.

## Extraction and merge

An XLIFF workflow is a round trip:

1. An **extractor** reads the original document, separates translatable text from structure, and writes an XLIFF file plus, optionally, a skeleton.
2. Translators fill in `<target>` elements in a CAT tool, which protects the inline codes.
3. A **merger** puts the translated text back into the structure and writes the translated document.

The XLIFF file is a bitext: source and translation side by side, organized into units.

## Core structure

| Element | Role |
|---|---|
| `<xliff>` | Root. Attributes `version` (`2.1`), `srcLang` (required) and `trgLang` (required once any `<target>` exists). Namespace `urn:oasis:names:tc:xliff:document:2.0`. |
| `<file>` | Everything extracted from one original document. `id` is required; `original` names the source file. |
| `<skeleton>` | The non-translatable remainder of the original, embedded or referenced with `href`. |
| `<group>` | Optional container for units that mirror nested structure, for example a list. |
| `<unit>` | One logical block of text, such as a paragraph, heading or list item. Tools must not change the unit structure. |
| `<segment>` | One source/target pair inside a unit. A unit can hold several segments, for example one per sentence. Segmentation may change during translation. |
| `<source>`, `<target>` | The text, including inline codes. |
| `<notes>` / `<note>` | Comments for translators. |
| `<originalData>` / `<data>` | The original markup that inline codes refer to. |

The split between a fixed `<unit>` structure and flexible `<segment>` boundaries is what lets a merger rebuild the document reliably while still allowing sentence-level translation.

## Inline codes

XLIFF 1.2 used `<bpt>`, `<ept>`, `<ph>` and `<it>`. XLIFF 2.x replaces them with three elements:

| Element | Purpose | Content | Typical HTML or Markdown |
|---|---|---|---|
| `<ph>` | Placeholder for a standalone code | Empty, e.g. `<ph id="1" dataRef="d1"/>` | `<img>`, `<br>`, `<hr>`, Markdown `---` |
| `<pc>` | Paired code around text | Text and nested codes | `<b>…</b>`, `<a href="…">…</a>`, `**bold**` |
| `<mrk>` | Annotation of a span | Text and nested codes | `translate="no"`, terminology |

`vexy-markliff` deliberately uses `<mrk>` with Format Style attributes for inline HTML elements, and `<ph>` for void elements. It does not use `<pc>` or `dataRefStart`/`dataRefEnd`. See [HTML mapping rules](html-rules.md).

## Format Style module

The Format Style module (namespace `urn:oasis:names:tc:xliff:fs:2.0`) adds two attributes that let a tool rebuild a preview of the original:

- `fs:fs` names the original element, for example `p`, `h1` or `a`.
- `fs:subFs` carries its attributes as name/value pairs, for example `href,https://example.com`.

The design uses these attributes as the record of the original markup on `<unit>`, `<group>` and `<mrk>` elements. The escaping rules are in [HTML mapping rules](html-rules.md#attribute-encoding-in-fssubfs).

## ITS 2.0

ITS 2.0 is a W3C Recommendation for localization metadata in XML and HTML. XLIFF 2.1 maps several of its data categories:

| ITS data category | In HTML | In XLIFF 2.1 |
|---|---|---|
| Translate | `translate="no"` | Block level: `translate="no"` on `<unit>`. Inline: `<mrk translate="no">`. |
| Preserve Space | `xml:space="preserve"`, `<pre>` | `xml:space="preserve"` on the unit |
| Localization Note | ITS note markup | `<note>` inside the unit's `<notes>` |
| Terminology, Allowed Characters, Storage Size | ITS attributes | Carried through to the matching XLIFF modules |

## Worked example

Input `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Product Information</h1>
    <p>Please visit <a href="https://example.com">our website</a> for more details.</p>
</body>
</html>
```

Skeleton `skeleton/index.skl.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>###u1###</title>
</head>
<body>
    <h1>###u2###</h1>
    <p>###u3###</p>
</body>
</html>
```

XLIFF after translation into Spanish:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.0"
       xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"
       version="2.1" srcLang="en" trgLang="es">
  <file id="f1" original="index.html">
    <skeleton href="skeleton/index.skl.html"/>
    <unit id="u1" fs:fs="title">
      <segment>
        <source>Welcome</source>
        <target>Bienvenido</target>
      </segment>
    </unit>
    <unit id="u2" fs:fs="h1">
      <segment>
        <source>Product Information</source>
        <target>Información del producto</target>
      </segment>
    </unit>
    <unit id="u3" fs:fs="p">
      <segment>
        <source>Please visit <mrk id="m1" fs:fs="a"
          fs:subFs="href,https://example.com">our website</mrk> for more details.</source>
        <target>Visite <mrk id="m1" fs:fs="a"
          fs:subFs="href,https://example.com">nuestro sitio web</mrk> para más detalles.</target>
      </segment>
    </unit>
  </file>
</xliff>
```

The merger replaces `###u1###` to `###u3###` with the target text and rebuilds the `<a>` element from the `<mrk>` attributes.

Compare this with what version 1.3 writes today in [XLIFF output](../output-format.md).
