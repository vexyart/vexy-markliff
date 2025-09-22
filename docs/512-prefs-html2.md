---
this_file: docs/512-prefs-html2.md
---

# 4. HTML → XLIFF Structural Rules (Part 3)

## Scope
- Consolidates cross-cutting rules for attributes, namespaces, foreign content, and legacy tags.
- Provides a complete lookup table covering every HTML5 element with references back to handling instructions in `docs/510-prefs-html0.md` and `docs/511-prefs-html1.md`.

## 1. Namespace & attribute handling
- Always declare `xmlns="urn:oasis:names:tc:xliff:document:2.0"` and `xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"` on `<xliff>` roots.
- Store HTML attribute name/value pairs inside `fs:subFs` using the escape rules below so round-tripping remains lossless.

### 1.1 `fs:subFs` escaping rules
- `,` separates the attribute name from its value (`href,https://example.com`).
- `\` separates attribute pairs (`class,hero\id,lead`).
- Escape literal commas as `\,` and literal backslashes as `\\`.
- Empty attribute values become `name,`.

### 1.2 Original data payloads
- Use `<originalData><data id="...">…</data></originalData>` to hold verbatim HTML fragments.
- Prefer CDATA to avoid double escaping when the fragment contains `<` or `&` characters.

## 2. Custom elements, web components & foreign content
- Elements whose names contain a hyphen (for example `<app-shell>`) are treated like inline spans: wrap their textual content in `<unit>`/`<mrk>` structures with `fs:fs` set to the literal tag name.
- `<template>` content stays in the skeleton unless it contains user-facing fallback strings—in that case, promote the text to units but keep execution scaffolding untouched.
- `<slot>` and `slot="…"` attributes are serialized into `fs:subFs`; fallback text inside slots is handled as regular inline content.
- SVG or MathML embedded inside HTML should stay intact inside a `<unit>` with `xml:space="preserve">`; do not rewrite their internal structure.

## 3. Deprecated & legacy elements
Elements: `acronym`, `applet`, `basefont`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `hgroup` (historically obsolete but still encountered), `isindex`, `marquee`, `menuitem`, `noframes`, `strike`, `tt`.

- Preserve them exactly as author-supplied, using the same strategies described for their modern counterparts (for example `center` behaves like `div`).
- Surface the visible text through `<unit>` and `<mrk>` elements so translators can edit legacy content safely.

## 4. Complete HTML element reference
Reference column abbreviations: `510 §n` → section number inside `docs/510-prefs-html0.md`; `511 §n` → section number inside `docs/511-prefs-html1.md`.

### 4.1 Document & metadata

| Elements | Handling summary | Reference |
|----------|------------------|-----------|
| `<!DOCTYPE>` | Remains in skeleton alongside file scaffolding. | 510 §1 |
| `html`, `head`, `body` | Skeleton placeholders; promote child text via units. | 510 §1 |
| `base`, `link`, `meta` | Skeleton-first; inline fallbacks use `<ph>` with `originalData`. | 510 §1 / 511 §1 |
| `title` | Unit with `fs:fs="title"`; placeholder embedded in skeleton. | 510 §5 |
| `style`, `script`, `noscript` | Skeleton; `noscript` fallback text promoted to unit. | 511 §4 |
| `template` | Skeleton unless it contains fallback text; then treat as unit with placeholders. | 511 §4 |

### 4.2 Sectioning & grouping

| Elements | Handling summary | Reference |
|----------|------------------|-----------|
| `article`, `aside`, `main`, `nav`, `section` | `<group>`/`<unit>` wrappers tagged with `fs:fs` + attributes. | 510 §2 |
| `header`, `footer`, `div` | Skeleton wrapper; promote textual children to units. | 510 §2 |
| `figure`, `figcaption` | `figure` as group/unit; `figcaption` as text unit. | 510 §2 |
| `details`, `summary`, `dialog` | Preserve block with `fs:fs`; extract textual children as units. | 510 §2 |
| `fieldset`, `legend` | Group for fieldset, legend as unit. | 510 §2 / 511 §3 |
| `menu` | Treat like list container (`<group fs:fs="menu">`). | 510 §3 |

### 4.3 Text-level semantics & phrasing content

| Elements | Handling summary | Reference |
|----------|------------------|-----------|
| `p`, `address`, `blockquote`, `pre`, `caption` | Units with `fs:fs`; manage segmentation as defined. | 510 §5 |
| `h1`–`h6`, `hgroup` | Units tagged with heading level; `hgroup` wraps child units. | 510 §5 |
| `span`, `mark`, `strong`, `em`, `i`, `b`, `u`, `small`, `s` | `<mrk>` inline markers with attribute capture. | 510 §6 |
| `cite`, `q`, `dfn`, `abbr`, `var`, `code`, `kbd`, `samp` | `<mrk>` inline markers with semantics in `fs:fs`. | 510 §6 |
| `time`, `data`, `output`, `label` | `<mrk>` inline markers retaining value attributes. | 510 §6 |
| `sub`, `sup`, `bdi`, `bdo`, `ruby`, `rb`, `rt`, `rp`, `rtc` | `<mrk>` inline markers; maintain direction/ruby metadata. | 510 §6 |
| `del`, `ins` | Inline `<mrk>`; include change metadata in `fs:subFs`. | 510 §6 |
| `hr` | `<ph>` placeholder for horizontal rules. | 511 §1 |
| `br`, `wbr` | `<ph>` placeholders referencing `originalData`. | 511 §1 |

### 4.4 Lists & tables

| Elements | Handling summary | Reference |
|----------|------------------|-----------|
| `ul`, `ol`, `li` | Container groups + child units; preserve numbering attributes. | 510 §3 |
| `dl`, `dt`, `dd` | Definition list as group; term/definition units. | 510 §3 |
| `table`, `caption`, `thead`, `tbody`, `tfoot`, `tr`, `th`, `td` | Table preserved as unit or nested groups; `xml:space="preserve"` when needed. | 510 §4 |
| `colgroup`, `col` | Remain inside preserved table markup; use placeholders if edited separately. | 510 §4 / 511 §1 |

### 4.5 Forms & interactive controls

| Elements | Handling summary | Reference |
|----------|------------------|-----------|
| `form` | Preserve as unit with placeholders for controls; textual children as units. | 511 §3 |
| `label`, `legend`, `button` | Units containing visible text. | 510 §6 / 511 §3 |
| `input`, `textarea`, `select` | Placeholders inside the parent form unit. | 511 §3 |
| `option`, `optgroup`, `datalist` | Units for visible captions; `option` text localized per item. | 511 §3 |
| `meter`, `progress`, `output` | Placeholders for control markup + optional inline `<mrk>` for textual fallback. | 511 §3 |

### 4.6 Embedded content & graphics

| Elements | Handling summary | Reference |
|----------|------------------|-----------|
| `img`, `picture`, `source`, `track` | `<ph>` placeholders inside media units; retain attributes. | 511 §1 / §2 |
| `audio`, `video` | Units with `fs:fs`; child sources/tracks as placeholders. | 511 §2 |
| `map`, `area` | Map as unit; area elements as placeholders inside the unit. | 511 §2 |
| `iframe`, `embed`, `object`, `param` | Units containing full markup; children recorded via `originalData`. | 511 §2 |
| `canvas` | Preserve drawing surface as unit with `xml:space="preserve"`. | 511 §2 |
| `svg`, `math` | Store entire fragment in unit; do not alter internal markup. | 511 §2 |

### 4.7 Scripting, web components & custom tags

| Elements | Handling summary | Reference |
|----------|------------------|-----------|
| `script` | Skeleton only; no in-line translation. | 511 §4 |
| `noscript` | Fallback text extracted as unit; wrapper in skeleton. | 511 §4 |
| `template`, `slot` | Preserve structure, promote fallback text when present. | 511 §4 |
| Custom elements (`geo-map`, `app-shell`, etc.) | Treat like inline or block elements depending on content; store tag name in `fs:fs`. | 511 §4 |

With this table we can audit coverage quickly while cross-referencing the authoritative handling instructions.

## 5. Validation checklist
- Verify that every `<unit>` created from HTML carries `fs:fs` matching the original tag.
- Ensure all placeholder `<ph>` nodes reference a defined `<data id="…">` entry.
- Confirm segmentation rules: `<s>` elements map 1:1 with `<segment>` entries; paragraphs run through sentence splitting.
- Compare conversions against the official OASIS XLIFF 2.1 specification located at `external/901-xliff-spec-core-21.xml` whenever uncertainty arises.
