# External Libraries and Specifications

This document provides a detailed overview of the external libraries, specifications, and tools that are relevant to this project.

## 1. XLIFF 2.1 Specification (`901-xliff-spec-core-21.xml`)

This XML file contains the official OASIS specification for XLIFF (XML Localization Interchange File Format) Version 2.1. XLIFF is designed to standardize the way localizable data is passed between tools during the localization process.

### Key Information from the Specification:

*   **Title:** XLIFF Version 2.1
*   **Status:** OASIS Standard
*   **Publication Date:** 13 February 2018
*   **Abstract:** The purpose of this vocabulary is to store localizable data and carry it from one step of the localization process to the other, while allowing interoperability between and among tools.
*   **Core Namespace:** `urn:oasis:names:tc:xliff:document:2.0`

The document details the core structure of an XLIFF document, including elements like `<xliff>`, `<file>`, `<unit>`, `<segment>`, `<source>`, and `<target>`. It also defines conformance criteria for both XLIFF documents and applications that process them.

*(Note: The full content of the specification file was truncated in the reading process.)*

## 2. `markdown-it-py`

`markdown-it-py` is a Python port of the popular JavaScript Markdown parser `markdown-it`. It is designed to be fast, configurable, and CommonMark compliant.

### `executablebooks-markdown-it-py.md`

This markdown file contains a collection of code snippets demonstrating the usage of the `markdown-it-py` library. The snippets cover a wide range of functionalities.

#### Snippet Categories:

*   **Installation:** Instructions for installing `markdown-it-py` using `pip` and `conda`, including optional extras like `plugins` and `linkify`.
*   **Basic Usage:** Simple examples of how to initialize `MarkdownIt` and render markdown to HTML.
*   **Configuration:** How to use presets (`commonmark`, `gfm-like`, `zero`) and override specific options.
*   **Plugins:** How to enable and use external plugins from `mdit-py-plugins`.
*   **Command-Line Usage:** How to use the `markdown-it` command-line tool.
*   **Advanced Usage:**
    *   Customizing renderer rules (e.g., for embedding Vimeo videos).
    *   Parsing text to a token stream.
    *   Enabling/disabling specific parsing rules.
*   **Syntax Examples:** Numerous examples of markdown syntax and its corresponding HTML output, including:
    *   Tables (basic, aligned, nested, edge cases)
    *   Links and Images
    *   Emphasis (bold, italic, nested)
    *   Strikethrough
    *   Typographic replacements (quotes, dashes, symbols)
    *   HTML blocks
    *   Fenced code blocks
*   **Development:** Instructions for setting up pre-commit hooks and building documentation.
*   **Fuzzing:** How to run fuzzing tests locally using `tox` and `oss-fuzz`.

This file serves as a practical guide and test suite for the `markdown-it-py` library's features.

### `executablebooks-markdown-it-py` Directory

This directory contains the documentation for the `markdown-it-py` project.

*   `architecture.md`: Explains the design principles of `markdown-it-py`, including the data flow (core, block, inline rule chains), the token stream representation, and the renderer architecture.
*   `conf.py`: The Sphinx configuration file for building the project's documentation.
*   `index.md`: The main index page for the documentation.
*   `performance.md`: Contains benchmarking information comparing `markdown-it-py` with other Python Markdown parsers.
*   `plugins.md`: Describes how to use built-in and external plugins.
*   `security.md`: Discusses security considerations when parsing untrusted content and recommends best practices.
*   `using.md`: A detailed guide on how to use the `markdown-it-py` API, including parser configuration, token stream manipulation, and custom renderers.

## 3. `mdit-py-plugins`

This directory contains a collection of plugins for `markdown-it-py`, extending its functionality with additional Markdown features.

### Available Plugins:

The `mdit_py_plugins` subdirectory includes the following plugins:

*   `admon`: Admonitions (e.g., `!!! note`).
*   `amsmath`: AMSmath blocks.
*   `anchors`: Header anchors.
*   `attrs`: Add attributes to elements.
*   `container`: Generic block-level containers.
*   `deflist`: Definition lists.
*   `dollarmath`: Dollar-enclosed math syntax.
*   `field_list`: Field lists.
*   `footnote`: Footnotes.
*   `front_matter`: YAML front matter.
*   `myst_blocks`: MyST-style block-level directives.
*   `myst_role`: MyST-style inline roles.
*   `subscript`: Subscript (`~sub~`).
*   `tasklists`: Task lists (`- [ ]`).
*   `texmath`: TeX-style math.
*   `wordcount`: Word counting.
*   `colon_fence.py`: Fenced code blocks with colons.
*   `substitution.py`: Substitution definitions.

## 4. `Xliff-AI-Translator`

This directory contains a Python tool for translating XLIFF files using AI models.

### `README.md`

The README provides an overview of the tool, its features, installation instructions, and basic usage.

*   **Features:** Automated translation of XLIFF files, integration with AI models, batch processing.
*   **Installation:** Can be installed via `pip` or from source.
*   **Usage:** A command-line tool that takes a source XLIFF file, a destination file, and a target language code.

### `xliff_ai_translator/main.py`

This is the main script for the translator.

*   It uses the `transformers` library from Hugging Face, specifically the `facebook/m2m100_418M` model, for translation.
*   It defines data classes to represent the structure of an XLIFF file (`File`, `TransUnit`, `TextContainer`, `GElement`).
*   It includes functions for parsing XLIFF files, translating text in batches, and building the translated XLIFF file.
*   The script is designed to be run from the command line.

## 5. `translate-toolkit`

This directory contains the Translate Toolkit, a comprehensive set of software and documentation for localizers.

### `README.rst`

The README provides a high-level overview of the toolkit.

*   **Purpose:** To help make the lives of localizers more productive and less frustrating.
*   **Features:**
    *   Conversion between various localization formats (DTD, .properties, OpenOffice.org, CSV, MO, Qt .ts, TMX, TBX, WordFast, RC, PO, XLIFF).
    *   Tools for checking and managing PO and XLIFF files (e.g., `pofilter`, `pomerge`, `pogrep`).
    *   Other utilities like `pocompile` (to create MO files), `pocount`, and `posegment`.
*   **Requirements:** Python 3.9+, `lxml`, and other optional dependencies for specific features.

### `translate` Directory Structure

The core logic of the toolkit is organized into several subpackages within the `translate` directory:

*   `convert`: Contains scripts for converting between different formats.
*   `filters`: Tools for checking and filtering translations.
*   `lang`: Language-specific data and utilities.
*   `misc`: Miscellaneous helper scripts.
*   `search`: Tools for searching within translation files.
*   `services`: Integration with translation services.
*   `share`: Shared resources.
*   `storage`: Classes for handling various storage formats (PO, XLIFF, etc.).
*   `tools`: Command-line tools.


## 1. XLIFF 2.1 Core Specification (901-xliff-spec-core-21.xml)

The file `901-xliff-spec-core-21.xml` is the authoritative DocBook XML source for the OASIS XLIFF Version 2.1 standard. XLIFF 2.1 is the current version of the XML-based format for localization interchange, approved as an OASIS Standard in 2018. It builds on 2.0 with enhanced module support for inline elements, fragments, and internationalization.

### Document Metadata
- **Title**: XLIFF Version 2.1
- **Status**: OASIS Standard
- **Language**: en-US
- **Product**: xliff-core-v2.1 (os)
- **Specification URIs**:
  - Authoritative HTML: http://docs.oasis-open.org/xliff/xliff-core/v2.1/os/xliff-core-v2.1-os.html
  - PDF: http://docs.oasis-open.org/xliff/xliff-core/v2.1/os/xliff-core-v2.1-os.pdf
  - XML: http://docs.oasis-open.org/xliff/xliff-core/v2.1/os/xliff-core-v2.1-os.xml
- **Committee**: OASIS XLIFF TC (https://www.oasis-open.org/committees/xliff/)

### Authors and Contributors
- **Chair**: Bryan Schnabel (bryan.s.schnabel@tektronix.com)
- **Editors**: David Filip, Tom Comerford, Soroush Zagorani, Felix Sasaki
- **Additional Key Contributors**: Yves Savourel (enunciate LLC), Rodolfo M. Raya (Max Programs), Phil Ritchie (译文堂), Steven Waxman (Individual), and TC members from SDL, Welocalize, etc.

### High-Level Structure
The XML parses into an <article> with:
- <articleinfo>: Metadata, abstract, keywords (e.g., "localization", "interchange", "translation").
- 5 Main <section>s: Core concepts, inline content, validation, extensions.
- 4 <appendix>es: Conformance, schemas, references, revisions.

### Detailed Content Breakdown
1. **Core Elements**:
   - <xliff version="2.1" srcLang="en" trgLang="es" xmlns="urn:oasis:names:tc:xliff:document:2.0">.
   - <file original="doc.html" datatype="html">, <group>, <notes>, <unit id="1">.
   - Within <unit>: <segment id="1"><source>Text</source><target>Translated</target></segment>.
   - Attributes: canMatch, canReorder, sizeRestriction, validated.

2. **Inline Content**:
   - Codes: <pc id="1" fs="b">bold</pc> (paired), <ph id="1" /> (placeholder), <sc id="1" /> <ec id="1" /> (start/end).
   - <mrk mtype="protected" > protected text, <sm>/<em> for modules.
   - <cp hex="3C"></cp> for chars >127.
   - fs module: fs:fs="i" subFs="class=emphasis" for <i class="emphasis">.
   - Space: <data xml:space="default"></data>.

3. **Segmentation and Units**:
   - <seg> for approved/translated states.
   - <ignorable> for non-translatable.
   - <match> in mda module.

4. **Modules and Extensions**:
   - Core only required; others optional (fs, its, res, etc.).
   - ITS 2.0: its:translate="no" via <mrk>.
   - Validation: Must validate against schemas.

5. **Processing Requirements**:
   - Preserve unknowns, process in order, bidirectional.

**Appendices**:
- A: Conformance (targets like CTR-CoreAll).
- B: Schemas (xliff_core_2.1.xsd, modules).
- C: Refs (RFC, Unicode TR9, etc.).
- D: Changes (e.g., relaxed <pc> nesting).

### File Stats
- Lines: ~4500 (estimated; detailed spec with examples/XML snippets).
- Parse: ElementTree succeeds; sections as list.

### Vexy Markliff Integration
- Dictates <unit> segmentation from Markdown paragraphs/sentences.
- fs for HTML attrs (e.g., <img src> as <ph fs="img src=..." />).
- Ensures round-trip: Skeleton for structure, content in units.

Header Sample:
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE article ... >
<article status="OASIS Standard" lang="en-US">
  <articleinfo><title>XLIFF Version 2.1</title>...</articleinfo>
```

## 2. executablebooks-markdown-it-py.md

A ~5580-line MD file of extracted code snippets from markdown-it-py docs. Format: ====================
TITLE: ...
DESCRIPTION: ...
SOURCE: github link
LANGUAGE: bash/python
CODE: ```
...
```
--------------------------------

### Major Themes
1. **Dev/Setup (~50 lines)**:
   - Pre-commit: install hooks for black, ruff, mypy.
   - Contributing: Git workflow, tox tests.

2. **Install (~20 lines)**:
   - pip: base, [plugins], [linkify], [full].
   - Conda: conda-forge channel.
   - Docker: For reproducible env.

3. **Core Usage (~100 lines)**:
   - Import MdIt, parse/render.
   - Options: html=True, xhtmlOut, typographer.
   - Env: md.render(src, env={'foo': 'bar'}).
   - Tokens: md.parse(src), token.type/content.

4. **Syntax Demos (~4000 lines)**:
   - Inline: Links (all types, 100+ ex in inline-links-flat.md), images, emphasis (*_ , ** , ~~), code `code`, autolink <https>.
   - Block: Headings #, lists -/1., blockquote >, code ```lang, tables |left| right:---:|--:|,
   - GFM: Def lists term: desc, footnotes [^1], tasklists - [x](id).
   - Escapes, entities, HR ***.
   - Samples from spec: commonmark-spec.md, gfm-spec.md excerpts.

5. **Advanced (~500 lines)**:
   - Plugins: md.use(plugins.MyPlugin()).
   - Custom rules: core.inline.rulesTokens.add('myrule').
   - Walk tokens: for t in tokens: if t.nesting == 1 and t.tag == 'p'.
   - Render override: class MyRenderer(MdRenderer): def text(self, tokens, idx): ...
   - Linkify: md.linkify = True.

### Relevance
Test cases for Vexy Markliff parser. Syntax for supported elements (e.g., tables → <table> in XLIFF skeleton).

Sample:
```bash
pip install markdown-it-py[plugins]
```

## 3. executablebooks-markdown-it-py Folder

markdown-it-py repo clone (v3.0.0+, Python 3.8). Fast MD parser (md4c C lib for blocks), CommonMark/GFM, extensible via rules/plugins.

### Full Structure
Root: .pre-commit-config.yaml, CHANGELOG.md, pyproject.toml (requires mistune? No, md4c).

src/markdown_it (~40 py, 5k loc):
- core: MarkdownIt (init, parse, render, parseInline, use, enable).
- renderer: render methods for tokens (link_open → <a>, code_inline → <code>).
- parser_core: Block/inline state, tokenize.
- rules_block: 15 py (e.g., table.py: parse | rows |, align left/center/right).
- rules_inline: 10 py (link.py: [text](url) → inline_link token).
- tokens: 10 classes (TextToken, DelimiterToken, etc.).
- presets: commonmark, default, zero (no rules).

tests (~100 py):
- test_rules_block.py: For each rule, spec tests.
- integration: Render and assert HTML.
- perf: timeit parse.

docs: Full API docs, examples.
benchmarking: 50 samples.md, run_bench.py.

### Key Impl Details
- Tokens as list of Token(type='heading', tag='h1', content='Text', nesting=-1/0/1).
- Plugins: def plugin(md): md.core.ruler.before('inline', 'foo', rule).
- Speed: 1M ch/s on block parsing.

Relevance: Base for MD→HTML, token walk for segmentation (e.g., split at sentences).

## 4. mdit-py-plugins Folder

Plugins repo (v0.3.0). 20 packages, each installable as mdit-py-plugin-name.

### Detailed Plugins
From dirs:
- anchor/: rule for {#anchor} in headings, token.meta['id'] = 'anchor'.
  Tests: test_anchor.py (pytest, assert meta).
- attrs/: ::: {.class #id} blocks, parse attrs dict.
- colon_fence/: Fenced ````:python`.
- container/: Admonitions !!! info > Title > content !!!
  Render: <details class="info"><summary>Title</summary>content</details>.
- dollarmath/: $f(x)$ → <span class="math inline">.</span> (needs texmath dep?)
- emphasis/: Extra delims ++mark++ → <ins>, ~~del~~ → <del>.
- field_list/: :author: Adam
  :date: 2024
  Token as definition_list.
- footnotes/: [^myref] text [^myref]: def.
  Env refs dict, render <sup id="fnref"> <section id="footnotes">
- implicit_figures/: ![fig](url) → <figure><img><figcaption>fig</figcaption></figure>.
- inline_svg/: ![svg](data:image/svg...) inline embed.
- linkify/: Auto <http> → link (uses linkify-it-py).
- replacements/: \" → “, ... → … .
- sub/: a~b~c → a<sub>b</sub>c (tilde sub).
- sup/: a^b^c → <sup>b</sup>.
- substitution/: |var| → env['var'] replace.
- table/ (core GFM tables, extensions for headers).
- tasklists/: - [x] → <input type=checkbox checked> (with id for js).
- texmath/: $$ eq $$ → <div class="math"> (dollar display).
- toc/: Auto [TOC] → <nav> headings links.
- typographer/: Advanced replacements (french quotes, etc.).

Common: pyproject.toml (hatchling), src/mdit_py_plugins_plugin_name/, tests/test_*.py (rule applications, render matches).

### Relevance
Enable in MdIt: `md.use('mdit-py-plugins', 'tasklists')` for project features (task_lists, footnotes, tables, strikethrough via emphasis).

## 5. Xliff-AI-Translator Folder

Python package for translating XLIFF segments using AI (OpenAI GPT). Preserves XLIFF structure, focuses on workflow automation.

### Structure
- setup.py: setuptools, entry_points={'console_scripts': ['xliff-ai = xliff_ai_translator.main:main']}.
- xliff_ai_translator/:
  - __init__.py: __version__ = '0.1.0'.
  - main.py: Parser, loop units, translate_source, write_xlf.
  - Models: Perhaps dataclass Unit(source, target, inline).
  - AI: openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Translate to {trg}: {source}"}]).
- Requirements: openai, lxml, click (CLI).

From py files: main.py handles file I/O, unit extraction via XPath //trans-unit/seg/source.

### Workflow
1. Parse XLIFF with lxml.etree.parse.
2. For each <source>: If <target empty, prompt AI with context (prev units?).
3. Preserve inline: Serialize <source> to str, replace text nodes only.
4. Update <target>, set state="translated".
5. Output new.xlf, log stats (units translated).

Features: --model, --lang, --api-key env, --dry-run print prompts.

### Relevance
Example for post-conversion AI step in Vexy workflows. Adapt for ITS locale info, fs preservation.

## 6. translate-toolkit Folder

Translate Toolkit v3.11.0 (GPL-2.0), localization Swiss Army knife. Lib + 60+ CLI tools for formats, quality, conversion. Python 3.9+, deps lxml, Babel, six.

### Comprehensive Structure
Root: .mailmap, AUTHORS.rst, FUNDING.yml, README.rst, pyproject.toml (hatchling), renovate.json (dep updates).

.well-known/funding-manifest-urls (github).

.github/workflows (5): docs (Sphinx), pre-commit (pre-commit run), setup (hatch build/release), test (pytest -m "not slow" --cov), test-qemu (cross-arch).


docs (120+ rst/py):
- Makefile, make.bat (sphinx-build).
- _ext/translate_docs.py (custom dir).
- _static/README.txt.
- api/10 rst: convert (format conv API), filters (vis/dec/spell), lang (BCP47), misc, search (levenshtein), services (Weblate/MO), storage (XliffFile class), tools (CLI wrappers).
- commands/65 rst: Each tool doc, e.g., android2po (XML→PO), csv2po/tbx (CSV), html2po (lxml parse), idml_update (InDesign), json2po (i18n JSON), po2*, rc2po (Win res), txt2po (plain), xliff2po/po2xliff (full), xliff_check (validate).
- formats/41 rst: Detailed specs, e.g., xliff.rst (1.2/2.0, modules its/res/mda, inline g/x/bx).
- guides/12 rst: Weblate, Virtaal, Okapi integration.
- releases/113: v1.10.0 to v3.11.0 changelogs.
- Other: features (list tools), history, index, installation (pip/conda), license.

translate/ (core, 300+ py, 50k loc):
- misc/12 py: dictutils (nested get/set), ourdom (lxml monkeypatch), file_discovery (walk dirs), xml_helpers (ns clean, indent), optrecurse (options recurse), deprecation (warn), quote (PO escapes), selector (css-like //div.class), multistring (plural str).
- storage/ (format classes):
  - base: MultilingualMultiFile, MultiFile.
  - xliff.py (~1000 lines): XliffFile, parse (lxml iter trans-unit), units as list of Unit(source, target, note, locations), inline to/from str (protect <g id="1">), save (pretty xml), supports 1.2/2.0, modules.
  - Other: po.py, tmx14/21.py, tbx.py, gettextrm.py, etc.
- filters/: base.py (decorator), checks (quality placeholders), decoration (vis escapes), pofilter (checks), spellchecker (pyenchant).
- lang/: BCP47.py (parse en-US), data (codes dicts), identify (lang guess).
- convert/20 py: Converters like Csv2Po, Html2Po (BeautifulSoup? No lxml), Xliff2Po (extract units).
- tools/: 60+ CLI, e.g., xliff2po.py (storage + argparse).

tests/translate/ (full pytest, ~80% cov): test_storage_xliff.py (load/save roundtrip, inline preserve).

locale/ (i18n PO files).

### XLIFF Deep Dive
- XliffFile: fromfile/tofile, units = [Unit('hello', None, note='foo')];
  unit.source = 'hola'; unit.addlocation('file.py:10').
- Inline: unit.gettargets() → str with protected <x id="1"/>.
- Modules: Parse <its:locQualityIssue> etc.
- CLI ex: `toolkit convert xliff2po input.xlf` (opts --threshold=80 for fuzzy).
- Limits: 2.1 basic (no full fs module), but extensible via add_module.

### Relevance & Usage in Vexy
- Leverage storage.xliff for parse/gen, unit iter for segmentation match.
- Convert to PO for CAT tools, back.
- Validate: toolkit validate --language en xliff.xlf.
- Custom: Subclass XliffFile for HTML skeleton, fs attrs.
- Add: uv add translate-toolkit; import translate.storage.xliff.

These resources form the foundation for Vexy Markliff's technical accuracy and extensibility.
