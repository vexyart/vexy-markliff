---
author: Unknown
date: Unknown
id: Unknown
title: 'Research Report: Markdown-it-py Ecosystem and XLIFF 2.1 Serialization for
  Parallel Markdown Prose'
type: research report
---

# Research Report: Markdown-it-py Ecosystem and XLIFF 2.1 Serialization for Parallel Markdown Prose

## Executive Summary

This report investigates the markdown-it-py ecosystem and proposes an optimal strategy for serializing parallel Markdown prose in XLIFF 2.1. The key finding is that while markdown-it-py provides excellent parsing capabilities, the serialization strategy should prioritize simplicity by **keeping inline Markdown formatting directly in XLIFF segment text** when possible, using `<s>` elements for explicit segmentation control, and leveraging `fs` attributes for semantic tagging.

## Part 1: Markdown-it-py Ecosystem Analysis

### 1.1 markdown-it-py Core

**markdown-it-py** is a high-performance, CommonMark-compliant Markdown parser for Python, ported from the JavaScript markdown-it library. Key characteristics:

- **Token Stream Architecture**: Parses Markdown into a linear stream of tokens (not a traditional AST), where each token represents a syntactic element with properties like type, nesting, content, and children.
- **CommonMark Compliance**: Strictly adheres to CommonMark specification by default, with configurable presets ('commonmark', 'js-default', 'gfm-like').
- **Plugin System**: Extensible architecture allowing custom parsing rules and syntax extensions.
- **Performance**: Among the fastest pure-Python Markdown parsers.

**Critical Limitation**: markdown-it-py does not natively support serialization back to Markdown. The token stream is designed for HTML rendering, not Markdown reconstruction.

### 1.2 mdformat: The Serialization Solution

**mdformat** fills the gap by providing Markdown-to-Markdown transformation:

```python
from markdown_it import MarkdownIt
from mdformat.renderer import MDRenderer

# Parse to tokens
md_parser = MarkdownIt()
tokens = md_parser.parse(markdown_text)

# Serialize back to Markdown
renderer = MDRenderer()
markdown_output = renderer.render(tokens, md_parser.options, {})
```

**Important Caveat**: mdformat is **opinionated** and **normalizing**. It does not preserve original formatting choices (like `*` vs `_` for emphasis), making it unsuitable for bit-perfect round-tripping.

### 1.3 mdit-py-plugins

The **mdit-py-plugins** package provides essential extensions:

- **Front Matter**: YAML metadata blocks
- **Footnotes**: CommonMark-style footnote syntax
- **Tables**: GitHub Flavored Markdown tables
- **Tasklists**: Checkbox list items `[ ]` and `[x]`
- **Deflist**: Definition lists
- **Admonition**: Block-level callouts

Example usage:
```python
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

md = MarkdownIt().use(front_matter_plugin).use(footnote_plugin)
```

## Part 2: XLIFF 2.1 Serialization Strategy

### 2.1 Core XLIFF 2.1 Principles

Based on the XLIFF 2.1 specification research:

1. **Segment flexibility**: Segments can contain multiple sentences if the source explicitly groups them.
2. **Custom metadata**: Original IDs and attributes can be preserved using namespaces or `<mda:metadata>`.
3. **Inline formatting**: The standard recommends using `<pc>` (paired codes) and `<ph>` (placeholders) for formatting, BUT...

### 2.2 Proposed Simplified Approach

**Key Innovation**: For Markdown-to-XLIFF serialization, we can **keep inline Markdown formatting directly in the text** because:

1. **Markdown is plain text**: Unlike HTML or RTF, Markdown formatting markers (`*`, `**`, `` ` ``) are human-readable text.
2. **CAT tool compatibility**: Professional translators can see and preserve Markdown syntax naturally.
3. **Round-trip simplicity**: No complex originalData mappings needed.
4. **Reduced complexity**: Avoids the overhead of `<pc>` elements for every formatting span.

### 2.3 The `<s>` Element Strategy

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

**Benefits**:
- Preserves original IDs
- Maintains explicit segmentation boundaries
- Allows custom attributes on segments

### 2.4 `fs` vs `type`/`subType` Usage

| Attribute | Purpose | Use in `<unit>` | Use in `<segment>` |
|-----------|---------|-----------------|-------------------|
| **`fs`** | Format Style - HTML-equivalent semantic tag | `fs="p"`, `fs="h2"`, `fs="ul"` for block types | `fs="s"` for sentence-level semantics |
| **`type`** | Structural category | `type="paragraph"`, `type="heading"` | `type="sentence"` if needed |
| **`subType`** | Subcategory | `subType="2"` for h2 | `subType="declarative"` for sentence types |

**Recommendation**: Use `fs` as the primary semantic indicator since it's standardized and CAT-tool friendly.

### 2.5 Optimal Serialization Pattern

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff xmlns="urn:oasis:names:tc:xliff:document:2.1"
       xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0"
       xmlns:mda="urn:oasis:names:tc:xliff:metadata:2.0"
       version="2.1">
  <file id="doc1" srcLang="en" trgLang="de" original="source.md">
    
    <!-- Heading with direct Markdown -->
    <unit id="h1-1" fs="h1">
      <segment id="h1-1-s1">
        <source># Welcome to **Markdown**</source>
        <target># Willkommen bei **Markdown**</target>
      </segment>
    </unit>
    
    <!-- Paragraph with explicit <s> elements -->
    <unit id="p1" fs="p">
      <mda:metadata>
        <mda:metaGroup category="markdown">
          <mda:meta type="has-s-elements">true</mda:meta>
        </mda:metaGroup>
      </mda:metadata>
      <segment id="s1" fs="s">
        <source>This is *italic* text.</source>
        <target>Dies ist *kursiver* Text.</target>
      </segment>
      <segment id="s2" fs="s">
        <source>This has a [link](https://example.com).</source>
        <target>Dies hat einen [Link](https://example.com).</target>
      </segment>
    </unit>
    
    <!-- Paragraph without <s> elements - auto-segmented -->
    <unit id="p2" fs="p">
      <segment id="p2-s1">
        <source>First sentence with **bold**.</source>
        <target>Erster Satz mit **fett**.</target>
      </segment>
      <segment id="p2-s2">
        <source>Second sentence with `code`.</source>
        <target>Zweiter Satz mit `Code`.</target>
      </segment>
    </unit>
    
    <!-- Code block - non-translatable -->
    <unit id="code1" fs="pre" translate="no">
      <segment id="code1-s1">
        <source>```python
def hello():
    print("Hello, World!")
```</source>
        <target>```python
def hello():
    print("Hello, World!")
```</target>
      </segment>
    </unit>
    
  </file>
</xliff>
```

### 2.6 Implementation Algorithm

```python
def markdown_to_xliff(source_md, target_md):
    """
    Convert parallel Markdown documents to XLIFF 2.1
    """
    # 1. Parse both documents
    parser = MarkdownIt()
    source_tokens = parser.parse(source_md)
    target_tokens = parser.parse(target_md)
    
    # 2. For each block token
    for src_block, tgt_block in zip(source_tokens, target_tokens):
        
        # 3. Check for explicit <s> elements in content
        if has_s_elements(src_block.content):
            # Extract each <s> as a segment
            segments = extract_s_elements(src_block.content)
            for s in segments:
                create_xliff_segment(
                    id=s.id or generate_id(),
                    source=s.content,  # Keep Markdown formatting
                    target=find_matching_target(s, tgt_block)
                )
        else:
            # Auto-segment by sentences
            sentences = segment_sentences(src_block.content)
            for sent in sentences:
                create_xliff_segment(
                    source=sent,  # Keep Markdown formatting
                    target=find_matching_target(sent, tgt_block)
                )
```

## Part 3: Advantages of This Approach

### 3.1 Simplicity Benefits

1. **No originalData complexity**: Markdown syntax stays in the text.
2. **Natural translator experience**: Translators see and work with readable Markdown.
3. **Straightforward round-trip**: Extract text, restore to Markdown blocks.
4. **Reduced XML verbosity**: Fewer nested elements and references.

### 3.2 Flexibility with `<s>` Elements

The `<s>` element approach provides:
- **Explicit control** over segmentation boundaries
- **ID preservation** for cross-referencing
- **Attribute support** for linguistic annotations
- **Backward compatibility** with documents lacking `<s>` elements

### 3.3 CAT Tool Compatibility

Modern CAT tools can:
- Display Markdown syntax as-is (readable by translators)
- Apply QA checks that understand Markdown patterns
- Preserve formatting during translation memory matching
- Export back to valid Markdown

## Part 4: Edge Cases and Solutions

### 4.1 Nested Formatting

For complex nested formatting:
```markdown
This is ***bold and italic*** text.
```

Keep as-is in XLIFF:
```xml
<source>This is ***bold and italic*** text.</source>
```

### 4.2 Inline HTML in Markdown

When Markdown contains inline HTML:
```markdown
This is <span class="highlight">highlighted</span> text.
```

Options:
1. **Keep as-is** (simplest): `<source>This is <span class="highlight">highlighted</span> text.</source>`
2. **Escape for XML**: `<source>This is &lt;span class="highlight"&gt;highlighted&lt;/span&gt; text.</source>`
3. **Use `<ph>` only for HTML** (hybrid approach)

### 4.3 Links with Titles

For links with title attributes:
```markdown
[Link text](https://example.com "Title here")
```

Preserve entirely:
```xml
<source>[Link text](https://example.com "Title here")</source>
```

Or store title in metadata if needed:
```xml
<mda:meta type="link-title" ref="seg1">Title here</mda:meta>
```

## Part 5: Recommendations

### 5.1 For Implementation

1. **Use markdown-it-py** for parsing (or markdown-it-pyrs for performance).
2. **Keep Markdown syntax inline** unless specific CAT tool requires `<pc>`/`<ph>`.
3. **Honor `<s>` elements** when present; auto-segment otherwise.
4. **Use `fs` attributes** for semantic tagging (better tool support).
5. **Minimize metadata** - only store what's essential for round-tripping.

### 5.2 For Standards Compliance

1. **Validate against XLIFF 2.1 schemas** including fs and mda modules.
2. **Test with target CAT tools** to ensure formatting preservation.
3. **Document the serialization choices** for downstream consumers.

### 5.3 For Future Enhancement

1. **Consider plugin development** for markdown-it-py to support `<s>` element parsing.
2. **Explore mdformat customization** for format-preserving serialization.
3. **Investigate XLIFF 2.2** features that might simplify Markdown handling.

## Conclusion

The optimal approach for serializing parallel Markdown prose in XLIFF 2.1 is to:

1. **Keep it simple**: Preserve Markdown formatting directly in segment text.
2. **Use `<s>` elements** for explicit segmentation control when available.
3. **Leverage `fs` attributes** for semantic markup without complexity.
4. **Avoid over-engineering**: Use `<pc>`/`<ph>` only when CAT tools demand it.