---
author: Unknown
date: '2023-01-01'
id: '1'
title: markdown-it-py and markdown-it-pyrs Overview with Plugin and XLIFF Serialization
  Details
type: technical_documentation
---

{
  "author": "Unknown",
  "date": "2023-01-01",
  "id": "1",
  "title": "markdown-it-py and markdown-it-pyrs Overview with Plugin and XLIFF Serialization Details",
  "type": "technical_documentation"
}

# markdown-it-py and markdown-it-pyrs Overview with Plugin and XLIFF Serialization Details

### Key Points
- **markdown-it-py Overview**: As a Python port of the JavaScript markdown-it parser, it provides 100% CommonMark compliance, high-speed parsing, and extensible syntax via plugins. It generates a token stream (AST-like) for manipulation but does not natively render back to Markdown; however, it integrates well with tools like mdformat for serialization, allowing round-trip editing without external dependencies.
- **markdown-it-py Plugins**: The mdit-py-plugins collection includes essential extensions like front-matter for metadata parsing, footnotes for reference notes, definition lists for key-value structures, task lists for checkboxes, and heading anchors for permalinks. These enhance standard Markdown without compromising compliance, though custom plugin development requires familiarity with the token-based system.
- **XLIFF 2.1 Serialization for Parallel Markdown Prose**: Research suggests mapping Markdown blocks to <unit> elements, sentences to <segment>, and using inline codes (<pc>, <ph>) for formatting while storing markers in <originalData> for round-tripping. To avoid overcomplication as prioritized, evidence leans toward embedding Markdown syntax directly in <source>/<target> text (e.g., keeping *emphasis* inline), treating explicit <s> (sentence) wrappers as single segments; without <s>, segment naturally by sentences. This balances simplicity with CAT tool usability, though it may limit advanced rendering.
- **fs vs. type/subType Usage**: The fs module (attributes fs, subFs) provides HTML-like styling hints for previews (e.g., fs="em" for emphasis), ideal for semantic rendering without round-trip obligations. In contrast, type/subType attributes on <unit>/<segment> or inline codes offer classification (e.g., type="emphasis", subType="xlf:markdown"), better for metadata and processing rules. Use fs for visual cues in tools, type/subType for structural logic; combining both yields optimal interoperability.

### markdown-it-py and Plugins
markdown-it-py serves as a reliable Python alternative to JavaScript's markdown-it, emphasizing spec compliance and extensibility. It parses Markdown into tokens, enabling AST manipulation before rendering to HTML, and supports options like breaks, HTML allowance, and typographer replacements. For round-tripping (Markdown -> AST -> Markdown), pair it with mdformat's renderer, as shown in examples where tokens are modified (e.g., uppercasing text) and serialized back. Plugin integration uses .use() chaining, with community plugins available via pip extras.

The mdit-py-plugins package offers a suite of core extensions:

| Plugin | Description | Usage Example |
|--------|-------------|---------------|
| Front-Matter | Parses YAML/TOML metadata at document start. | md.use(front_matter_plugin) |
| Footnotes | Adds reference/inline footnotes with optional end placement. | md.use(footnote_plugin, inline=True) |
| Definition Lists | Supports key: value structures like in Pandoc. | md.use(deflist_plugin) |
| Task Lists | Renders checkboxes [ ]/[x] in lists. | md.use(tasklists_plugin, enabled=True) |
| Field Lists | Maps field names to bodies (reStructuredText style). | md.use(fieldlist_plugin) |
| Heading Anchors | Adds IDs and permalinks to headers. | md.use(anchors_plugin, permalink=True) |
| MyST Role/Block | Custom directives for advanced syntax (e.g., roles like {role}`content`). | md.use(myst_role_plugin) |
| AMSMath/Dollarmath | Parses LaTeX math environments. | md.use(amsmath_plugin) |
| Colon Fence | Custom fenced blocks with ::: delimiters. | md.use(colon_fence_plugin) |
| Attributes | Adds {id/class} attributes to elements. | md.use(attributes_plugin) |
| Container | Generic containers for custom blocks. | md.use(container_plugin) |

These plugins maintain CommonMark compliance while adding features, installable via pip install mdit-py-plugins.

### XLIFF 2.1 Overview and Optimal Serialization for Parallel Markdown Prose
XLIFF 2.1, defined by OASIS, standardizes localization data exchange with a core vocabulary for extracting, translating, and merging content. Key elements include <xliff> (root), <file> (document container), <group> (hierarchy), <unit> (translatable block), <segment> (sentence-level), <source>/<target> (text pairs), and <originalData>/<data> (markup storage).

For serializing parallel Markdown (source + translation) while prioritizing simplicity:
- Map Markdown blocks (e.g., paragraphs, headings) to <unit>, nesting in <group> for lists/tables.
- Embed inline formatting directly in <source>/<target> text (e.g., <source>Text with *emphasis*</source>) to avoid overcomplication, using <mrk> for annotations if needed. This keeps translators focused on content, but for round-tripping, optionally abstract with <pc>/<ph> referencing <originalData> (e.g., <pc dataRefStart="d1" dataRefEnd="d2">emphasis</pc> where d1="*", d2="*").
- Segmentation: If Markdown uses explicit <s> (sentence wrappers, e.g., in custom AST), treat as one <segment> even with multiple sentences; otherwise, segment by natural sentences, setting canResegment="no" on <unit> for fixed blocks. Use <ignorable> for non-translatable parts.
- Preserve attributes via mda module (e.g., <mda:meta type="list-tight">true</mda:meta>).

This approach ensures standards compliance, CAT tool productivity, and bit-for-bit regeneration, validated via schemas.

### fs vs. type/subType Discussion
In XLIFF 2.1, fs (Format Style module) and type/subType serve complementary roles for Markdown:
- **fs/subFs**: Attributes for lightweight HTML-equivalent labeling (e.g., fs="em" for *italic*, fs="h2" for ## heading), enabling previews in CAT tools without round-trip enforcement. Use on <unit>/<group> or inline codes for visual hints; ideal for Markdown semantics like fs="ul" for lists.
- **type/subType**: Core attributes for classification (e.g., type="heading", subType="2" on <unit>), with subType prefixed (xlf: or custom). Better for processing logic, like filtering or validation; combine with fs for full semantics (e.g., type="emphasis" subType="xlf:markdown-italic" fs="em").
- Recommendation: Favor fs for rendering-focused tasks (e.g., in <segment> for quick views), type/subType for structural/metadata needs (e.g., in <unit> for hierarchy). This hybrid avoids redundancy while supporting diverse tools.