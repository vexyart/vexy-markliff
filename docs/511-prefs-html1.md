---
this_file: docs/511-prefs-html1.md
---

# 3. HTML → XLIFF Structural Rules (Part 2)

## Scope
- Defines handling for HTML5 void elements, embedded media, and form controls.
- Builds on `docs/510-prefs-html0.md`; attribute serialization and escaping still follow `docs/512-prefs-html2.md`.

## 1. Void & placeholder elements
Primary elements: `area`, `base`, `br`, `col`, `embed`, `hr`, `img`, `input`, `link`, `meta`, `param`, `source`, `track`, `wbr`.

- Represent each occurrence with a `<ph>` tag whose `dataRef` points to `originalData`.
- `originalData` holds the literal HTML (escaped or wrapped in CDATA when needed).
- Metadata-only tags (`base`, `link`, `meta`) usually remain in the skeleton, but this rule covers inline fallbacks when they appear in mixed content (for example Markdown raw HTML).
- Provide deterministic IDs (for example `ph-img-001`) so merge operations can match placeholders back to their HTML counterparts.

**Example**

```xml
<unit id="hero-copy" fs:fs="p">
  <originalData>
    <data id="img1">&lt;img src="hero.png" alt="Dashboard screenshot" width="640" height="320"/&gt;</data>
    <data id="br1">&lt;br/&gt;</data>
  </originalData>
  <segment>
    <source><ph id="ph-img1" dataRef="img1"/> Experience Markliff today.<ph id="ph-br1" dataRef="br1"/></source>
  </segment>
</unit>
```

## 2. Embedded & interactive media
Elements: `audio`, `video`, `canvas`, `iframe`, `map`, `object`, `picture`, `svg`, `math` (foreign content), plus supporting children `area`, `source`, `track`, `param`.

- For self-contained widgets (`iframe`, `canvas`, `object`, `svg`, `math`), store the full markup inside a `<unit>` with `xml:space="preserve"`.
- Maintain hierarchy when `picture` wraps multiple `source` tags; keep the wrapper as a `<unit>` and reference children through `originalData` entries so resolvers can rebuild the responsive set.
- `map` regions: record the `<map>` element as a `<unit>` and treat each `<area>` as a placeholder inside it.
- `audio`/`video`: if they contain captions or tracks, mirror the nesting as groups (`fs:fs="audio"`, child placeholders for `<source>` and `<track>`). Embed transcripts as child units when present.

**Example**

```xml
<unit id="product-video" fs:fs="video" fs:subFs="controls,\true\width,640" xml:space="preserve">
  <originalData>
    <data id="src-main">&lt;source src="promo.mp4" type="video/mp4"/&gt;</data>
    <data id="src-webm">&lt;source src="promo.webm" type="video/webm"/&gt;</data>
    <data id="trk-en">&lt;track kind="subtitles" src="promo-en.vtt" srclang="en" label="English" default&gt;</data>
  </originalData>
  <segment>
    <source><ph id="ph-src1" dataRef="src-main"/><ph id="ph-src2" dataRef="src-webm"/><ph id="ph-trk1" dataRef="trk-en"/></source>
  </segment>
</unit>
```

## 3. Forms & controls
Elements: `form`, `button`, `datalist`, `fieldset`, `input`, `label`, `legend`, `meter`, `optgroup`, `option`, `output`, `progress`, `select`, `textarea`.

- Preserve complete forms (`<form>` through closing tag) as `<unit>` blocks with `xml:space="preserve"`; this keeps validation attributes intact.
- Inside forms, treat visible text (for example `<label>`, button captions) as child units so translators can edit them without touching markup.
- Void controls (`input`, `meter`, `progress`) use placeholders, but they remain inside the parent unit to maintain ordering.
- When Markdown produces standalone inputs (task lists), fall back to the placeholder workflow defined above.

**Example**

```xml
<unit id="contact-form" fs:fs="form" fs:subFs="action,/submit\method,POST" xml:space="preserve">
  <segment>
    <source><![CDATA[<form action="/submit" method="POST">
  <label for="name">###u-name###</label>
  <input id="name" name="name" type="text" required>
  <button type="submit">###u-submit###</button>
</form>]]></source>
  </segment>
</unit>
<unit id="u-name" fs:fs="label"><segment><source>Name</source></segment></unit>
<unit id="u-submit" fs:fs="button"><segment><source>Send</source></segment></unit>
```

## 4. Scripting & templating hooks
Elements: `script`, `noscript`, `template`, `slot`.

- Default placement is the skeleton; keep localization content outside executable code.
- If a `<script>` tag contains user-facing strings, extract them separately (for example via JSON parsing) before they reach Markliff; we do not translate inline JavaScript.
- `noscript` blocks with fallback text become `<unit>` elements so the message is localizable, while the tag itself stays in the skeleton.
- Web component anchors (`template`, `slot`, and any custom-element name containing a hyphen) are preserved as either skeleton fragments or `<unit>` blocks with placeholders, depending on whether they contain textual fallback content. See `docs/512-prefs-html2.md` for the custom-element policy.

By combining these rules with the block and inline guidance in `docs/510-prefs-html0.md`, every HTML5 element now has an explicitly documented XLIFF representation.
