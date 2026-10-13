# Markdown mapping rules

!!! warning "Specification"
    These rules describe the planned behaviour. Version 1.3 renders Markdown to HTML and extracts plain text nodes; it records no round-trip metadata.

Markdown is never mapped to XLIFF directly. It is rendered to HTML first, and the HTML goes through the [HTML mapping rules](html-rules.md). This keeps one set of extraction rules for both input formats. What Markdown adds is metadata: the information needed to write Markdown, not just HTML, after translation.

## Pipeline

1. **Parse.** `markdown-it-py` turns the Markdown into a token stream.
2. **Render.** The tokens are rendered to deterministic HTML5.
3. **Extract.** The HTML rules produce units, groups, markers and placeholders.
4. **Record hints.** Markdown-specific details are stored on each unit so the merger can rebuild the original syntax.

Version 1.3 performs steps 1 and 2 with the CommonMark preset plus the `table` and `strikethrough` rules, and with raw HTML enabled.

## Block constructs

| Markdown | HTML | XLIFF |
|---|---|---|
| Headings `#` to `######` | `<h1>`–`<h6>` | `<unit fs:fs="hN">` |
| Paragraphs | `<p>` | One unit per paragraph, one segment per sentence |
| Block quotes `>` | `<blockquote>` with `<p>` | `<group fs:fs="blockquote">` around paragraph units |
| Lists `-`, `*`, `1.` | `<ul>`/`<ol>` with `<li>` | `<group fs:fs="ul">` or `"ol"` with `<unit fs:fs="li">`; `start` and `type` kept |
| Definition lists (plugin) | `<dl>`, `<dt>`, `<dd>` | As HTML definition lists |
| Fenced code | `<pre><code>` | `<unit fs:fs="pre" xml:space="preserve">`, content verbatim |
| Thematic break `---`, `***`, `___` | `<hr>` | `<ph>` with `<originalData>` |
| Tables (extension) | `<table>` | Preserved unit unless cell-level translation is needed |
| Footnotes (plugin) | Footnote section and back links | Groups and units mirroring the HTML; links as `<mrk>` |
| Front matter (plugin) | Not rendered | Kept verbatim in metadata; not translated |

Example:

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

## Inline constructs

| Markdown | HTML | XLIFF |
|---|---|---|
| `*em*`, `_em_`, `**strong**`, `__strong__` | `<em>`, `<strong>` | `<mrk fs:fs="em">`, `<mrk fs:fs="strong">`; nesting allowed |
| `` `code` `` | `<code>` | `<mrk fs:fs="code">` |
| `[text](url "title")` | `<a href title>` | `<mrk fs:fs="a" fs:subFs="href,…">` with the title in `fs:subFs` |
| `![alt](src)` | `<img>` | `<ph>` with `<originalData>`; the `alt` text stays in the attribute |
| Autolinks, reference links | `<a>` | As links; reference definitions stored once in metadata |
| `~~strike~~` | `<s>` | `<mrk fs:fs="s">` |
| Task items `- [ ]` (plugin) | `<li>` with `<input type="checkbox">` | Checkbox as placeholder; item text as usual |
| Footnote references (plugin) | `<sup><a>` | Nested `<mrk>` |

!!! note
    The original design note maps strikethrough to `<del>`. `markdown-it-py` renders `~~text~~` as `<s>text</s>`, so the marker carries `fs:fs="s"`.

Example:

```markdown
See [docs](https://example.com) and ![logo](logo.svg).
```

```xml
<unit id="p2" fs:fs="p">
  <originalData>
    <data id="img1">&lt;img src="logo.svg" alt="logo"/&gt;</data>
  </originalData>
  <segment>
    <source>See <mrk id="m1" fs:fs="a" fs:subFs="href,https://example.com">docs</mrk>
      and <ph id="ph1" dataRef="img1"/>.</source>
  </segment>
</unit>
```

## Raw HTML and custom syntax

- Raw HTML inside Markdown skips Markdown processing and goes straight to the HTML rules.
- Extensions that emit custom elements (`<note-box>`, `<callout>`) follow the custom-element rule in [HTML mapping rules](html-rules.md#scripts-templates-and-custom-elements).
- When inline HTML introduces new block boundaries, the HTML segmentation decides the units.

## Round-trip metadata

To write Markdown, not HTML, after translation, each unit records (in `<notes>` or in extra `fs:subFs` keys):

| Construct | What to record |
|---|---|
| Emphasis | `*` or `_`, and the marker length for strong emphasis |
| Code fences | Fence characters (` ``` ` or `~~~`) and the info string |
| Links | Inline or reference style; reference labels and definitions |
| Task items | The original `[ ]` or `[x]` token and whether the box was disabled |
| Tables | Column alignment markers (`:---`, `:---:`, `---:`) |
| Front matter | The original serialization (YAML, TOML or JSON), verbatim |

## Errors and fallbacks

- HTML outside the mapped set is logged and treated as literal text inside a segment, with an extraction note.
- HTML entities are unescaped by the renderer; the XLIFF writer must not escape them twice.
- Extensions that inject `<script>` or `<style>` must be disabled or explicitly allowed. Executable content is never localized.

## Test checklist

- Render Markdown fixtures to HTML and compare with stored HTML snapshots before testing extraction.
- Every generated unit has `fs:fs` matching its HTML element.
- `markdown → XLIFF → markdown` round trips cover headings, lists, tables, code fences, task lists and footnotes.
- The recorded metadata reproduces the original Markdown syntax when merging back.
