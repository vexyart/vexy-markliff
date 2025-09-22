# 4. Additional HTML-XLIFF rules by Vexy Markliff

## 1. Additional HTML5 Elements

### 1.1. Ruby Annotations (East Asian Text)

```
ruby, rt, rp, rb, rtc
```

Ruby annotations are preserved with their structure intact:

```xml
<!-- Ruby text with annotations -->
<unit id="u1">
  <segment>
    <source>The Japanese word <mrk id="m1" fs:fs="ruby">漢字<mrk id="m2" fs:fs="rt">かんじ</mrk></mrk> means Chinese characters.</source>
  </segment>
</unit>

<!-- Ruby with fallback parentheses -->
<unit id="u2" xml:space="preserve">
  <segment>
    <source><![CDATA[<ruby>
  漢 <rp>(</rp><rt>かん</rt><rp>)</rp>
  字 <rp>(</rp><rt>じ</rt><rp>)</rp>
</ruby>]]></source>
  </segment>
</unit>
```

### 1.2. Interactive Elements

```
details, summary, dialog, menu
```

Interactive elements are preserved as units or inline markers depending on context:

```xml
<!-- Details/summary element -->
<unit id="u1" fs:fs="details" fs:subFs="open," xml:space="preserve">
  <segment>
    <source><![CDATA[<details open>
  <summary>More information</summary>
  <p>This is the detailed content that can be toggled.</p>
</details>]]></source>
  </segment>
</unit>

<!-- Dialog element -->
<unit id="u2" fs:fs="dialog" fs:subFs="id,confirm-dialog" xml:space="preserve">
  <segment>
    <source><![CDATA[<dialog id="confirm-dialog">
  <p>Are you sure you want to proceed?</p>
  <button>Yes</button>
  <button>No</button>
</dialog>]]></source>
  </segment>
</unit>
```

### 1.3. Semantic Text Elements

```
bdi, bdo, data, dfn, kbd, mark, output, progress, time, var
```

These are handled as inline markers with Format Style:

```xml
<!-- Bidirectional text -->
<segment>
  <source>User <mrk id="m1" fs:fs="bdi">إيان</mrk> joined the chat.</source>
</segment>

<!-- Data element with machine-readable value -->
<segment>
  <source>Product code: <mrk id="m2" fs:fs="data" fs:subFs="value,ISBN-13-978-3-16-148410-0">978-3-16-148410-0</mrk></source>
</segment>
```

### 1.4. Obsolete but Still Encountered Elements

```
center, font, marquee, big, blink, strike, tt, acronym, applet, basefont, dir, frame, frameset, noframes, isindex
```

These deprecated elements are handled for backward compatibility:

```xml
<!-- Legacy formatting -->
<segment>
  <source><mrk id="m1" fs:fs="font" fs:subFs="color,red\size,+2">Important Notice</mrk></source>
</segment>

<!-- Legacy center element -->
<unit id="u1" fs:fs="center">
  <segment>
    <source>Centered content for legacy pages</source>
  </segment>
</unit>
```

## 2. Namespace Declarations

Always include necessary namespace declarations:

```xml
<xliff version="2.1"
       xmlns="urn:oasis:names:tc:xliff:document:2.0"
       xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"
       srcLang="en"
       trgLang="fr">
```

## 2. Escaping Rules

### 2.1. For `fs:subFs` attributes:

- `,` separates name from value
- `\` separates attribute pairs
- `\,` for literal comma
- `\\` for literal backslash
- Empty values: `controls,`

### 2.2. For originalData in CDATA:

- Use CDATA sections for complex HTML
- Or escape: `&lt;` for `<`, `&gt;` for `>`, `&amp;` for `&`

**Example:**

```xml
<originalData>
  <data id="d1">&lt;img src="C:\Images\photo.jpg" alt="A &quot;nice&quot; day"/&gt;</data>
  <!-- OR -->
  <data id="d2"><![CDATA[<img src="C:\Images\photo.jpg" alt="A "nice" day"/>]]></data>
</originalData>
```

## 3. Complete HTML5 Tag Reference Summary

### 3.1. Categorization by XLIFF Handling

| Category | Elements | XLIFF Method |
|----------|----------|---------------|
| **Structural** | html, head, body, base, link, meta, noscript, script, style, template, article, aside, details, dialog, fieldset, figure, footer, header, main, menu, nav, section, div | Skeleton file |
| **List Containers** | dl, ol, ul | `<group>` with fs:fs |
| **Text Blocks** | blockquote, caption, dd, dt, h1-h6, legend, li, p, pre, title, address, figcaption, summary | `<unit>` with fs:fs |
| **Inline Text** | a, b, button, cite, code, del, em, i, label, q, s, samp, small, span, strike, strong, sub, sup, tt, u, abbr, bdi, bdo, data, dfn, ins, kbd, mark, output, progress, ruby, rt, rp, time, var | `<mrk>` with fs:fs |
| **Self-closing** | br, hr, wbr, img, audio, video, canvas, embed, iframe, object, picture, map, area, source, track, col, base, link, meta, input, meter | `<ph>` with originalData |
| **Tables** | table, tbody, tfoot, thead, tr, td, th, col, colgroup | Preserve in `<unit>` with xml:space="preserve" |
| **Forms** | form, input, select, datalist, optgroup, option, textarea, label, button, output, fieldset, legend | Preserve in `<unit>` with xml:space="preserve" |
| **Media Complex** | audio, video (with source/track children) | Preserve in `<unit>` |
| **Web Components** | slot, template, custom elements | Preserve or `<ph>` based on complexity |

## 4. Complete Example

**XLIFF Extraction:**

```xml
<xliff version="2.1"
       xmlns="urn:oasis:names:tc:xliff:document:2.0"
       xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"
       srcLang="en" trgLang="fr">
  <file id="f1" original="review.html">
    <unit id="u1" fs:fs="h1">
      <segment>
        <source>Product Review</source>
      </segment>
    </unit>
    <unit id="u2" fs:fs="p">
      <originalData>
        <data id="d1">&lt;br/&gt;</data>
        <data id="d2">&lt;meter value="9" max="10"&gt;9 out of 10&lt;/meter&gt;</data>
      </originalData>
      <segment>
        <source>This is an <mrk id="m1" fs:fs="strong">excellent</mrk> product!<ph id="ph1" dataRef="d1"/>
        Rating: <ph id="ph2" dataRef="d2"/></source>
      </segment>
    </unit>
    <unit id="u3">
      <originalData>
        <data id="d3">&lt;img src="product.jpg" alt="Product photo"/&gt;</data>
      </originalData>
      <segment>
        <source><ph id="ph3" dataRef="d3"/></source>
      </segment>
    </unit>
    <unit id="u4" fs:fs="p">
      <segment>
        <source>Buy it <mrk id="m2" fs:fs="a" fs:subFs="href,/shop">here</mrk>.</source>
      </segment>
    </unit>
  </file>
</xliff>
```
