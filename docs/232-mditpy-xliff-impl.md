---
author: Unknown
date: Unknown
id: Unknown
title: 'Technical Implementation Guide: Markdown-it-py to XLIFF 2.1'
type: Technical Guide
---

# Technical Implementation Guide: Markdown-it-py to XLIFF 2.1

```python
from markdown_it import MarkdownIt
from markdown_it.token import Token
import re
from typing import List, Tuple, Optional
import spacy
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Initialize parser
md = MarkdownIt("commonmark")

# Parse markdown
text = """# Hello World

This is a paragraph with *italic* and **bold** text.

- Item 1
- Item 2
"""

tokens = md.parse(text)

# Token structure example
for token in tokens:
    print(f"Type: {token.type}, Tag: {token.tag}, Nesting: {token.nesting}")
    if token.content:
        print(f"  Content: {token.content}")
    if token.children:
        print(f"  Children: {len(token.children)} inline tokens")

# Key token properties:
# - type: 'paragraph_open', 'paragraph_close', 'inline', 'heading_open', etc.
# - tag: HTML tag equivalent ('p', 'h1', 'ul', etc.)
# - nesting: 1 (opening), -1 (closing), 0 (self-closing)
# - content: Text content (for inline tokens)
# - children: List of child tokens (for inline tokens)
# - attrs: List of [name, value] pairs
# - level: Nesting level
# - markup: Original Markdown markup used

def analyze_token_stream(tokens):
    """Analyze token structure for XLIFF conversion"""
    blocks = []
    current_block = None
    
    for token in tokens:
        if token.nesting == 1:  # Opening tag
            current_block = {
                'type': token.type,
                'tag': token.tag,
                'attrs': dict(token.attrs) if token.attrs else {},
                'content': [],
                'tokens': []
            }
        elif token.nesting == -1:  # Closing tag
            if current_block:
                blocks.append(current_block)
                current_block = None
        elif token.type == 'inline':
            if current_block:
                current_block['content'].append(token.content)
                current_block['tokens'].append(token)
    
    return blocks

class SentenceElement:
    def __init__(self, id: str, content: str, attrs: dict = None):
        self.id = id
        self.content = content
        self.attrs = attrs or {}

def extract_s_elements(text: str) -> List[SentenceElement]:
    """Extract <s> elements from Markdown text"""
    pattern = r'<s(?:\s+([^>]+))?>(.+?)</s>'
    elements = []
    
    for match in re.finditer(pattern, text, re.DOTALL):
        attrs_str = match.group(1) or ""
        content = match.group(2)
        
        # Parse attributes
        attrs = {}
        id_match = re.search(r'id="([^"]+)"', attrs_str)
        if id_match:
            attrs['id'] = id_match.group(1)
        
        # Extract other attributes
        for attr_match in re.finditer(r'(\w+)="([^"]+)"', attrs_str):
            if attr_match.group(1) != 'id':
                attrs[attr_match.group(1)] = attr_match.group(2)
        
        elements.append(SentenceElement(
            id=attrs.get('id', None),
            content=content.strip(),
            attrs=attrs
        ))
    
    return elements

def has_s_elements(text: str) -> bool:
    """Check if text contains <s> elements"""
    return bool(re.search(r'<s(?:\s+[^>]+)?>', text))

def segment_sentences(text: str) -> List[str]:
    """Segment text into sentences when no <s> elements present"""
    # Simple rule-based approach
    import re
    
    # Handle common abbreviations
    text = re.sub(r'\b(Mr|Mrs|Dr|Ms|Prof|Sr|Jr)\.\s*', r'\1<DOT> ', text)
    
    # Split on sentence endings
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Restore dots
    sentences = [s.replace('<DOT>', '.') for s in sentences]
    
    return [s.strip() for s in sentences if s.strip()]

# Or use spacy for better accuracy
def segment_sentences_nlp(text: str, lang='en') -> List[str]:
    """Advanced sentence segmentation using spaCy"""
    try:
        nlp = spacy.load(f"{lang}_core_web_sm")
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents]
    except:
        # Fallback to rule-based
        return segment_sentences(text)

class XLIFFBuilder:
    """Builder for XLIFF 2.1 documents"""
    
    def __init__(self, src_lang: str, trg_lang: str, original: str = None):
        self.xliff = Element('xliff', {
            'xmlns': 'urn:oasis:names:tc:xliff:document:2.1',
            'xmlns:fs': 'urn:oasis:names:tc:xliff:fs:2.0',
            'xmlns:mda': 'urn:oasis:names:tc:xliff:metadata:2.0',
            'version': '2.1'
        })
        
        self.file = SubElement(self.xliff, 'file', {
            'id': self._generate_file_id(original),
            'srcLang': src_lang,
            'trgLang': trg_lang
        })
        
        if original:
            self.file.set('original', original)
        
        self.unit_counter = 0
        self.segment_counter = 0
    
    def _generate_file_id(self, path: str = None) -> str:
        if path:
            import os
            return os.path.splitext(os.path.basename(path))[0]
        return 'document'
    
    def add_unit(self, unit_type: str, fs: str = None) -> Element:
        """Add a new unit to the file"""
        self.unit_counter += 1
        unit = SubElement(self.file, 'unit', {
            'id': f"{unit_type}-{self.unit_counter}"
        })
        
        if fs:
            unit.set('fs', fs)
        
        return unit
    
    def add_segment(self, unit: Element, source: str, target: str = None, 
                    segment_id: str = None, fs: str = None) -> Element:
        """Add a segment to a unit"""
        self.segment_counter += 1
        
        segment = SubElement(unit, 'segment', {
            'id': segment_id or f"seg-{self.segment_counter}"
        })
        
        if fs:
            segment.set('fs', fs)
        
        source_elem = SubElement(segment, 'source')
        source_elem.text = source
        
        if target:
            target_elem = SubElement(segment, 'target')
            target_elem.text = target
        
        return segment
    
    def add_metadata(self, element: Element, category: str, meta_items: dict):
        """Add metadata to an element"""
        metadata = SubElement(element, '{urn:oasis:names:tc:xliff:metadata:2.0}metadata')
        metagroup = SubElement(metadata, '{urn:oasis:names:tc:xliff:metadata:2.0}metaGroup', {
            'category': category
        })
        
        for key, value in meta_items.items():
            meta = SubElement(metagroup, '{urn:oasis:names:tc:xliff:metadata:2.0}meta', {
                'type': key
            })
            meta.text = str(value)
    
    def to_string(self, pretty: bool = True) -> str:
        """Convert to XML string"""
        xml_str = tostring(self.xliff, encoding='unicode')
        
        if pretty:
            dom = minidom.parseString(xml_str)
            return dom.toprettyxml(indent="  ")
        
        return xml_str

class MarkdownToXLIFF:
    """Convert parallel Markdown documents to XLIFF 2.1"""
    
    def __init__(self, src_lang: str, trg_lang: str):
        self.src_lang = src_lang
        self.trg_lang = trg_lang
        self.md = MarkdownIt("commonmark")
    
    def convert(self, source_md: str, target_md: str, source_path: str = None) -> str:
        """Convert parallel Markdown to XLIFF"""
        # Parse both documents
        source_tokens = self.md.parse(source_md)
        target_tokens = self.md.parse(target_md)
        
        # Create XLIFF builder
        xliff = XLIFFBuilder(self.src_lang, self.trg_lang, source_path)
        
        # Process token pairs
        src_blocks = self._extract_blocks(source_tokens)
        trg_blocks = self._extract_blocks(target_tokens)
        
        for src_block, trg_block in zip(src_blocks, trg_blocks):
            self._process_block_pair(xliff, src_block, trg_block)
        
        return xliff.to_string()
    
    def _extract_blocks(self, tokens: List[Token]) -> List[dict]:
        """Extract block-level elements from token stream"""
        blocks = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token.nesting == 1:  # Opening tag
                block = {
                    'type': token.type.replace('_open', ''),
                    'tag': token.tag,
                    'content': '',
                    'has_s_elements': False
                }
                
                # Find corresponding inline token
                i += 1
                while i < len(tokens) and tokens[i].nesting != -1:
                    if tokens[i].type == 'inline':
                        block['content'] = tokens[i].content
                        block['has_s_elements'] = has_s_elements(tokens[i].content)
                    i += 1
                
                blocks.append(block)
            
            i += 1
        
        return blocks
    
    def _process_block_pair(self, xliff: XLIFFBuilder, src_block: dict, trg_block: dict):
        """Process a pair of parallel blocks"""
        # Determine fs attribute based on tag
        fs_map = {
            'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h5', 'h6': 'h6',
            'p': 'p', 'ul': 'ul', 'ol': 'ol', 'li': 'li', 'pre': 'pre',
            'blockquote': 'blockquote', 'table': 'table'
        }
        
        fs = fs_map.get(src_block['tag'], src_block['tag'])
        
        # Create unit
        unit = xliff.add_unit(src_block['type'], fs)
        
        # Check for <s> elements
        if src_block['has_s_elements']:
            # Process explicit sentence elements
            src_sentences = extract_s_elements(src_block['content'])
            trg_sentences = extract_s_elements(trg_block['content'])
            
            # Add metadata to indicate s elements present
            xliff.add_metadata(unit, 'markdown', {'has-s-elements': 'true'})
            
            for src_s, trg_s in zip(src_sentences, trg_sentences):
                xliff.add_segment(
                    unit,
                    source=src_s.content,
                    target=trg_s.content if trg_s else None,
                    segment_id=src_s.id or None,
                    fs='s'  # Mark as sentence
                )
        else:
            # Auto-segment by sentences
            src_sentences = segment_sentences(src_block['content'])
            trg_sentences = segment_sentences(trg_block['content'])
            
            # Handle mismatched sentence counts
            max_sentences = max(len(src_sentences), len(trg_sentences))
            
            for i in range(max_sentences):
                src_sent = src_sentences[i] if i < len(src_sentences) else ''
                trg_sent = trg_sentences[i] if i < len(trg_sentences) else ''
                
                xliff.add_segment(unit, source=src_sent, target=trg_sent)

# Example usage
def main():
    source_markdown = """# Document Title

<s id="intro-1">This is the *first* sentence with emphasis.</s> <s id="intro-2">This is the **second** with bold.</s>

This paragraph has no explicit sentences. It will be auto-segmented. Here's a [link](https://example.com).

## Features

- Item with `inline code`
- Item with ***bold italic***
"""

    target_markdown = """# Dokumenttitel

<s id="intro-1">Dies ist der *erste* Satz mit Betonung.</s> <s id="intro-2">Dies ist der **zweite** mit Fettdruck.</s>

Dieser Absatz hat keine expliziten Sätze. Er wird automatisch segmentiert. Hier ist ein [Link](https://example.com).

## Funktionen

- Element mit `Inline-Code`
- Element mit ***fett kursiv***
"""

    # Convert to XLIFF
    converter = MarkdownToXLIFF('en', 'de')
    xliff_output = converter.convert(source_markdown, target_markdown, 'document.md')
    
    # Save to file
    with open('output.xliff', 'w', encoding='utf-8') as f:
        f.write(xliff_output)
    
    print("XLIFF file generated successfully!")

if __name__ == "__main__":
    main()

def xliff_to_markdown(xliff_path: str) -> Tuple[str, str]:
    """Convert XLIFF back to source and target Markdown"""
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(xliff_path)
    root = tree.getroot()
    
    # Namespace handling
    ns = {
        'xlf': 'urn:oasis:names:tc:xliff:document:2.1',
        'fs': 'urn:oasis:names:tc:xliff:fs:2.0',
        'mda': 'urn:oasis:names:tc:xliff:metadata:2.0'
    }
    
    source_md = []
    target_md = []
    
    for unit in root.findall('.//xlf:unit', ns):
        fs = unit.get('fs', '')
        
        # Reconstruct block based on fs
        block_map = {
            'h1': ('# ', ''),
            'h2': ('## ', ''),
            'h3': ('### ', ''),
            'h4': ('#### ', ''),
            'h5': ('##### ', ''),
            'h6': ('###### ', ''),
            'p': ('', ''),
            'li': ('- ', ''),
            'pre': ('```\n', '\n```')
        }
        
        prefix, suffix = block_map.get(fs, ('', ''))
        
        # Collect segments
        src_segments = []
        trg_segments = []
        
        for segment in unit.findall('xlf:segment', ns):
            src = segment.find('xlf:source', ns)
            trg = segment.find('xlf:target', ns)
            
            if src is not None and src.text:
                # Check if this was an <s> element
                if segment.get('fs') == 's' and segment.get('id'):
                    src_segments.append(f'<s id="{segment.get("id")}">{src.text}</s>')
                else:
                    src_segments.append(src.text)
            
            if trg is not None and trg.text:
                if segment.get('fs') == 's' and segment.get('id'):
                    trg_segments.append(f'<s id="{segment.get("id")}">{trg.text}</s>')
                else:
                    trg_segments.append(trg.text)
        
        # Reconstruct blocks
        if src_segments:
            source_md.append(prefix + ' '.join(src_segments) + suffix)
        if trg_segments:
            target_md.append(prefix + ' '.join(trg_segments) + suffix)
        
        # Add blank line between blocks
        source_md.append('')
        target_md.append('')
    
    return '\n'.join(source_md).strip(), '\n'.join(target_md).strip()
```