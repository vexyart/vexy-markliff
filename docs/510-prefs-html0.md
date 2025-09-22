
# 2. Expressing HTML elements in XLIFF by Vexy Markliff (1)

## 1. Structural elements

```
html, head, body, base, link, meta, noscript, script, style, template,
article, aside, details, dialog, fieldset, figure, footer, header, main,
menu, nav, section, div
```

In XLIFF, we express these elements using a skeleton file referenced in the `<file>` element.

**Example:**

```xml
<file id="f1" original="index.html">
  <skeleton href="skeleton/index.skl.html"/>
  <unit id="u1">
    <segment>
      <source>Welcome to our website</source>
    </segment>
  </unit>
</file>
```

The skeleton file (`skeleton/index.skl.html`) contains:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>###u1###</title>
  </head>
  <body>
    <header>###u2###</header>
    <main>###u3###</main>
    <footer>###u4###</footer>
  </body>
</html>
```

## 2. List elements

```
dl, ol, ul
```

In XLIFF, we express these elements using a `<group>` with the Format Style module to preserve list attributes.

**Example:**

```xml
<group id="g1" fs:fs="ul" fs:subFs="class,todo-list\id,main-list">
  <unit id="u1">
    <segment>
      <source>First list item</source>
    </segment>
  </unit>
  <unit id="u2">
    <segment>
      <source>Second list item</source>
    </segment>
  </unit>
</group>

<!-- Ordered list with start attribute -->
<group id="g2" fs:fs="ol" fs:subFs="start,5\type,A">
  <unit id="u3">
    <segment>
      <source>Item starting from 5</source>
    </segment>
  </unit>
</group>

<!-- Definition list -->
<group id="g3" fs:fs="dl">
  <unit id="u4" fs:fs="dt">
    <segment>
      <source>Term</source>
    </segment>
  </unit>
  <unit id="u5" fs:fs="dd">
    <segment>
      <source>Definition of the term</source>
    </segment>
  </unit>
</group>
```

## 3. Textual block elements

```
blockquote, caption, dd, dt, h1, h2, h3, h4, h5, h6, legend, li, p, pre,
title, address, figcaption, summary
```

In XLIFF, we express these elements using a `<unit>` with Format Style attributes.

**Examples:**

```xml
<!-- Heading with attributes -->
<unit id="u1" fs:fs="h1" fs:subFs="class,main-title\id,page-header">
  <segment>
    <source>Welcome to Our Service</source>
  </segment>
</unit>

<!-- Paragraph with inline elements and line break -->
<unit id="u2" fs:fs="p">
  <originalData>
    <data id="d1">&lt;br/&gt;</data>
  </originalData>
  <segment>
    <source>This is <mrk id="m1" fs:fs="strong">important</mrk> information.<ph id="ph1" dataRef="d1"/>
    Second line starts here.</source>
  </segment>
</unit>

<!-- Preformatted text preserving whitespace -->
<unit id="u3" fs:fs="pre" xml:space="preserve">
  <segment>
    <source>function hello() {
    console.log("Hello, World!");
}</source>
  </segment>
</unit>

<!-- Blockquote with citation -->
<unit id="u4" fs:fs="blockquote" fs:subFs="cite,https://example.com/quote">
  <segment>
    <source>The only way to do great work is to love what you do.</source>
  </segment>
</unit>
```

A `<unit>` contains one or more `<segment>` elements.

One segment may contain the entire content of a block element. However, our app should employ an additional step that: 

- If the HTML source contains a `<s>` element, we convert it into a single `<segment>`, and don’t split its content further. 
- If the HTML source contains a `<p>` element, we employ an intelligent sentence splitting algorithm that splits that `<p>` into multiple segments, one per sentence. 

### 3.1. 2.3 The `<s>` Element Strategy

When Markdown contains explicit `<s>` (sentence) elements:

```markdown
<s id="intro-1">This is the first sentence.</s> <s id="intro-2">This is the second.</s>
```

Convert each `<s>` to one XLIFF segment:

```xml
<segment id="intro-1" state="initial">
  <source>This is the first sentence.</source>
  <target>Dies ist der erste Satz.</target>
</segment>
<segment id="intro-2" state="initial">
  <source>This is the second.</source>
  <target>Dies ist der zweite.</target>
</segment>
```



## 4. Table elements

```
col, colgroup, table, tbody, tfoot, thead, tr, td, th
```

In XLIFF, we retain an HTML `<table>` verbatim as a single `<unit>` with `xml:space="preserve"`. We store the table's root attributes using Format Style attributes on the unit, and keep all internal structure intact.

**Examples:**

```xml
<!-- Simple table -->
<unit id="u1" fs:fs="table" fs:subFs="class,data-table\id,users" xml:space="preserve">
  <segment>
    <source><![CDATA[<table class="data-table" id="users">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John Doe</td>
      <td>john@example.com</td>
    </tr>
    <tr>
      <td>Jane Smith</td>
      <td>jane@example.com</td>
    </tr>
  </tbody>
</table>]]></source>
  </segment>
</unit>

<!-- Complex table with colspan/rowspan -->
<unit id="u2" fs:fs="table" fs:subFs="border,1\cellpadding,5" xml:space="preserve">
  <segment>
    <source><![CDATA[<table border="1" cellpadding="5">
  <caption>Sales Report</caption>
  <colgroup>
    <col style="background-color:#f0f0f0">
    <col span="2">
  </colgroup>
  <thead>
    <tr>
      <th rowspan="2">Product</th>
      <th colspan="2">Sales</th>
    </tr>
    <tr>
      <th>Q1</th>
      <th>Q2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Widget A</td>
      <td>$10,000</td>
      <td>$12,000</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td>Total</td>
      <td colspan="2">$22,000</td>
    </tr>
  </tfoot>
</table>]]></source>
  </segment>
</unit>
```

## 5. Inline elements with text content

```
a, b, button, cite, code, del, em, i, label, q, s, samp, small,
span, strike, strong, sub, sup, tt, u, abbr, bdi, bdo, data,
dfn, ins, kbd, mark, output, progress, ruby, rt, rp, time, var
```

In XLIFF, we express these elements containing text using `<mrk>` elements with Format Style attributes.

**Examples:**

```xml
<!-- Link with multiple attributes -->
<segment>
  <source>Visit our <mrk id="m1" fs:fs="a"
    fs:subFs="href,https://example.com\target,_blank\rel,noopener\class,external-link">
    homepage</mrk> for more info.</source>
</segment>

<!-- Nested inline elements -->
<segment>
  <source>This is <mrk id="m2" fs:fs="strong">very
    <mrk id="m3" fs:fs="em">important</mrk></mrk> text.</source>
</segment>

<!-- Button with attributes -->
<segment>
  <source><mrk id="m4" fs:fs="button"
    fs:subFs="type,submit\class,btn btn-primary\onclick,handleSubmit()">
    Submit Form</mrk></source>
</segment>

<!-- Time element with datetime -->
<segment>
  <source>Meeting at <mrk id="m5" fs:fs="time"
    fs:subFs="datetime,2024-01-15T14:30:00Z">2:30 PM</mrk></source>
</segment>

<!-- Abbreviation -->
<segment>
  <source>The <mrk id="m6" fs:fs="abbr"
    fs:subFs="title,World Wide Web">WWW</mrk> revolutionized communication.</source>
</segment>

<!-- Code with escaping -->
<segment>
  <source>Use <mrk id="m7" fs:fs="code">console.log("Hello\, World")</mrk> to debug.</source>
</segment>

<!-- Progress bar with value -->
<segment>
  <source>Download progress: <mrk id="m8" fs:fs="progress"
    fs:subFs="value,70\max,100">70%</mrk></source>
</segment>
```

