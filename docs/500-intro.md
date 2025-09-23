# 1. HTML-XLIFF Handling by Vexy Markliff

## 1. Introduction

The XML Localization Interchange File Format (XLIFF), particularly its current OASIS Standard version 2.1, represents the pinnacle of standardized data exchange in the modern localization industry. Ratified on February 13, 2018, XLIFF 2.1 builds upon the significant architectural overhaul of version 2.0, offering a more modular, extensible, and robust framework than its widely adopted but aging predecessor, XLIFF 1.2. Its core purpose is to serve as a universal, tool-agnostic container for localizable data, facilitating seamless interchange throughout the complex, multi-step localization lifecycle. By design, it allows content to be extracted from a native format, translated in a Computer-Assisted Translation (CAT) tool, and then merged back into the original structure with high fidelity.

This capability is of paramount importance in the context of web and digital content, which is predominantly authored in HyperText Markup Language (HTML) and, increasingly, in lightweight markup languages like Markdown. The central challenge in localizing such content extends beyond the mere translation of text. It encompasses the critical need to preserve the structural integrity, inline formatting, and semantic metadata of the original document. A failure to manage this complex interplay of text and code can lead to broken layouts, corrupted files, increased costs, and a degraded user experience. Therefore, a clear and precise understanding of the interoperability mechanisms between XLIFF 2.1 and these formats is not an academic exercise but a foundational requirement for building scalable, efficient, and reliable global content pipelines.

This report provides a definitive technical analysis of the official standards and established industry practices governing the relationship between XLIFF 2.1, HTML, and Markdown. It will demonstrate that while XLIFF 2.1 provides a mature, sophisticated, and formally standardized framework for interoperability with HTML—primarily through the normative integration of the W3C Internationalization Tag Set (ITS) 2.0—its relationship with Markdown is fundamentally different. The XLIFF 2.1 specification does not define a standard for handling Markdown, leaving its implementation to a landscape of de facto, tool-dependent workflows. This distinction presents localization architects and internationalization engineers with a clear set of architectural trade-offs that must be carefully evaluated when designing content localization systems.

## 2. The XLIFF 2.1 Core: A Foundation for Interchange

To comprehend how XLIFF 2.1 interacts with external formats like HTML and Markdown, it is essential to first understand its core architectural philosophy and the key structural elements that enable its function as an interchange format. The design of XLIFF is predicated on the principle of abstraction: separating the translatable "meat" of a document from its non-translatable "skeleton". This separation allows translators to work within a standardized environment, focusing solely on the linguistic task without the risk of accidentally altering the underlying code structure of the source file.

### 2.1. Architectural Philosophy

The fundamental goal of an XLIFF-based workflow is to create a "bitext" document—a single file that contains both the source language text and its corresponding translation, organized into discrete units. This is achieved through an "extraction and merge" round-trip process. An "Extractor" agent parses a source file (e.g., an HTML page), identifies the localizable text, and places it within a structured XLIFF document. The surrounding code, layout information, and non-translatable elements are preserved in a separate part of the XLIFF file known as the skeleton. After translation, a "Merger" agent recombines the translated text with the original skeleton to reconstruct a fully localized version of the source file. XLIFF 2.1 provides a rich set of elements to manage this process with precision and to carry contextual information that aids translators.

### 2.2. Key Structural Elements

The XLIFF 2.1 standard defines a clear and logical hierarchy of elements that form the basis of any compliant document. A thorough understanding of these elements is critical for implementing correct and efficient localization workflows.

* **`<xliff>`**: This is the root element of any XLIFF 2.1 document. It is mandatory and contains one or more `<file>` elements. Its attributes define the foundational parameters of the interchange: `version` (which must be "2.1"), `srcLang` (the source language code, required), and `trgLang` (the target language code, optional but required if any `<target>` elements are present).

* **`<file>`**: This element acts as a container for all the localizable material extracted from a single source document. For example, if localizing three separate HTML files, the XLIFF document would contain three distinct `<file>` elements. The `id` attribute provides a unique identifier for the file within the XLIFF document, while the optional `original` attribute is crucial for the round-trip process, as it can store the path or name of the source file from which the content was extracted.

* **`<skeleton>`**: This element is central to achieving high-fidelity round-tripping. It is designed to hold the non-translatable parts of the original file. For an HTML document, this could include the `<html>`, `<head>`, and `<body>` tags, stylesheet links, and script blocks—everything except the translatable content itself. The skeleton can either be embedded directly within the XLIFF file or, more commonly for large files, stored externally and referenced via an `href` attribute. The specification is strict: processing tools must not modify the contents of the `<skeleton>` element.

* **`<unit>`**: A `<unit>` represents a fundamental, logical block of translatable content extracted from the source file. This could correspond to a paragraph (`<p>`), a list item (`<li>`), a heading (`<h1>`), or a single string from a resource file. Each `<unit>` is assigned a unique `id` for addressing. A crucial architectural principle of XLIFF 2.1 is that the structure at the `<unit>` level and higher is considered immutable. Downstream tools, such as CAT tools, are prohibited from adding, deleting, or reordering `<unit>` elements. This ensures that the macro-structure of the original document is preserved throughout the localization process.

* **`<segment>`**: Contained within a `<unit>`, the `<segment>` element holds a single source-target pair of text. A key innovation in XLIFF 2.0, refined in 2.1, is the decoupling of the logical `<unit>` from the translatable `<segment>`. A single `<unit>` (e.g., a paragraph) can be broken down into multiple `<segment>` elements (e.g., individual sentences) by the extraction tool or even by the translator within the CAT tool. This provides linguistic flexibility without violating the structural integrity of the `<unit>`.

* **`<source>` and `<target>`**: These are the simplest and most fundamental elements, residing within a `<segment>`. The `<source>` element contains the original text to be translated, and the `<target>` element holds its translation. These elements contain not only plain text but also the inline elements (`<pc>`, `<ph>`, `<mrk>`) that represent formatting and other markup from the source document.

The distinction between the immutable high-level structure and the malleable segmentation within it is a deliberate and powerful design feature of XLIFF 2.1. The specification's strict hierarchy and the prohibition on modifying the `<unit>` structure ensure that an automated merger agent can always reconstruct the target document correctly by re-inserting the translated units into their original positions within the skeleton. At the same time, the ability for CAT tools to split or join `<segment>` elements within a `<unit>` empowers translators to work with more logical and contextually appropriate chunks of text, improving translation quality and efficiency.

## 3. Mechanisms for Representing Inline Markup

The primary challenge when extracting content from formats like HTML and Markdown is preserving the inline formatting codes that are interspersed with the translatable text. These codes, such as bold tags, hyperlinks, or italics, must be protected from alteration by the translator but must also be correctly placed in the translated target text. XLIFF 2.1 provides a sophisticated and streamlined set of inline elements for this purpose.

### 3.1. XLIFF 2

XLIFF 1.2 relied on a set of generic tags such as `<bpt>` (begin paired tag), `<ept>` (end paired tag), `<ph>` (placeholder), and `<it>` (isolated tag) to represent inline markup. While functional, this system could be cumbersome and less intuitive.

XLIFF 2.0 introduced a completely redesigned model, which is carried forward in 2.1, centered around three primary inline elements: `<ph>` (placeholder), `<pc>` (paired code), and the annotation-focused `<mrk>` (marker). This modern approach more clearly distinguishes between different types of inline content, simplifying both the extraction and translation processes.

### 3.2. The `<ph>` (Placeholder) Element

* **Definition:** The `<ph>` element represents a standalone, or "empty," inline code that does not enclose any translatable text. It acts as a placeholder for an element from the original format that must be preserved in the translated text.

* **Use Cases (HTML/Markdown):** This element is ideal for representing self-closing HTML tags like `<br/>`, `<hr/>`, and `<img>`. It is also the correct representation for simple, non-paired Markdown syntax, such as a horizontal rule (`---`). In some scenarios, it can also be used as a fallback mechanism to "hide" non-translatable inline content (like a `<code>` tag) when the content itself is not needed for context by the translator, effectively replacing the entire inline element with a single, protected placeholder tag. For example, the HTML snippet `Click here.<br/>` would be extracted into a `<source>` element as `Click here.<ph id="1"/>`. The actual `<br/>` tag would be stored in a separate `<originalData>` section of the XLIFF file, linked by the `id`.

### 3.3. The `<pc>` (Paired Code) Element

* **Definition:** The `<pc>` element is the primary mechanism for handling paired formatting codes. It represents a pair of opening and closing codes from the source document that surround a span of text. The content within the `<pc>` element is part of the translatable text and can contain further nested inline codes.

* **Use Cases (HTML/Markdown):** This element is perfectly suited for representing common paired HTML tags such as `<b>...</b>`, `<i>...</i>`, `<u>...</u>`, `<span>...</span>`, and `<a href="...">...</a>`. In Markdown, it would be used to represent formatting like `**bold text**` or `*italic text*`. The translator can see and translate the text inside the `<pc>` element, but the element itself acts as a protected boundary, ensuring the formatting is correctly applied in the target segment.

* **Example:** The HTML snippet `<p>Please <b>click here</b> to continue.</p>` would be represented in an XLIFF `<source>` element as `Please <pc id="1">click here</pc> to continue.`. The `<originalData>` section would contain a reference mapping the `id="1"` to the original `<b>` and `</b>` tags, allowing the merger agent to reconstruct the HTML correctly.

### 3.4. The `<mrk>` (Marker) Element

* **Definition:** The `<mrk>` element is fundamentally different from `<ph>` and `<pc>`. It is an annotation element that marks or "highlights" a span of text for a specific purpose, rather than representing a formatting code from the original document. Its purpose is to carry metadata about the enclosed text through the localization process.

* **Use Cases (HTML/Markdown):** The `<mrk>` element has several critical applications. Its most important function in the context of HTML interoperability is to carry ITS 2.0 metadata inline. For instance, if an HTML `<code>` tag is marked with `translate="no"`, this instruction is conveyed in XLIFF by wrapping the corresponding text in `<mrk translate="no">...</mrk>`. This tells the CAT tool to lock the enclosed text. Other uses include marking specific terms for terminology database lookups (`<mrk type="term">...`) or adding inline comments for the translator that are specific to a substring of the segment. The `<mrk>` tag must be correctly mirrored in the `<target>` element to ensure metadata integrity is maintained.

The following table provides a comparative summary of these three essential inline elements, offering a quick reference for developers and engineers tasked with creating XLIFF extraction rules.

| Element | Purpose | Content Model | Typical HTML/Markdown Use Case |
|---|---|---|---|
| `<ph>` | **Placeholder:** Represents a standalone, non-paired code. | Empty element (e.g., `<ph id="1"/>`). | `<img>`, `<br/>`, `<hr/>`, Markdown `---`. |
| `<pc>` | **Paired Code:** Represents a pair of codes surrounding text. | Can contain text and other nested inline elements. | `<b>...</b>`, `<a href="...">...</a>`, Markdown `**bold**`. |
| `<mrk>` | **Marker:** Annotates a span of text with metadata. | Can contain text and other nested inline elements. | Representing ITS `translate="no"`, flagging terminology. |

## 4. Official Interoperability with HTML: The ITS 2.0 Module

The formal, standards-based correspondence between XLIFF 2.1 and HTML is unequivocally established through the native integration of the W3C Internationalization Tag Set (ITS) 2.0. This integration is a cornerstone feature of the XLIFF 2.1 specification and provides a robust, standardized mechanism for communicating localization-specific instructions from a source HTML document to the localization toolchain.

### 4.1. The Role of the W3C Internationalization Tag Set (ITS) 2.0

ITS 2.0 is a W3C Recommendation that defines a vocabulary of attributes and elements used to add internationalization and localization metadata to XML and HTML documents. The purpose of ITS is to make content "localization-ready" by embedding instructions directly within the source file. These instructions, known as "data categories," cover a wide range of localization concerns, from specifying which parts of a document should or should not be translated, to providing notes for translators, identifying terminology, and setting constraints on text length. By using ITS attributes in HTML, content creators can provide explicit guidance that can be programmatically interpreted by localization tools, reducing ambiguity and manual intervention.

### 4.2. Normative Integration in XLIFF 2.1

A major advancement in XLIFF 2.1 is its native, normative support for ITS 2.0. This means that the XLIFF 2.1 standard formally defines how ITS metadata from a source document should be represented within the XLIFF file. This is not an optional or proprietary extension; it is a core part of the specification. This formal bridge ensures that localization instructions applied in an HTML document are preserved and understood throughout the XLIFF-based workflow. To enable this, XLIFF 2.1 reserves a specific namespace, `urn:oasis:names:tc:xliff:itsm:2.1` (typically prefixed as `itsm`), for ITS attributes when used within an XLIFF document.

The integration of ITS 2.0 elevates XLIFF 2.1 beyond a simple bitext format. It transforms it into a sophisticated metadata hub for the entire localization lifecycle. An instruction, such as a "do not translate" flag, can originate with a content author in a CMS, be embedded as an ITS attribute in the published HTML, travel losslessly within the XLIFF file to the CAT tool, be used to automatically lock the relevant segment for the translator, and then be carried back in the translated XLIFF file for final validation. This creates a single, authoritative channel for localization metadata, significantly reducing the potential for human error and eliminating the need for out-of-band communication like spreadsheets or email instructions.

### 4.3. Mapping Key ITS Data Categories

The XLIFF 2.1 specification provides clear mappings for several of the most important ITS 2.0 data categories.

* **Translate Data Category:** This is the most critical and frequently used data category. It specifies whether a piece of content is translatable. In HTML, this is typically done with the `translate` attribute (e.g., `<span translate="no">ProductCode-123</span>`). During extraction, this metadata is mapped directly to the corresponding XLIFF elements:
* If applied to a block-level element in HTML (e.g., `<p translate="no">...`), it maps to a `translate="no"` attribute on the XLIFF `<unit>` element.
* If applied to an inline element in HTML (e.g., `<code translate="no">...`), it maps to a `<mrk translate="no">...` element within the XLIFF `<source>` tag.

This provides an unambiguous, standard way to protect content from translation.

* **Preserve Space Data Category:** This data category controls the handling of whitespace. In HTML, the `xml:space="preserve"` attribute (often used on `<pre>` or `<code>` tags) indicates that all whitespace, including line breaks and multiple spaces, is significant and must be maintained. XLIFF 2.1 honors this by mapping it to an `xml:space="preserve"` attribute on the corresponding `<unit>` element. This ensures that the formatting of code snippets or poetry is not corrupted by CAT tools that might otherwise normalize whitespace.

* **Localization Note Data Category:** ITS provides a standard way to embed notes for translators directly within the source HTML. These notes can provide crucial context, explain ambiguity, or give instructions on tone and style. The XLIFF 2.1 extractor is designed to parse these ITS notes and place them within the `<notes>` element associated with the relevant `<unit>`. This makes the context immediately available to the translator in their working environment, improving translation quality.

* **Other Data Categories:** While the above are the most common, the ITS 2.0 integration also allows for the transport of other important metadata. The **Terminology** data category can be used to flag specific terms in the source and link them to a terminology database. The **Allowed Characters** and **Storage Size** data categories can convey technical constraints from a backend system (e.g., a database field with a character limit) to the translator, preventing errors that would break the application upon re-integration of the translated text.

## 5. Established Practices for HTML-to-XLIFF Conversion

While the ITS 2.0 module provides the formal standard for metadata exchange, the practical, day-to-day process of converting HTML content into XLIFF 2.1 files relies on a well-established workflow and specific features within modern localization platforms and CAT tools, following our Format Style-based approach.

### 5.1. The Extraction/Merge Workflow

The localization of an HTML file using XLIFF is a round-trip process orchestrated by two key types of software agents: an Extractor and a Merger.

1. **Extraction:** An Extractor agent is responsible for parsing the source HTML document. It performs a critical separation:
   * **Skeleton Creation:** For structural elements (html, head, body, div, section, etc.), it creates a skeleton file referenced in the `<file>` element. This skeleton contains the non-translatable structural markup with placeholders like `###u1###` where translatable units will be inserted.
   * **Content Extraction:** It identifies all the translatable content within block elements like `<p>`, `<h1>`, `<li>`, etc. Each is placed into its own `<unit>` with Format Style attributes (`fs:fs` and `fs:subFs`) preserving the element type and attributes.
   * **Inline Element Handling:** It converts inline HTML elements containing text (e.g., `<strong>`, `<a>`) into `<mrk>` elements with Format Style attributes. Self-closing elements (e.g., `<br/>`, `<img>`) become `<ph>` placeholders with originalData.
   * **Complex Structure Preservation:** Tables, forms, and media elements with tracks are preserved verbatim in units with `xml:space="preserve"`.

2. **Translation:** The resulting XLIFF 2.1 file is then processed by translators using a CAT tool. The tool presents only the text from the `<source>` elements for translation, while protecting the inline codes and Format Style markup from being accidentally modified.

3. **Merging:** After translation is complete and the `<target>` elements are populated, a Merger agent reconstructs the final translated HTML document by:
   * Processing the skeleton file and replacing placeholders with translated content
   * Restoring HTML elements from Format Style attributes
   * Reconstructing inline elements from `<mrk>` and `<ph>` elements
   * Preserving complex structures like tables and forms

### 5.2. Implementation in CAT Tools: Format Style Support

Modern localization platforms and Translation Management Systems (TMS) must provide sophisticated support for the Format Style module. When processing our XLIFF files, the tool must:
* Correctly interpret `fs:fs` attributes to identify the original HTML element type
* Parse `fs:subFs` attributes to restore HTML attributes (using our escaping convention: `,` separates name from value, `\` separates attribute pairs)
* Handle preserved content in units with `xml:space="preserve"` for tables, forms, and other complex structures
* Process `<mrk>` elements for inline formatting while maintaining Format Style metadata
* Manage `<ph>` placeholders with originalData references for non-localizable elements

### 5.3. Intelligent Segmentation

Our approach employs intelligent segmentation:
* When the HTML source contains an `<s>` element, we convert it into a single `<segment>` without further splitting
* When the HTML source contains a `<p>` element, we employ sentence splitting algorithms to create multiple segments per paragraph

### 5.4. Practical Example of HTML to XLIFF 2.1 Conversion

To illustrate the complete process following our preferences, consider the following simple HTML file:

**Original HTML (`index.html`)**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Product Information</h1>
    <p>Please visit <a href="https://example.com">our website</a> for more details.</p>
</body>
</html>
```

An XLIFF 2.1 Extractor following our approach would generate:

**Skeleton File (`skeleton/index.skl.html`)**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>###u1###</title>
</head>
<body>
    <h1>###u2###</h1>
    <p>###u3###</p>
</body>
</html>
```

**Resulting XLIFF 2.1 (`index.xlf`)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.0"
       xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"
       version="2.1" srcLang="en" trgLang="es">
    <file id="f1" original="index.html">
        <skeleton href="skeleton/index.skl.html"/>
        <unit id="u1">
            <segment>
                <source>Welcome</source>
                <target>Bienvenido</target>
            </segment>
        </unit>
        <unit id="u2" fs:fs="h1">
            <segment>
                <source>Product Information</source>
                <target>Información del Producto</target>
            </segment>
        </unit>
        <unit id="u3" fs:fs="p">
            <segment>
                <source>Please visit <mrk id="m1" fs:fs="a"
                    fs:subFs="href,https://example.com">our website</mrk> for more details.</source>
                <target>Por favor, visite <mrk id="m1" fs:fs="a"
                    fs:subFs="href,https://example.com">nuestro sitio web</mrk> para más detalles.</target>
            </segment>
        </unit>
    </file>
</xliff>
```

In this example:

* The skeleton file contains the HTML structure with `###u1###` style placeholders
* Text blocks use `<unit>` elements with Format Style attributes (`fs:fs="h1"`, `fs:fs="p"`)
* The hyperlink uses a `<mrk>` element with Format Style attributes to preserve the link URL
* The namespace is correctly set to `urn:oasis:names:tc:xliff:document:2.0` with the Format Style namespace
* No `<pc>` elements or `dataRefStart`/`dataRefEnd` attributes are used - instead we rely on Format Style

This approach provides a consistent, standardized method for handling all HTML elements while maintaining near-perfect round-trip fidelity.
