# 3. Expressing HTML elements in XLIFF by Vexy Markliff (2)

## 1. Self-closing and non-localizable inline elements

```
br, hr, wbr, img, audio, video, canvas, embed, iframe, object,
picture, map, area, source, track, col, base, link, meta,
input (standalone), meter, script, style, noscript
```

In XLIFF, we express these elements using `<ph>` (placeholder) elements with `originalData`.

**Examples:**

```xml
<!-- Paragraph with line breaks and horizontal rule -->
<unit id="u1" fs:fs="p">
  <originalData>
    <data id="d1">&lt;br/&gt;</data>
    <data id="d2">&lt;hr class="section-divider"/&gt;</data>
  </originalData>
  <segment>
    <source>First line<ph id="ph1" dataRef="d1"/>
    Second line<ph id="ph2" dataRef="d1"/>
    Third line<ph id="ph3" dataRef="d2"/>
    New section starts here.</source>
  </segment>
</unit>

<!-- Text with images -->
<unit id="u2">
  <originalData>
    <data id="d1">&lt;img src="/images/logo.png" alt="Company Logo" width="200" height="50"/&gt;</data>
    <data id="d2">&lt;img src="/images/icon.svg" alt="Icon" class="inline-icon"/&gt;</data>
  </originalData>
  <segment>
    <source><ph id="ph1" dataRef="d1"/> Welcome to our site. Click the <ph id="ph2" dataRef="d2"/> icon for help.</source>
  </segment>
</unit>

<!-- Word break opportunities -->
<unit id="u3">
  <originalData>
    <data id="d1">&lt;wbr/&gt;</data>
  </originalData>
  <segment>
    <source>Super<ph id="ph1" dataRef="d1"/>califragilistic<ph id="ph2" dataRef="d1"/>expialidocious</source>
  </segment>
</unit>

<!-- Embedded media -->
<unit id="u4">
  <originalData>
    <data id="d1">&lt;video src="intro.mp4" controls width="640" height="360" poster="poster.jpg"&gt;&lt;/video&gt;</data>
    <data id="d2">&lt;audio src="podcast.mp3" controls&gt;&lt;/audio&gt;</data>
  </originalData>
  <segment>
    <source>Watch our introduction video: <ph id="ph1" dataRef="d1"/>
    Listen to the podcast: <ph id="ph2" dataRef="d2"/></source>
  </segment>
</unit>

<!-- Iframe embed -->
<unit id="u5">
  <originalData>
    <data id="d1">&lt;iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" width="560" height="315" frameborder="0" allowfullscreen&gt;&lt;/iframe&gt;</data>
  </originalData>
  <segment>
    <source>Check out this video: <ph id="ph1" dataRef="d1"/></source>
  </segment>
</unit>

<!-- Script and style elements -->
<unit id="u6">
  <originalData>
    <data id="d1">&lt;script src="/js/analytics.js" async&gt;&lt;/script&gt;</data>
    <data id="d2">&lt;style&gt;.highlight { background: yellow; }&lt;/style&gt;</data>
    <data id="d3">&lt;noscript&gt;Please enable JavaScript&lt;/noscript&gt;</data>
  </originalData>
  <segment>
    <source><ph id="ph1" dataRef="d1"/><ph id="ph2" dataRef="d2"/>Content here<ph id="ph3" dataRef="d3"/></source>
  </segment>
</unit>

<!-- Canvas and meter -->
<unit id="u7">
  <originalData>
    <data id="d1">&lt;canvas id="myCanvas" width="300" height="150"&gt;&lt;/canvas&gt;</data>
    <data id="d2">&lt;meter value="6" min="0" max="10"&gt;6 out of 10&lt;/meter&gt;</data>
  </originalData>
  <segment>
    <source>Drawing area: <ph id="ph1" dataRef="d1"/> Score: <ph id="ph2" dataRef="d2"/></source>
  </segment>
</unit>

<!-- Picture element with sources -->
<unit id="u8">
  <originalData>
    <data id="d1">&lt;picture&gt;
  &lt;source media="(min-width:650px)" srcset="img_large.jpg"&gt;
  &lt;source media="(min-width:465px)" srcset="img_medium.jpg"&gt;
  &lt;img src="img_small.jpg" alt="Responsive image"&gt;
&lt;/picture&gt;</data>
  </originalData>
  <segment>
    <source>Product image: <ph id="ph1" dataRef="d1"/></source>
  </segment>
</unit>
```

## 2. Form elements

```
form, input, select, datalist, optgroup, option, textarea
```

Also `label, output, button` if inside a `form`

Forms are retained verbatim as a single `<unit>` with `xml:space="preserve"`. Standalone form inputs are wrapped in a form first.

**Examples:**

```xml
<!-- Complete form -->
<unit id="u1" fs:fs="form" fs:subFs="action,/submit\method,POST\id,contact-form" xml:space="preserve">
  <segment>
    <source><![CDATA[<form action="/submit" method="POST" id="contact-form">
  <div class="form-group">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
  </div>
  <div class="form-group">
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
  </div>
  <div class="form-group">
    <label for="country">Country:</label>
    <select id="country" name="country">
      <option value="">Select a country</option>
      <optgroup label="Europe">
        <option value="fr">France</option>
        <option value="de">Germany</option>
      </optgroup>
      <optgroup label="Americas">
        <option value="us">United States</option>
        <option value="ca">Canada</option>
      </optgroup>
    </select>
  </div>
  <div class="form-group">
    <label for="browser">Browser:</label>
    <input list="browsers" id="browser" name="browser">
    <datalist id="browsers">
      <option value="Chrome">
      <option value="Firefox">
      <option value="Safari">
      <option value="Edge">
    </datalist>
  </div>
  <div class="form-group">
    <label for="message">Message:</label>
    <textarea id="message" name="message" rows="4" cols="50"></textarea>
  </div>
  <button type="submit">Submit</button>
  <output id="result"></output>
</form>]]></source>
  </segment>
</unit>

<!-- Standalone input elements (not in a form) get treated as placeholders -->
<unit id="u2">
  <originalData>
    <data id="d1">&lt;input type="search" placeholder="Search..." name="q"&gt;</data>
    <data id="d2">&lt;input type="checkbox" id="agree" name="agree" value="yes"&gt;</data>
  </originalData>
  <segment>
    <source>Search box: <ph id="ph1" dataRef="d1"/>
    <ph id="ph2" dataRef="d2"/> I agree to the terms</source>
  </segment>
</unit>

<!-- Mixed content with form elements -->
<unit id="u3">
  <originalData>
    <data id="d1">&lt;input type="submit" value="Send"&gt;</data>
  </originalData>
  <segment>
    <source>Click here to submit: <ph id="ph1" dataRef="d1"/></source>
  </segment>
</unit>
```

## 3. Media elements with tracks

```
audio, video (with source and track children)
```

Media elements with multiple sources and tracks are preserved as complete units.

**Examples:**

```xml
<!-- Video with tracks - preserved as unit -->
<unit id="u1" fs:fs="video" fs:subFs="controls,\width,640\height,360" xml:space="preserve">
  <segment>
    <source><![CDATA[<video controls width="640" height="360">
  <source src="movie.mp4" type="video/mp4">
  <source src="movie.webm" type="video/webm">
  <track kind="captions" src="captions_en.vtt" srclang="en" label="English">
  <track kind="captions" src="captions_es.vtt" srclang="es" label="Español">
  Your browser doesn't support video.
</video>]]></source>
  </segment>
</unit>

<!-- Simple video as placeholder -->
<unit id="u2">
  <originalData>
    <data id="d1">&lt;video src="simple.mp4" controls&gt;&lt;/video&gt;</data>
  </originalData>
  <segment>
    <source>Tutorial video: <ph id="ph1" dataRef="d1"/></source>
  </segment>
</unit>

<!-- Audio with sources - preserved as unit -->
<unit id="u3" fs:fs="audio" fs:subFs="controls," xml:space="preserve">
  <segment>
    <source><![CDATA[<audio controls>
  <source src="audio.ogg" type="audio/ogg">
  <source src="audio.mp3" type="audio/mpeg">
  Your browser doesn't support audio.
</audio>]]></source>
  </segment>
</unit>

<!-- Image map with areas -->
<unit id="u4" xml:space="preserve">
  <segment>
    <source><![CDATA[<img src="workplace.jpg" alt="Workplace" usemap="#workmap">
<map name="workmap">
  <area shape="rect" coords="34,44,270,350" alt="Computer" href="computer.htm">
  <area shape="circle" coords="337,300,44" alt="Coffee" href="coffee.htm">
</map>]]></source>
  </segment>
</unit>
```

## 4. Web Components / Custom elements

```
slot, template, custom elements
```

Web components and templates are preserved as complete units when they contain complex structure, or as placeholders when standalone.

**Examples:**

```xml
<!-- Template element - preserved as unit -->
<unit id="u1" fs:fs="template" fs:subFs="id,user-card-template" xml:space="preserve">
  <segment>
    <source><![CDATA[<template id="user-card-template">
  <style>
    .card { border: 1px solid #ccc; padding: 10px; }
  </style>
  <div class="card">
    <h3><slot name="username">Default Name</slot></h3>
    <p><slot name="email">default@example.com</slot></p>
  </div>
</template>]]></source>
  </segment>
</unit>

<!-- Custom element with slots - preserved as unit -->
<unit id="u2" fs:fs="user-card" fs:subFs="user-id,123" xml:space="preserve">
  <segment>
    <source><![CDATA[<user-card user-id="123">
  <span slot="username">John Doe</span>
  <span slot="email">john@example.com</span>
</user-card>]]></source>
  </segment>
</unit>

<!-- Simple custom element as placeholder -->
<unit id="u3">
  <originalData>
    <data id="d1">&lt;my-component id="comp1" data-value="42"&gt;&lt;/my-component&gt;</data>
  </originalData>
  <segment>
    <source>Component output: <ph id="ph1" dataRef="d1"/></source>
  </segment>
</unit>

<!-- Shadow DOM template -->
<unit id="u4" xml:space="preserve">
  <segment>
    <source><![CDATA[<my-element>
  <template shadowrootmode="open">
    <style>:host { display: block; }</style>
    <slot></slot>
  </template>
  <p>Light DOM content</p>
</my-element>]]></source>
  </segment>
</unit>
```

# 2. Decision Matrix for Element Handling

| Element Type | XLIFF Representation | When to Use |
| --- | --- | --- |
| Structural (div, section, etc.) | Skeleton | Page structure |
| List containers (ul, ol, dl) | `<group>` | List organization |
| Text blocks (p, h1-h6, etc.) | `<unit>` | Translatable blocks |
| Inline with text (a, strong, em, etc.) | `<mrk>` | Inline formatting |
| Self-closing (br, hr, img, etc.) | `<ph>` with originalData | Non-translatable inline |
| Tables | Preserved in `<unit>` | Complex structures |
| Forms | Preserved in `<unit>` | Interactive elements |
| Media elements | `<ph>` or preserved unit | Depends on complexity |
| Scripts/styles | `<ph>` with originalData | Non-localizable |


