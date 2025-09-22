
---

<unit id="1">
  <segment>
    <source><sc id="1" type="fmt" subType="xlf:b"/>
        First sentence. </source>
  </segment>
  <segment>
    <source>Second sentence.<ec startRef="1" type="fmt"
        subType="xlf:b"/></source>
  </segment>
</unit>

The following XLIFF Module attributes are explicitly allowed by the wildcard other:

- attributes from the namespace urn:oasis:names:tc:xliff:fs:2.0, OPTIONAL, provided that the Constraints specified in the Format Style Module are met.
- attributes from the namespace urn:oasis:names:tc:xliff:sizerestriction:2.0, OPTIONAL, provided that the Constraints specified in the Size and Length Restriction Module are met.


5.3.4 Module Specification
Format Style module consists of just two attributes: fs and subFs. It does not specify any elements.

Format Style allows most structural and inline XLIFF core elements to convey basic formatting information using a predefined subset of HTML formatting elements. It primarily enables the generation of HTML pages or snippets for preview and review purposes. It MUST NOT be used to prescribe a roundtrip to a source document format.

The fs attribute holds the name of an HTML formatting element. If additional style information is needed, the OPTIONAL subFs attribute is provided.

Constraints

The Format Style attributes MUST be configured in such a way that the HTML [HTML5] snippet resulting at the <file> level is valid.

Processing Requirements

Extractors and Enrichers SHOULD use the following method to validate their HTML snippets:

Parse the snippet with the [HTML5] fragment parsing algorithm, see http://www.w3.org/TR/html5/syntax.html#parsing-html-fragments.

the result MUST be a valid DOM tree as per [HTML5], see http://www.w3.org/TR/html5/infrastructure.html#tree-order.

Note
The above constraint and validation method will make sure that the snippets are renderable by standard HTML browsers.

5.3.5 Module Attributes
The attributes defined in the Format Style module are: fs, subFs.

5.3.5.1 fs
Format style attribute, fs - allows most structural and inline XLIFF core elements to convey basic formatting information using a predefined subset of HTML formatting elements (for example, HTML elements names like <script> are not included). It enables the generation of HTML pages or snippets for preview and review purposes. If additional style information is needed, the OPTIONAL subFs attribute is provided.

Value description:

Table 4. Values

a anchor
b bold text style
bdo I18N BiDi over-ride
big large text style
blockquote  long quotation
body  document body
br  forced line break
button  push button
caption table caption
center  shorthand for DIV align=center
cite  citation
code  computer code fragment
col table column
colgroup  table column group
dd  definition description
del deleted text
div generic language/style container
dl  definition list
dt  definition term
em  emphasis
h1  heading
h2  heading
h3  heading
h4  heading
h5  heading
h6  heading
head  document head
hr  horizontal rule
html  document root element
i italic text style
img image
label form field label text
legend  fieldset legend
li  list item
ol  ordered list
p paragraph
pre preformatted text
q short inline quotation
s strike-through text style
samp  sample program output, scripts, etc.
select  option selector
small small text style
span  generic language/style container
strike  strike-through text
strong  strong emphasis
sub subscript
sup superscript
table 
tbody table body
td  table data cell
tfoot table footer
th  table header cell
thead table header
title document title
tr  table row
tt  teletype or monospaced text style
u underlined text style
ul  unordered list

Default value: undefined.

Used in: <file>, <unit>, <note>, <sc>, <ec>, <ph>, <pc>, <mrk>, and <sm>.

Warning
The fs attribute is not intended to facilitate Merging back into the original format.

Constraints

The fs MUST only be used with <ec> in cases where the isolated attribute is set to 'yes'.

Processing Requirements

Writers updating the attribute fs MUST also update or delete subFs.

Example: To facilitate HTML preview, fs can be applied to XLIFF like this like:

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
With an XSL stylesheet like this:

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
You can generate a an HTML page like this:

<html>
  <p>Mick Jones renewed his interest in the Vintage <strong>'72
      Telecaster Thinline </strong> guitar. <br/>He says <q>I love 'em
      </q><img src="smileface.png"/></p>
</html>
5.3.5.2 subFs
Sub-format style, subFs - allows extra metadata, like URL for example, to be added in concert with the fs attribute.

Value description: The subFs attribute is used to specify the HTML attributes to use along with the HTML element declared in the fs attribute. It is a list of name/value pairs. Each pair is separated from the next with a backslash (\). The name and the value of a pair are separated with a comma (,). Both literal backslash and comma characters are escaped with a backslash prefix.

Default value: undefined.

Used in: <file>, <unit>, <note>, <source>, <target>, <sc>, <ec>, <ph>, <pc>, <mrk>, and <sm>.

Warning
The subFs attribute is not intended to facilitate Merging back into the original format.

Constraints

Commas (,) and backslashes (\) in the value parts of the subFs MUST be escaped with a backslash (\).

If the attribute subFs is used, the attribute fs MUST be specified as well.

The subFs MUST only be used with <ec> in cases where the isolated attribute is set to 'yes'.

Processing Requirements

Writers updating the attribute fs MUST also update or delete subFs.

Example: For complex HTML previews that require more than one attribute on an HTML preview element, attribute pairs are separated by backslashes (\). Any literal comma or backslash in an attribute value MUST be escaped with a backslash.

For example, we would use this convention:

<ph id="p1" fs="img" subFs="src,c:\\docs\\images\\smile.png\alt,
    My Happy Smile\title,Smiling faces\, are nice" />
To produce this HTML preview:

<img src="c:\docs\images\smile.png" alt="My Happy Smile" title="Smiling
    faces, are nice" />




<unit id="1">
  <segment>
    <source>First sentence.</source>
    <target>Première phrase.</target>
  </segment>
  <ignorable>
    <source> </source>
  </ignorable>
  <segment>
    <source>Second sentence.</source>
  </segment>
</unit>


::: warning
*here be dragons*
:::
.... and specify how they should be rendered. If no renderer defined, <div> with container name class will be created:

<div class="warning">
<em>here be dragons</em>
</div>


Markdown "containers" are emerging as an increasingly popular extension: 

```markdown
:::: class1
::: class2
*text*
:::
::::
```

becomes

```html
<div class="class1">
<div class="class2">
<em>text</em>
</div>
</div>
```

- https://www.npmjs.com/package/markdown-it-container (JS)
- https://mdit-py-plugins.readthedocs.io/en/latest/#containers (Py)






----



You're absolutely right to point that out! According to the OASIS spec, `fs` **is** allowed as an attribute of `<mrk>`, but it **must be prefixed with a namespace**. 

Looking at the documentation:

1. **The `fs` attribute is explicitly allowed on `<mrk>`**:
   - The Format Style Module states: "Used in: `<file>`, `<unit>`, `<note>`, `<sc>`, `<ec>`, `<ph>`, `<pc>`, **`<mrk>`**, and `<sm>`"

2. **But it requires namespace prefixing**:
   - The Format Style Module is in the namespace `urn:oasis:names:tc:xliff:fs:2.0`
   - The core `<mrk>` element specification states: "attributes from the namespace `urn:oasis:names:tc:xliff:fs:2.0`, OPTIONAL, provided that the Constraints specified in the Format Style Module are met"

So combining both `<mrk>` with Format Style attributes would look like this:

```xml
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.1" 
       xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"
       version="2.1" srcLang="en" trgLang="de">
  <file id="f1">
    <unit id="u1">
      <segment>
        <source>
          This is 
          <mrk id="m1" fs:fs="strong">important</mrk> 
          and 
          <mrk id="m2" fs:fs="em">emphasized</mrk> 
          text with 
          <mrk id="m3" fs:fs="a" 
               fs:subFs="href,https://example.com\title,Click here">a link</mrk>.
        </source>
      </segment>
    </unit>
  </file>
</xliff>
```

This gives us a powerful combination where:
- **`type` attribute** (core XLIFF) can indicate the semantic purpose (`term`, `comment`, or custom values)
- **`fs:fs` attribute** (Format Style module) can indicate the HTML formatting element
- **`fs:subFs` attribute** can provide additional HTML attributes
- **`value` attribute** (core XLIFF) can store original markup syntax
- **`ref` attribute** (core XLIFF) can store URIs

So for a universal markup preservation system, you could use:
- `fs:fs` + `fs:subFs` for HTML-based preview/rendering
- `type` with custom prefixes for semantic classification
- `value` for preserving original non-HTML markup (Markdown, LaTeX, etc.)

This approach would be fully spec-compliant and provide maximum flexibility for handling various markup formats!


