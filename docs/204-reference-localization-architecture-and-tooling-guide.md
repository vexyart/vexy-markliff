---
author: Unknown
date: Unknown
id: Unknown
title: Localization File Formats and Tools
type: Unknown
---

{"author":"Unknown","date":"Unknown","id":"Unknown","title":"Localization File Formats and Tools","type":"Unknown"}

# Localization File Formats and Tools

## XLIFF (.xlf) - The Professional Translation Interchange Standard

The XML Localization Interchange File Format (XLIFF) was developed and maintained by the OASIS consortium as a standardized, bilingual data container for exchanging localizable content between different tools and services. Its primary purpose is to serve as a robust bridge between a content management system (CMS) or code repository and the sophisticated CAT tools used by professional translators.

The core philosophy of XLIFF is interoperability. It abstracts the localizable content away from its original format, encapsulating it in a structured XML file rich with metadata. This file can then be ingested by any compliant CAT tool, allowing translators to work in their preferred environment without needing access to the original source files. Once translation is complete, the XLIFF file containing both source and target text can be automatically merged into the original application.

### Understanding XLIFF's Role and Structure

An XLIFF document is an XML file with a defined structure. XLIFF 2.0 (and the minor revision 2.1) introduced a simpler, more streamlined structure:

* `<xliff>`: The root element, specifying the version number.
* `<file>`: A container for content extracted from a single original file.
* `<unit>`: The core element representing a single unit of translation (a string). It has a unique `id` attribute.
* `<segment>`: Explicitly holds the `<source>` and `<target>` pair.
* `<source>`: Contains the text in the source language.
* `<target>`: Contains the translated text in the target language.

### Providing Rich Context for Translators

XLIFF provides mechanisms to embed contextual information for translators:

* **Notes:** The `<note>` element is the primary mechanism for adding developer comments or instructions. It can be placed within a `<file>` or a `<unit>` to provide guidance.
* **Context Group:** XLIFF includes a `<context-group>` element, which can contain one or more `<context>` elements. Each `<context>` element can provide specific information with its purpose defined by the `context-type` attribute.

### Handling Plurals in XLIFF via ICU MessageFormat

XLIFF lacks a native mechanism for handling pluralization. This has been addressed by the industry through embedding strings formatted with the **ICU MessageFormat** syntax directly within the `<source>` and `<target>` tags.

**Example: XLIFF 2.0 with ICU Plural for Polish**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.0" version="2.0" srcLang="en" trgLang="pl">
  <file id="f1">
    <unit id="file_count">
      <notes>
        <note>Pluralized string for number of files. The '#' is replaced by the count.</note>
      </notes>
      <segment>
        <source>{count, plural, one {# file found} other {# files found}}</source>
        <target>{count, plural, one {Znaleziono # plik} few {Znaleziono # pliki} other {Znaleziono # plików}}</target>
      </segment>
    </unit>
  </file>
</xliff>
```

## XLIFF in Python

To work with XLIFF files in Python, the `lxml` library is a popular choice for parsing and manipulating the XML structure. Here's an example of how to extract translatable strings and their metadata from an XLIFF file:

```python
from lxml import etree

xliff_content = """
<xliff version="1.2" xmlns="urn:oasis:"""

namespaces = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

# Parse the XLIFF file
tree = etree.parse('example.xlf')
root = tree.getroot()

# Extract translatable strings
for trans_unit in root.xpath('//xliff:trans-unit', namespaces=namespaces):
    source = trans_unit.xpath('./xliff:source', namespaces=namespaces)[0].text
    target = trans_unit.xpath('./xliff:target', namespaces=namespaces)[0].text
    id = trans_unit.get('id')
    print(f"ID: {id}, Source: {source}, Target: {target}")

# Update a translation
target_elem = root.xpath('//xliff:trans-unit[@id="welcome_message"]/xliff:target', namespaces=namespaces)[0]
target_elem.text = "Bienvenue"

# Save the modified XLIFF file
tree.write('modified_example.xlf', pretty_print=True, xml_declaration=True, encoding='utf-8')
```

For more advanced manipulation, including handling XLIFF 2.0 and ICU MessageFormat pluralization, consider using the **Translate Toolkit**'s Python API.

### The Universal Toolkit: File Conversion with Translate Toolkit

The **Translate Toolkit** is an indispensable suite of command-line utilities for localization efforts. Written in Python, it acts as a "Rosetta Stone" for localization formats, capable of converting between dozens of types.

The toolkit provides converters that follow a simple `source2target` naming convention.

**Common CLI Conversion Examples:**

* **PO to XLIFF:** Essential for sending Gettext files to professional translators who use XLIFF-based CAT tools.
```bash
po2xliff messages.de.po messages.de.xlf
```

* **XLIFF to PO:** For converting translated XLIFF files back to the Gettext format.
```bash
xliff2po messages.de.xlf messages.de.po
```

## Working with Markdown and HTML

For Markdown and HTML files, the **markdown-it-py** library is an excellent tool for parsing and manipulating content. It can be used to extract translatable text from Markdown documents while preserving their structure.

```python
from markdown_it import MarkdownIt
from markdown_it.token import Token

# Initialize the Markdown parser
md = MarkdownIt()

# Parse a Markdown document
tokens = md.parse("# Hello World\n\nThis is a **test**.")

# Extract text content for translation
def extract_text_tokens(tokens: list[Token]) -> list[str]:
    texts = []
    for token in tokens:
        if token.type == 'text' and token.content.strip():
            texts.append(token.content)
        # Recursively process children
        if token.children:
            texts.extend(extract_text_tokens(token.children))
    return texts

translatable_texts = extract_text_tokens(tokens)
print(translatable_texts)  # Output: ['Hello World', 'This is a ', 'test', '.']
```

This example shows how to use `markdown-it-py` to parse a Markdown document and extract text content suitable for translation