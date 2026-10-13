# HTML mapping rules

!!! warning "Specification"
    These rules describe the planned extractor. Version 1.3 extracts plain text nodes only; see [XLIFF output](../output-format.md).

The rules decide, for every HTML5 element, whether it stays in the skeleton, becomes a `<unit>` or `<group>`, becomes an inline `<mrk>`, or becomes a `<ph>` placeholder. All of them rely on the Format Style attributes `fs:fs` and `fs:subFs` to remember the original element and its attributes.

## Namespaces

Every generated `<xliff>` root declares:

```xml
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.0"
       xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"
       version="2.1" srcLang="en" trgLang="de">
```

## Attribute encoding in `fs:subFs`

HTML attributes are stored as name/value pairs:

- `,` separates a name from its value: `href,https://example.com`.
- `\` separates pairs: `class,hero\id,lead`.
- A literal comma is written `\,`; a literal backslash `\\`.
- An empty value is written `name,`.

So `<a href="https://example.com" target="_blank">` becomes `fs:fs="a" fs:subFs="href,https://example.com\target,_blank"`.

Verbatim HTML fragments go into `<originalData><data id="…">…</data></originalData>`, as CDATA where the fragment contains `<` or `&`, to avoid double escaping.

## Document skeleton

Elements: `<!DOCTYPE>`, `html`, `head`, `body`, `base`, `link`, `meta`, `script`, `style`, `noscript`, `template`.

These stay in the skeleton file referenced by `<file><skeleton href="…"/>`. Placeholders such as `###u17###` mark where units go back in. Only text inside child elements described below (for example `<title>`) is promoted to units.

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

## Sectioning and grouping

Elements: `article`, `aside`, `details`, `dialog`, `div`, `fieldset`, `figure`, `figcaption`, `footer`, `header`, `main`, `menu`, `nav`, `section`, `summary`.

- Wrap each section in a `<group>` or `<unit>` with `fs:fs` set to the element name and attributes in `fs:subFs`.
- Keep purely structural wrappers (a `<div>` that holds only blocks) in the skeleton and promote only the child blocks.
- Promote text-bearing elements (`figcaption`, `summary`, `dialog`) to units.

```xml
<group id="nav" fs:fs="nav" fs:subFs="class,main-menu">
  <unit id="nav-title" fs:fs="h2">
    <segment><source>Site navigation</source></segment>
  </unit>
</group>
```

## Lists

Elements: `ul`, `ol`, `li`, `menu`, `dl`, `dt`, `dd`.

- Each list container becomes a `<group>` with `fs:fs` set to the container element.
- Each `li`, `dt` and `dd` becomes a child `<unit>`.
- List attributes (`start`, `type`, `reversed`, `value`) go into `fs:subFs`.
- Nested lists become nested groups.

```xml
<group id="faq" fs:fs="dl">
  <unit id="q1" fs:fs="dt"><segment><source>What is Markliff?</source></segment></unit>
  <unit id="a1" fs:fs="dd"><segment><source>It is our HTML to XLIFF bridge.</source></segment></unit>
</group>
```

## Tables

Elements: `table`, `caption`, `colgroup`, `col`, `thead`, `tbody`, `tfoot`, `tr`, `th`, `td`.

- By default keep the whole table in one `<unit fs:fs="table" xml:space="preserve">`, with table attributes in `fs:subFs`.
- When cells must be translated one by one, break the table into child units and keep the outer markup in `<originalData>`.

```xml
<unit id="pricing" fs:fs="table" fs:subFs="class,pricing" xml:space="preserve">
  <segment>
    <source><![CDATA[<table class="pricing"><thead><tr><th>Plan</th><th>Price</th></tr></thead>
    <tbody><tr><td>Starter</td><td>$9</td></tr></tbody></table>]]></source>
  </segment>
</unit>
```

## Text blocks and headings

Elements: `address`, `blockquote`, `caption`, `h1`–`h6`, `hgroup`, `legend`, `p`, `pre`, `title`.

- Each becomes a `<unit>` with `fs:fs` set to the element name.
- `pre` gets `xml:space="preserve"`.
- `title` text is a unit; its position is a skeleton placeholder.
- `hgroup` becomes a `<group fs:fs="hgroup">` around its heading units.

Segmentation inside these units:

- An `<s>` element is one `<segment>` and is never split.
- A `<p>` is split into sentences, one `<segment>` per sentence. See [Sentence segmentation](segmentation.md).
- Other blocks are one segment unless the HTML already carries `<s>` elements.

## Inline text semantics

Elements: `a`, `abbr`, `b`, `bdi`, `bdo`, `cite`, `code`, `data`, `del`, `dfn`, `em`, `i`, `ins`, `kbd`, `label`, `mark`, `output`, `q`, `ruby`, `rb`, `rp`, `rt`, `rtc`, `s`, `samp`, `small`, `span`, `strong`, `sub`, `sup`, `time`, `u`, `var`.

- Each becomes a `<mrk>` inside the surrounding segment, with `fs:fs` set to the element and its attributes (`href`, `datetime`, `title`, `aria-*` and so on) in `fs:subFs`.
- Nesting is kept as it appears; the merger replays it.
- `ins` and `del` keep change metadata such as `datetime`.
- `ruby`, `rb`, `rt`, `rp` and `rtc` stay grouped so that ruby layout can be rebuilt.
- `lang`, `dir` and `translate` stay on the marker. `bdi` and `bdo` always keep `dir`; if it is absent, record `dir,auto`.

```xml
<segment>
  <source>View the <mrk id="m1" fs:fs="a" fs:subFs="href,https://example.com\target,_blank">documentation</mrk>
    updated on <mrk id="m2" fs:fs="time" fs:subFs="datetime,2024-05-12">May 12</mrk>.</source>
</segment>
```

## Void elements and placeholders

Elements: `area`, `base`, `br`, `col`, `embed`, `hr`, `img`, `input`, `link`, `meta`, `param`, `source`, `track`, `wbr`.

- Each occurrence becomes `<ph>` with `dataRef` pointing to an `<originalData>` entry that holds the literal HTML.
- `base`, `link` and `meta` normally stay in the skeleton; the placeholder rule covers them when they appear in mixed content, for example raw HTML in Markdown.
- Placeholder ids are deterministic (for example `ph-img-001`) so that the merger can match them.

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

## Embedded media

Elements: `audio`, `video`, `canvas`, `iframe`, `map`, `object`, `picture`, `svg`, `math`, and their children `area`, `source`, `track`, `param`.

- Self-contained widgets (`iframe`, `canvas`, `object`, `svg`, `math`) are stored whole in a `<unit xml:space="preserve">`. SVG and MathML internals are never rewritten.
- `picture` is a unit; its `source` children are `<originalData>` entries.
- `map` is a unit; each `area` is a placeholder inside it.
- `audio` and `video` mirror their nesting: `source` and `track` become placeholders, transcripts become child units.

```xml
<unit id="product-video" fs:fs="video" fs:subFs="controls,\width,640" xml:space="preserve">
  <originalData>
    <data id="src-main">&lt;source src="promo.mp4" type="video/mp4"/&gt;</data>
    <data id="trk-en">&lt;track kind="subtitles" src="promo-en.vtt" srclang="en" label="English" default&gt;</data>
  </originalData>
  <segment>
    <source><ph id="ph-src1" dataRef="src-main"/><ph id="ph-trk1" dataRef="trk-en"/></source>
  </segment>
</unit>
```

## Forms

Elements: `form`, `button`, `datalist`, `fieldset`, `input`, `label`, `legend`, `meter`, `optgroup`, `option`, `output`, `progress`, `select`, `textarea`.

- A whole form is kept as one `<unit xml:space="preserve">` so that validation attributes survive.
- Visible text inside it (`label`, button captions, `option` text) becomes separate units referenced by placeholders.
- Void controls (`input`, `meter`, `progress`) are placeholders inside the form unit.
- Markdown task-list checkboxes use the same placeholder rule.

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

## Scripts, templates and custom elements

- `script` stays in the skeleton. Inline JavaScript is not translated; extract user-facing strings from it (for example from JSON) before conversion.
- `noscript` fallback text becomes a unit; the tag stays in the skeleton.
- `template` stays in the skeleton unless it contains fallback text, which is then promoted.
- `slot` and `slot="…"` are recorded in `fs:subFs`; fallback text in slots is ordinary inline content.
- Custom elements (any name with a hyphen, such as `app-shell` or `geo-map`) are treated as inline or block elements depending on their content, with the literal tag name in `fs:fs`.

## Deprecated elements

`acronym`, `applet`, `basefont`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `marquee`, `menuitem`, `noframes`, `strike` and `tt` are kept as written and handled like their modern counterparts (for example `center` like `div`). Their visible text is still extracted.

## Attributes that matter for localization

Most attributes are carried through `fs:subFs` untouched. A few carry text or localization instructions:

| Attribute | Relevance |
|---|---|
| `lang` | Language of the content (BCP 47 tag); must change in the target |
| `dir` | `ltr`, `rtl` or `auto`; matters for mixed-direction text |
| `translate` | `yes` or `no`; maps to ITS Translate |
| `title` | Tooltip text, often the expansion of an `<abbr>`; translatable |
| `alt` | Text alternative of an image; translatable |
| `aria-label`, `aria-describedby`, `aria-labelledby` | Accessible names and descriptions; `aria-label` is translatable text |
| `cite`, `datetime` | On `blockquote`, `q`, `del`, `ins`: source URL and ISO 8601 time |
| `data-*` | Script data; not translatable |

## Element reference

| Elements | Handling |
|---|---|
| `<!DOCTYPE>`, `html`, `head`, `body` | Skeleton; child text promoted to units |
| `base`, `link`, `meta` | Skeleton; inline occurrences become `<ph>` |
| `title` | Unit `fs:fs="title"`, placeholder in skeleton |
| `style`, `script` | Skeleton only |
| `noscript`, `template` | Skeleton; fallback text promoted |
| `article`, `aside`, `main`, `nav`, `section` | Group or unit with `fs:fs` and attributes |
| `header`, `footer`, `div` | Skeleton wrapper; text children promoted |
| `figure`, `figcaption` | Figure as group or unit; caption as unit |
| `details`, `summary`, `dialog` | Block kept with `fs:fs`; text children as units |
| `fieldset`, `legend` | Fieldset as group; legend as unit |
| `menu`, `ul`, `ol`, `li` | List group and item units |
| `dl`, `dt`, `dd` | Definition-list group, term and definition units |
| `p`, `address`, `blockquote`, `pre`, `caption` | Units; paragraphs split into sentences |
| `h1`–`h6`, `hgroup` | Units; `hgroup` as wrapping group |
| `span`, `mark`, `strong`, `em`, `i`, `b`, `u`, `small`, `s` | `<mrk>` |
| `cite`, `q`, `dfn`, `abbr`, `var`, `code`, `kbd`, `samp` | `<mrk>` |
| `time`, `data`, `output`, `label` | `<mrk>` with value attributes |
| `sub`, `sup`, `bdi`, `bdo`, `ruby`, `rb`, `rt`, `rp`, `rtc` | `<mrk>` with direction and ruby data |
| `del`, `ins` | `<mrk>` with change metadata |
| `hr`, `br`, `wbr` | `<ph>` |
| `table` and its parts | Preserved unit, or nested groups for cell-level work |
| `colgroup`, `col` | Inside the preserved table markup |
| `form` | Preserved unit; text children as units |
| `button` | Unit |
| `input`, `textarea`, `select`, `meter`, `progress` | Placeholders inside the form unit |
| `option`, `optgroup`, `datalist` | Units for visible captions |
| `img`, `picture`, `source`, `track` | `<ph>` inside media units |
| `audio`, `video` | Units; sources and tracks as placeholders |
| `map`, `area` | Map as unit; areas as placeholders |
| `iframe`, `embed`, `object`, `param` | Unit with full markup |
| `canvas`, `svg`, `math` | Preserved unit; internals untouched |
| `slot`, custom elements | Structure kept; fallback text promoted; tag name in `fs:fs` |

## Validation checklist

- Every unit created from HTML has `fs:fs` matching the original element.
- Every `<ph>` refers to an existing `<data id="…">`.
- Each `<s>` maps to exactly one `<segment>`; paragraphs are sentence-split.
- When in doubt, check against the OASIS XLIFF 2.1 specification.
