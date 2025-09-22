---
this_file: docs/510-prefs-html0.md
---

# 2. HTML → XLIFF Structural Rules (Part 1)

## Scope
- Covers document-level, sectioning, block, and inline HTML5 elements that carry translatable text.
- Establishes how we rely on the XLIFF 2.1 Format Style module (`fs:fs`, `fs:subFs`) to retain HTML semantics.
- All attribute serialization follows the escaping rules in `docs/512-prefs-html2.md`.

## 1. Document skeleton & non-translatable wrappers
Elements: `<!DOCTYPE>`, `html`, `head`, `body`, `base`, `link`, `meta`, `script`, `style`, `noscript`, `template`.

- These nodes live in the XLIFF skeleton referenced from `<file><skeleton href="..."/>`.
- Place holders such as `###u17###` mark where localizable units return during merge.
- The only text promoted out of the skeleton is content inside child elements described in later sections (for example `<title>` or `<p>`).

**Skeleton example**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>###u1###</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body class="landing">###u2###</body>
</html>
```

## 2. Sectioning & grouping elements
Elements: `article`, `aside`, `details`, `dialog`, `div`, `fieldset`, `figure`, `figcaption`, `footer`, `header`, `main`, `menu`, `nav`, `section`, `summary`.

- Wrap each section as a `<unit>` or `<group>` with `fs:fs` pointing at the HTML element name.
- Store attributes in `fs:subFs` (escape commas/backslashes per `docs/512-prefs-html2.md`).
- Keep purely structural nodes (for example `<div>` with only child blocks) in the skeleton and promote only child blocks to units.
- Promote text-bearing nodes (`figcaption`, `summary`, `dialog`) into units so the strings are editable.

**Example**

```xml
<group id="nav" fs:fs="nav" fs:subFs="class,main-menu">
  <unit id="nav-title" fs:fs="h2">
    <segment><source>Site navigation</source></segment>
  </unit>
</group>
```

## 3. Lists
Elements: `ul`, `ol`, `li`, `menu`, `dl`, `dt`, `dd`.

- Represent each list container with a `<group>` whose `fs:fs` is the container tag.
- Each `<li>`, `<dt>`, `<dd>` becomes a child `<unit>` tagged with the element name.
- Preserve list-specific attributes (`start`, `type`, `reversed`, `value`) inside `fs:subFs`.
- For nested lists, create nested groups mirroring the HTML hierarchy.

**Example**

```xml
<group id="faq" fs:fs="dl">
  <unit id="q1" fs:fs="dt"><segment><source>What is Markliff?</source></segment></unit>
  <unit id="a1" fs:fs="dd"><segment><source>It is our HTML↔XLIFF bridge.</source></segment></unit>
</group>
```

## 4. Tabular structures
Elements: `table`, `caption`, `colgroup`, `col`, `thead`, `tbody`, `tfoot`, `tr`, `th`, `td`.

- Preserve the full table markup in a `<unit>` with `xml:space="preserve"` when cell structure must survive intact.
- Add `fs:fs="table"` (or the relevant element) on that unit and capture table-level attributes inside `fs:subFs`.
- If the table content needs cell-by-cell editing, break the table into child units while keeping the outer table skeleton in `originalData`.
- Use `<originalData>` with CDATA for complex tables to avoid double escaping.

**Example**

```xml
<unit id="pricing" fs:fs="table" fs:subFs="class,pricing" xml:space="preserve">
  <segment>
    <source><![CDATA[<table class="pricing"><thead><tr><th>Plan</th><th>Price</th></tr></thead>
    <tbody><tr><td>Starter</td><td>$9</td></tr></tbody></table>]]></source>
  </segment>
</unit>
```

## 5. Flow text blocks & headings
Elements: `address`, `blockquote`, `caption`, `h1`–`h6`, `hgroup`, `legend`, `p`, `pre`, `title`.

- Each element becomes a `<unit>` with `fs:fs` equal to the tag name.
- Preserve whitespace-sensitive elements (`pre`) using `xml:space="preserve"`.
- For `<title>` we use the skeleton placeholder pattern (see section 1) but store the string inside a unit so translators can update it.
- `hgroup` is treated as a container whose headings become sequential units; include a `group` wrapper tagged `hgroup` to retain semantics.

### 5.1 Segmentation policy
- `<s>` elements: never split; one segment per element.
- `<p>` elements: run sentence segmentation so each sentence becomes its own `<segment>`.
- Other block elements default to one segment unless the HTML already carries `<s>` or explicit inline segmentation cues.

## 6. Inline text semantics
Elements: `a`, `abbr`, `b`, `bdi`, `bdo`, `cite`, `code`, `data`, `del`, `dfn`, `em`, `i`, `ins`, `kbd`, `label`, `mark`, `output`, `q`, `ruby`, `rb`, `rp`, `rt`, `rtc`, `s`, `samp`, `small`, `span`, `strong`, `sub`, `sup`, `time`, `u`, `var`.

- Inline tags become `<mrk>` nodes nested inside the surrounding segment.
- Set `fs:fs` to the tag, and serialize attributes (for example `href`, `datetime`, `title`, `aria-*`) in `fs:subFs`.
- Preserve nested inline markup exactly as it appears; the merger replays the hierarchy when injecting the translation.
- For edit tracking tags (`ins`, `del`) include state attributes (for example `datetime`) so reviewers can reconstruct change history.
- Ruby annotations combine `ruby`, `rb`, `rt`, `rp`, `rtc` markers; keep them grouped so downstream tooling can rebuild East Asian text layout.

**Example**

```xml
<segment>
  <source>View the <mrk id="m1" fs:fs="a" fs:subFs="href,https://example.com\target,_blank">
    documentation</mrk> updated on <mrk id="m2" fs:fs="time" fs:subFs="datetime,2024-05-12">May 12</mrk>.</source>
</segment>
```

## 7. Directionality & emphasis helpers
- Apply `fs:subFs` to keep `lang`, `dir`, `translate`, and other global attributes on inline spans.
- For `<bdi>`/`<bdo>`, always retain the `dir` attribute; if missing, set `fs:subFs="dir,auto"` to capture defaults.
- Convert `<span>` or `<mark>` used solely for styling into `<mrk>` with the relevant class information so CSS round-trips cleanly.

These rules align with the preference tables in `docs/512-prefs-html2.md`, ensuring every HTML5 element now has a defined XLIFF strategy.
