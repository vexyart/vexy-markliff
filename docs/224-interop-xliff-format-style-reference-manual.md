---
author: OASIS XLIFF TC
date: '2023'
id: 5.3.5.1-5.3.5.2
title: XLIFF fs and subFs Attributes
type: Technical Documentation
---

```markdown
# XLIFF fs and subFs Attributes

## 5.3.5.1 fs

Format style attribute, fs - allows most structural and inline XLIFF core elements to convey basic formatting information using a predefined subset of HTML formatting elements (for example, HTML elements names like `<script>` are not included). It enables the generation of HTML pages or snippets for preview and review purposes. If additional style information is needed, the OPTIONAL subFs attribute is provided.

### Value description:

| Value | Description |
|-------|-------------|
| a | anchor |
| b | bold text style |
| bdo | I18N BiDi over-ride |
| big | large text style |
| blockquote | long quotation |
| body | document body |
| br | forced line break |
| button | push button |
| caption | table caption |
| center | shorthand for DIV align=center |
| cite | citation |
| code | computer code fragment |
| col | table column |
| colgroup | table column group |
| dd | definition description |
| del | deleted text |
| div | generic language/style container |
| dl | definition list |
| dt | definition term |
| em | emphasis |
| h1 | heading |
| h2 | heading |
| h3 | heading |
| h4 | heading |
| h5 | heading |
| h6 | heading |
| head | document head |
| hr | horizontal rule |
| html | document root element |
| i | italic text style |
| img | image |
| label | form field label text |
| legend | fieldset legend |
| li | list item |
| ol | ordered list |
| p | paragraph |
| pre | preformatted text |
| q | short inline quotation |
| s | strike-through text style |
| samp | sample program output, scripts, etc. |
| select | option selector |
| small | small text style |
| span | generic language/style container |
| strike | strike-through text |
| strong | strong emphasis |
| sub | subscript |
| sup | superscript |
| table |  |
| tbody | table body |
| td | table data cell |
| tfoot | table footer |
| th | table header cell |
| thead | table header |
| title | document title |
| tr | table row |
| tt | teletype or monospaced text style |
| u | underlined text style |
| ul | unordered list |

**Default value:** undefined.

**Used in:** `<file>`, `<unit>`, `<note>`, `<sc>`, `<ec>`, `<ph>`, `<pc>`, `<mrk>`, and `<sm>`.

### Warning
The fs attribute is not intended to facilitate Merging back into the original format.

### Constraints
The fs MUST only be used with `<ec>` in cases where the isolated attribute is set to 'yes'.

### Processing Requirements
Writers updating the attribute fs MUST also update or delete subFs.

### Example
To facilitate HTML preview, fs can be applied to XLIFF like this:

```xml
<xliff xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0">
  <file fs:fs="html">
    <unit id="1" fs:fs="p">
      <segment>
        <source>Mick Jones renewed his interest in the Vintage <pc id="1"
            fs:fs="strong">'72 Telecaster Thinline </pc> guitar.
            <ph id="ph2" fs:fs="br" />He says <pc fs:fs="q">I love 'em
            </pc><ph id="ph1" fs:fs="img"
            fs:subFs="src,smileface.png" /></source>
      </segment>
    </unit>
  </file>
</xliff>
```

With an XSL stylesheet like this:

```xsl
<xsl:template match="*" priority="2"
    xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0">
  <xsl:choose>
    <xsl:when test="@fs:fs">
      <xsl:element name="{@fs:fs}">
        <xsl:if test="@fs:subFs">
          <xsl:variable name="att_name"
              select="substring-before(@fs:subFs,',')" />
          <xsl:variable name="att_val"
              select="substring-after(@fs:subFs,',')" />
          <xsl:attribute name="{$att_name}">
            <xsl:value-of select="$att_val" />
          </xsl:attribute>
        </xsl:if>
        <xsl:apply-templates />
      </xsl:element>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates />
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>
```

You can generate an HTML page like this:

```html
<html>
  <p>Mick Jones renewed his interest in the Vintage <strong>'72
      Telecaster Thinline </strong> guitar. <br/>He says <q>I love 'em
      </q><img src="smileface.png"/></p>
</html>
```

## 5.3.5.2 subFs

Sub-format style, subFs - allows extra metadata, like URL for example, to be added in concert with the fs attribute.

### Value description
The subFs attribute is used to specify the HTML attributes to use along with the HTML element declared in the fs attribute. It is a list of name/value pairs. Each pair is separated from the next with a backslash (`\`). The name and the value of a pair are separated with a comma (`,`). Both literal backslash and comma characters are escaped with a backslash prefix.

**Default value:** undefined.

**Used in:** `<file>`, `<unit>`, `<note>`, `<source>`, `<target>`, `<sc>`, `<ec>`, `<ph>`, `<pc>`, `<mrk>`, and `<sm>`.

### Warning
The subFs attribute is not intended to facilitate Merging back into the original format.

### Constraints
- Commas (`,`) and backslashes (`\`) in the value parts of the subFs MUST be escaped with a backslash (`\`).
- If the attribute subFs is used, the attribute fs MUST be specified as well.
- The subFs MUST only be used with `<ec>` in cases where the isolated attribute is