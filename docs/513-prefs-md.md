---
this_file: docs/513-prefs-md.md
---

# 5. Markdown → HTML → XLIFF Mapping

## Scope & pipeline
- Markdown content is converted to semantic HTML using `markdown-it-py` (CommonMark + selected extensions).
- The resulting HTML is processed by the HTML rules defined in `docs/510-prefs-html0.md`, `docs/511-prefs-html1.md`, and `docs/512-prefs-html2.md`.
- Markdown syntax that does not map to HTML (for example raw prose inside fenced code blocks) is treated as literal text inside `<segment>` elements.

### Conversion stages
1. **Parse Markdown** → token stream (markdown-it-py).
2. **Render HTML** → deterministic HTML5 markup.
3. **Apply HTML rules** → XLIFF extraction using Format Style metadata.
4. **Persist Markdown hints** → store data needed for round-trip reconstruction in unit-level metadata (see §4).

## 1. Block-level constructs

| Markdown feature | HTML emitted | XLIFF handling | Reference |
|------------------|--------------|----------------|-----------|
| Headings (`#`…`######`) | `<h1>`…`<h6>` | Each heading becomes a `<unit fs:fs="hN">`; keep hierarchy, allow sentence splitting if `<s>` is present. | 510 §5 |
| Paragraphs | `<p>` | One `<unit>` per paragraph; sentence split each `<p>` into `<segment>` entries. | 510 §5 |
| Block quotes (`>`) | Nested `<blockquote>` + `<p>` | Outer `<group fs:fs="blockquote">`; inner paragraphs follow paragraph rules. | 510 §2 / §5 |
| Lists (`-`, `*`, digits) | `<ul>`/`<ol>` with `<li>` | Create `<group fs:fs="ul|ol">` and child `<unit fs:fs="li">`; preserve attributes (`start`, `type`). | 510 §3 |
| Definition lists (extension) | `<dl>` + `<dt>/<dd>` | Same pattern as HTML definition lists. | 510 §3 |
| Code fences | `<pre><code>` | `<unit fs:fs="pre" xml:space="preserve">` with content stored verbatim. | 510 §5 |
| Horizontal rules (`---`, `***`, `___`) | `<hr/>` | `<ph>` placeholder referencing `originalData`. | 511 §1 |
| Tables (extension) | `<table>` markup | Preserve entire table as `xml:space="preserve"` unit unless cell granularity is required. | 510 §4 |
| Footnotes (extension) | `<section class="footnotes">` etc. | Footnote section uses groups/units mirroring generated HTML; links are inline `<mrk>` elements. | 510 §2 / §6 |
| Front matter (YAML/TOML) | Metadata block | Retain unchanged; store snapshot in `<notes>` and exclude from translation segments. | 513 §4 |

### Example: headings & paragraphs

```markdown
# Product Overview
Welcome to **Vexy Markliff**.
```

```xml
<unit id="h1" fs:fs="h1"><segment><source>Product Overview</source></segment></unit>
<unit id="p1" fs:fs="p">
  <segment><source>Welcome to <mrk id="m1" fs:fs="strong">Vexy Markliff</mrk>.</source></segment>
</unit>
```

## 2. Inline constructs

| Markdown feature | HTML emitted | XLIFF handling | Reference |
|------------------|--------------|----------------|-----------|
| Emphasis / strong (`*`, `_`, `**`, `__`) | `<em>`, `<strong>` | `<mrk>` markers with `fs:fs="em|strong"`; nested emphasis supported. | 510 §6 |
| Inline code (`` `code` ``) | `<code>` | `<mrk fs:fs="code">`; escape backticks in HTML stage. | 510 §6 |
| Links | `<a href="…">` | `<mrk fs:fs="a" fs:subFs="href,…">`; titles preserved in `fs:subFs`. | 510 §6 |
| Images (`![alt](src)`) | `<img/>` | `<ph>` placeholder referencing `originalData`; alt text stays inside HTML attribute. | 511 §1 |
| Autolinks / reference links | `<a>` | Same handling as links; reference definitions serialized once into metadata to recreate Markdown syntax. | 510 §6 / 513 §4 |
| Strikethrough (`~~`) | `<del>` | Inline `<mrk fs:fs="del">`. | 510 §6 |
| Task items (`- [ ]`) | `<li>` with `<input type="checkbox">` | Checkbox rendered as placeholder inside list item; list text follows normal rules. | 510 §3 / 511 §3 |
| Footnote references | `<sup><a>` | Superscript and link converted into nested `<mrk>` structures. | 510 §6 |

### Example: links & images

```markdown
See [docs](https://example.com) and ![logo](logo.svg).
```

```xml
<segment>
  <source>See <mrk id="m1" fs:fs="a" fs:subFs="href,https://example.com">docs</mrk>
    and <ph id="ph1" dataRef="img1"/>.</source>
</segment>
<originalData>
  <data id="img1">&lt;img src="logo.svg" alt="logo"/&gt;</data>
</originalData>
```

## 3. HTML passthrough & custom syntax
- Raw HTML inside Markdown bypasses Markdown-specific processing and is handled strictly by the HTML rules.
- Unknown Markdown extensions that emit custom elements (`<note-box>`, `<callout>`) follow the custom-element policy in `docs/512-prefs-html2.md`.
- Guard against mixed content: when Markdown renders inline HTML that introduces new block boundaries, trust the HTML segmentation to create separate units.

## 4. Round-trip metadata
To reconstruct Markdown faithfully after translation, record the following in unit-level metadata (for example using `<notes>`, or custom `fs:subFs` keys on the unit):

- **Emphasis markers**: `*` vs `_`, and the number of characters for strong emphasis.
- **Code fences**: fence character (` ``` ` or `~~~`) and info string (language).
- **Links**: whether original syntax was inline or reference; keep reference labels and definitions together.
- **Task list state**: store original `[ ]` / `[x]` token plus whether the checkbox was disabled.
- **Tables**: column alignment markers (`:---`, `:---:`) captured as metadata to recreate Markdown table formatting.
- **Front matter**: original serialization (YAML/TOML/JSON) stored verbatim so we can write it back untouched.

## 5. Error handling & fallbacks
- If Markdown yields HTML outside the mapped set, log the offending tag and fall back to treating it as literal text within a `<segment>` while recording an extraction note.
- When Markdown content contains HTML entities, rely on the HTML renderer for unescaping; the XLIFF exporter should not double-escape these sequences.
- Any Markdown extension that injects script/style blocks must be disabled or whitelisted explicitly; we do not localize executable content.

## 6. Testing checklist
- Render Markdown fixtures to HTML and diff against expected HTML snapshots before running XLIFF extraction.
- Verify that every generated `<unit>` carries an `fs:fs` value that matches the HTML element name.
- Run round-trip tests (`markdown → XLIFF → markdown`) covering headings, lists, tables, code fences, task lists, and footnotes.
- Confirm that metadata emitted during extraction reproduces the original Markdown syntax when merging back.

By anchoring Markdown processing to the HTML handling rules, Vexy Markliff avoids duplicating logic and guarantees that Markdown localization quality matches the robustness of our HTML workflow.
