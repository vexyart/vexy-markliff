---
author: Unknown
date: '2023-01-01'
id: html-attributes-xliff
title: HTML Attributes in XLIFF
type: technical documentation
---

You express HTML attributes in XLIFF by using the standard **Metadata Module (`mda`)**. This module provides a flexible, key-value system to store non-translatable information, like attributes, and associate it with the correct block or inline element.

This approach keeps the translatable text clean while ensuring all data is preserved for perfect round-tripping.

## 🧱 Attributes on Block Elements (`<p>`, `<h1>`, `<blockquote>`)

A block-level HTML element maps to an XLIFF `<unit>`. You should store its attributes within an `<mda:metadata>` element inside that `<unit>`.

The process is:

1.  Create a `<unit>` for the HTML block.
2.  Inside the `<unit>`, add an `<mda:metadata>` block.
3.  Inside that, create an `<mda:metaGroup>` to hold all the attributes for that block.
4.  For each HTML attribute, add an `<mda:meta>` element. Use the `type` attribute for the attribute's name (e.g., `type="id"`, `type="class"`, `type="cite"`) and place the value inside the tag.

**Example:**

**Source HTML**

```html
<blockquote id="quote1" class="important" cite="http://example.com/source">
```

**Corresponding XLIFF**

```xml
<unit id="bq1">
  <mda:metadata>
    <mda:metaGroup category="html:attributes">
      <mda:meta type="id">quote1</mda:meta>
      <mda:meta type="class">important</mda:meta>
      <mda:meta type="cite">http://example.com/source</mda:meta>
    </mda:metaGroup>
  </mda:metadata>
  <segment>
    </segment>
</unit>
```

## 🔗 Attributes on Inline Elements (`<s>`, `<span>`)

An inline HTML element maps to an XLIFF inline code, typically `<pc>` (paired code). Since you cannot place metadata inside a `<segment>`, you store the attributes in the parent `<unit>`'s `<mda:metadata>` block and link them using the `<pc>` element's `id`.

The process is:

1.  Give the `<pc>` element a unique `id` within the unit (e.g., `id="c1"`).
2.  In the `<unit>`'s `<mda:metadata>` block, add `<mda:meta>` elements for each attribute.
3.  For the `type` of each meta tag, use a convention like **`[code_id]:[attribute_name]`** (e.g., `type="c1:id"`, `type="c1:title"`). This creates an unambiguous link between the metadata and the specific inline code.

**Example:**

**Source HTML**

```html
<p>Please review the <span class="doc-ref" data-version="2.1" title="Click to view">document</span>.</p>
```

**Corresponding XLIFF**

```xml
<unit id="p1">
  <mda:metadata>
    <mda:metaGroup category="html:inline-attributes">
      <mda:meta type="c1:class">doc-ref</mda:meta>
      <mda:meta type="c1:data-version">2.1</mda:meta>
      <mda:meta type="c1:title">Click to view</mda:meta>
    </mda:metaGroup>
  </mda:metadata>
  <segment>
    <source>Please review the <pc id="c1" dataRefStart="span-start" dataRefEnd="span-end">document</pc>.</source>
    <target>Bitte überprüfen Sie das <pc id="c1" dataRefStart="span-start" dataRefEnd="span-end">Dokument</pc>.</target>
  </segment>
  <originalData>
    <data id="span-start">&lt;span&gt;</data> <data id="span-end">&lt;/span&gt;</data>
  </originalData>
</unit>
```

In this example, `c1:class` clearly indicates that it is the `class` attribute for the `<pc>` element with `id="c1"`.

## ✅ Complete Annotated Example

This example combines both block and inline attributes.

**Source HTML**

```html
<p id="p-10" class="legal-notice">
  This is a <s id="s-final" data-ref="x-987">final</s> statement.
</p>
```

**Resulting XLIFF 2.1**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.1"
       xmlns:mda="urn:oasis:names:tc:xliff:metadata:2.0"
       version="2.1" srcLang="en" trgLang="de">
  <file id="f1">
    <unit id="unit1" name="paragraph">
      <mda:metadata>
        <mda:metaGroup category="html:attributes">
          <mda:meta type="id">p-10</mda:meta>
          <mda:meta type="class">legal-notice</mda:meta>
        </mda:metaGroup>
        <mda:metaGroup category="html:inline-attributes">
          <mda:meta type="c1:id">s-final</mda:meta>
          <mda:meta type="c1:data-ref">x-987</mda:meta>
        </mda:metaGroup>
      </mda:metadata>

      <segment>
        <source>This is a <pc id="c1" dataRefStart="s-start" dataRefEnd="s-end">final</pc> statement.</source>
        <target>Dies ist eine <pc id="c1" dataRefStart="s-start" dataRefEnd="s-end">endgültige</pc> Aussage.</target>
      </segment>
      
      <originalData>
        <data id="s-start">&lt;s&gt;</data>
        <data id="s-end">&lt;/s&gt;</data>
      </originalData>
    </unit>
  </file>
</xliff>
```