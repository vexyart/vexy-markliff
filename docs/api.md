# Vexy Markliff API Documentation

This document provides comprehensive API documentation for the vexy-markliff package.

## Table of Contents

- [config](#config)
  - [ConversionMode](#conversionmode)
  - [StorageMode](#storagemode)
  - [OutputFormat](#outputformat)
  - [ConversionConfig](#conversionconfig)
- [vexy_markliff](#vexy-markliff)
  - [Config](#config)
- [cli](#cli)
  - [VexyMarkliffCLI](#vexymarkliffcli)
- [exceptions](#exceptions)
  - [VexyMarkliffError](#vexymarklifferror)
  - [ParsingError](#parsingerror)
  - [ValidationError](#validationerror)
  - [XLIFFValidationError](#xliffvalidationerror)
  - [ConversionError](#conversionerror)
  - [AlignmentError](#alignmenterror)
  - [ConfigurationError](#configurationerror)
  - [FileOperationError](#fileoperationerror)
- [structure_handler](#structure-handler)
  - [StructureType](#structuretype)
  - [ComplexStructure](#complexstructure)
  - [StructureHandler](#structurehandler)
- [skeleton_generator](#skeleton-generator)
  - [SkeletonGenerator](#skeletongenerator)
- [converter](#converter)
  - [VexyMarkliff](#vexymarkliff)
- [parser](#parser)
  - [MarkdownParser](#markdownparser)
  - [HTMLParser](#htmlparser)
- [format_style](#format-style)
  - [FormatStyleSerializer](#formatstyleserializer)
- [inline_handler](#inline-handler)
  - [InlineElement](#inlineelement)
  - [InlineHandler](#inlinehandler)
- [element_classifier](#element-classifier)
  - [ElementCategory](#elementcategory)
  - [HTMLElementClassifier](#htmlelementclassifier)
- [logging](#logging)
- [text](#text)
- [resilience](#resilience)
  - [CircuitState](#circuitstate)
  - [RetryConfig](#retryconfig)
  - [CircuitBreakerConfig](#circuitbreakerconfig)
  - [CircuitBreaker](#circuitbreaker)
  - [EnhancedErrorContext](#enhancederrorcontext)
- [validation](#validation)
- [xliff](#xliff)
  - [TranslationUnit](#translationunit)
  - [SkeletonFile](#skeletonfile)
  - [XLIFFFile](#xlifffile)
  - [XLIFFDocument](#xliffdocument)
- [document_pair](#document-pair)
  - [AlignmentMode](#alignmentmode)
  - [AlignmentQuality](#alignmentquality)
  - [DocumentSegment](#documentsegment)
  - [AlignedSegmentPair](#alignedsegmentpair)
  - [TwoDocumentPair](#twodocumentpair)
  - [Config](#config)

---

## config

Configuration management for vexy-markliff.

### ConversionMode

Supported conversion modes.

### StorageMode

Supported storage modes.

### OutputFormat

Supported output formats.

### ConversionConfig

Configuration for conversion operations with comprehensive validation.

This model provides secure configuration management with validation
for language codes, file paths, and all conversion settings.

Examples:
    >>> config = ConversionConfig()
    >>> config.source_language
    'en'

    >>> config = ConversionConfig(
    ...     source_language="fr",
    ...     target_language="de",
    ...     mode=ConversionMode.TWO_DOC
    ... )
    >>> config.mode
    'two-doc'

#### ConversionConfig.validate_language_code

```python
Validate language codes using ISO 639-1 pattern.

Args:
    v: Language code to validate

Returns:
    Validated language code

Raises:
    ValueError: If language code is invalid
```

```python
def validate_language_code(cls, v) -> str
```

#### ConversionConfig.validate_directory_path

```python
Validate directory paths for security.

Args:
    v: Directory path to validate

Returns:
    Validated Path object

Raises:
    ValueError: If path is insecure or invalid
```

```python
def validate_directory_path(cls, v) -> Optional[Path]
```

#### ConversionConfig.validate_markdown_extensions

```python
Validate markdown extensions.

Args:
    v: List of extension names

Returns:
    Validated extension list

Raises:
    ValueError: If extension is not supported
```

```python
def validate_markdown_extensions(cls, v) -> List[str]
```

#### ConversionConfig.validate_configuration_consistency

```python
Validate configuration consistency.

Returns:
    Validated configuration

Raises:
    ValueError: If configuration is inconsistent
```

```python
def validate_configuration_consistency() -> 'ConversionConfig'
```

#### ConversionConfig.from_file

```python
Load configuration from YAML file.

Args:
    config_path: Path to configuration file

Returns:
    Configuration instance

Raises:
    ConfigurationError: If file cannot be loaded or is invalid

Examples:
    >>> config = ConversionConfig.from_file(Path("config.yaml"))
```

```python
def from_file(cls, config_path) -> 'ConversionConfig'
```

#### ConversionConfig.to_file

```python
Save configuration to YAML file.

Args:
    config_path: Path where to save configuration

Raises:
    ConfigurationError: If file cannot be written
```

```python
def to_file(config_path) -> None
```

#### ConversionConfig.validate_file_path

```python
Validate a file path for security.

Args:
    file_path: File path to validate

Returns:
    Validated and resolved path

Raises:
    ConfigurationError: If path is insecure
```

```python
def validate_file_path(file_path) -> Path
```

---

## vexy_markliff

Core helpers for the vexy_markliff package.

### Config

Minimal configuration container used by ``process_data``.

---

## cli

Fire CLI interface for vexy-markliff.

### VexyMarkliffCLI

Command-line interface for Vexy Markliff conversion tools.

Global options:
    --verbose: Enable verbose debug logging
    --log-file: Path to log file for debug output

#### VexyMarkliffCLI.md2xliff

```python
Convert Markdown to XLIFF format.

Args:
    input_file: Path to input Markdown file
    output_file: Path to output XLIFF file
    source_lang: Source language code (default: en)
    target_lang: Target language code (default: es)
```

```python
def md2xliff(input_file, output_file, source_lang, target_lang) -> None
```

#### VexyMarkliffCLI.html2xliff

```python
Convert HTML to XLIFF format.

Args:
    input_file: Path to input HTML file
    output_file: Path to output XLIFF file
    source_lang: Source language code (default: en)
    target_lang: Target language code (default: es)
```

```python
def html2xliff(input_file, output_file, source_lang, target_lang) -> None
```

#### VexyMarkliffCLI.xliff2md

```python
Convert XLIFF to Markdown format.

Args:
    input_file: Path to input XLIFF file
    output_file: Path to output Markdown file
```

```python
def xliff2md(input_file, output_file) -> None
```

#### VexyMarkliffCLI.xliff2html

```python
Convert XLIFF to HTML format.

Args:
    input_file: Path to input XLIFF file
    output_file: Path to output HTML file
```

```python
def xliff2html(input_file, output_file) -> None
```

---

## exceptions

Custom exceptions for vexy-markliff.

### VexyMarkliffError

Base exception for all vexy-markliff errors.

### ParsingError

Raised when document parsing fails.

### ValidationError

Raised when document validation fails.

### XLIFFValidationError

Raised when XLIFF document validation fails.

### ConversionError

Raised when document conversion fails.

### AlignmentError

Raised when document alignment fails.

### ConfigurationError

Raised when configuration is invalid.

### FileOperationError

Raised when file operations fail.

---

## structure_handler

Complex structure handler for tables, forms, and media elements.

### StructureType

Types of complex structures.

### ComplexStructure

Represents a complex HTML structure.

### StructureHandler

Handle complex structures for XLIFF conversion.

#### StructureHandler.classify_structure

```python
Classify the structure type of an element.

Args:
    tag_name: HTML tag name

Returns:
    StructureType or None if not a complex structure
```

```python
def classify_structure(tag_name) -> StructureType | None
```

#### StructureHandler.create_unit_element

```python
Create a <unit> element for complex structure.

Args:
    tag_name: HTML tag name
    attributes: HTML attributes
    content: HTML content
    preserve_space: Whether to preserve whitespace
    use_cdata: Whether to use CDATA for content

Returns:
    XML Element for <unit>
```

```python
def create_unit_element(tag_name, attributes, content, preserve_space, use_cdata) -> Element
```

#### StructureHandler.create_group_element

```python
Create a <group> element for nested structures.

Args:
    tag_name: HTML tag name
    attributes: HTML attributes

Returns:
    XML Element for <group>
```

```python
def create_group_element(tag_name, attributes) -> Element
```

#### StructureHandler.process_table_structure

```python
Process a table structure for XLIFF.

Args:
    html_element: HTML table element
    cell_by_cell: Whether to break down by cells

Returns:
    XML Element for table structure
```

```python
def process_table_structure(html_element, cell_by_cell) -> Element
```

#### StructureHandler.process_form_structure

```python
Process a form structure for XLIFF.

Args:
    html_element: HTML form element

Returns:
    XML Element for form structure
```

```python
def process_form_structure(html_element) -> Element
```

#### StructureHandler.process_media_structure

```python
Process a media structure for XLIFF.

Args:
    html_element: HTML media element

Returns:
    XML Element for media structure
```

```python
def process_media_structure(html_element) -> Element
```

#### StructureHandler.should_preserve_structure

```python
Check if element should preserve its structure.

Args:
    tag_name: HTML tag name

Returns:
    True if structure should be preserved
```

```python
def should_preserve_structure(tag_name) -> bool
```

#### StructureHandler.reset

```python
Reset counters for new document.
```

```python
def reset() -> None
```

---

## skeleton_generator

Skeleton generator for XLIFF document structure preservation.

### SkeletonGenerator

Generate XLIFF skeleton files with placeholders for structure preservation.

#### SkeletonGenerator.generate_placeholder

```python
Generate a placeholder for a void or inline element.

Args:
    element_name: Name of the HTML element
    attributes: Element attributes
    element_type: Type of placeholder (standalone, open, close)

Returns:
    Tuple of (placeholder ID, data reference ID)

Examples:
    >>> generator = SkeletonGenerator()
    >>> ph_id, data_id = generator.generate_placeholder("img", {"src": "image.jpg", "alt": "Test"})
    >>> ph_id
    'ph-img001'
    >>> data_id
    'd1'
    >>> generator.original_data[data_id]
    '<img src="image.jpg" alt="Test"/>'
```

```python
def generate_placeholder(element_name, attributes, element_type) -> tuple[str, str]
```

#### SkeletonGenerator.create_skeleton_element

```python
Create a skeleton element for non-translatable structure.

Args:
    element_name: Name of the HTML element
    attributes: Element attributes
    content: Optional text content

Returns:
    XML Element for skeleton
```

```python
def create_skeleton_element(element_name, attributes, content) -> Element
```

#### SkeletonGenerator.generate_skeleton_document

```python
Generate a complete skeleton document.

Args:
    html_structure: List of skeleton elements

Returns:
    Serialized skeleton document
```

```python
def generate_skeleton_document(html_structure) -> str
```

#### SkeletonGenerator.create_placeholder_element

```python
Create a placeholder element for XLIFF.

Args:
    placeholder_id: Unique ID for the placeholder
    data_ref_id: Reference to original data
    can_copy: Whether placeholder can be copied
    can_delete: Whether placeholder can be deleted
    can_reorder: Whether placeholder can be reordered
    equiv_text: Equivalent text for accessibility

Returns:
    XML Element for placeholder
```

```python
def create_placeholder_element(placeholder_id, data_ref_id, can_copy, can_delete, can_reorder, equiv_text) -> Element
```

#### SkeletonGenerator.create_original_data_element

```python
Create originalData element with all data references.

Returns:
    XML Element for originalData or None if no data
```

```python
def create_original_data_element() -> Element | None
```

#### SkeletonGenerator.should_be_skeleton

```python
Check if element should be in skeleton only.

Args:
    element_name: Name of the HTML element

Returns:
    True if element should be skeleton-only
```

```python
def should_be_skeleton(element_name) -> bool
```

#### SkeletonGenerator.should_be_placeholder

```python
Check if element should become a placeholder.

Args:
    element_name: Name of the HTML element

Returns:
    True if element should be a placeholder
```

```python
def should_be_placeholder(element_name) -> bool
```

#### SkeletonGenerator.reset

```python
Reset counters and data for new document.
```

```python
def reset() -> None
```

#### SkeletonGenerator.generate_inline_code_placeholder

```python
Generate inline code placeholder for paired tags.

Args:
    element_name: Name of the HTML element
    element_type: Type of code (open/close)
    attributes: Element attributes (for open tags)

Returns:
    Tuple of (placeholder element, data reference ID)
```

```python
def generate_inline_code_placeholder(element_name, element_type, attributes) -> tuple[Element, str]
```

---

## converter

Main conversion orchestrator.

### VexyMarkliff

Main converter class for handling bidirectional Markdown/HTML to XLIFF conversion.

#### VexyMarkliff.markdown_to_xliff

```python
Convert Markdown content to XLIFF format.

Args:
    markdown_content: Markdown content to convert
    source_lang: Source language code
    target_lang: Target language code

Returns:
    XLIFF formatted string

Raises:
    ValidationError: If input validation fails
```

```python
def markdown_to_xliff(markdown_content, source_lang, target_lang) -> str
```

#### VexyMarkliff.html_to_xliff

```python
Convert HTML content to XLIFF format.

Args:
    html_content: HTML content to convert
    source_lang: Source language code
    target_lang: Target language code

Returns:
    XLIFF formatted string

Raises:
    ValidationError: If input validation fails
```

```python
def html_to_xliff(html_content, source_lang, target_lang) -> str
```

#### VexyMarkliff.xliff_to_markdown

```python
Convert XLIFF content back to Markdown format.

Args:
    xliff_content: XLIFF content to convert

Returns:
    Markdown formatted string

Raises:
    ValidationError: If input validation fails
```

```python
def xliff_to_markdown(xliff_content) -> str
```

#### VexyMarkliff.xliff_to_html

```python
Convert XLIFF content back to HTML format.

Args:
    xliff_content: XLIFF content to convert

Returns:
    HTML formatted string

Raises:
    ValidationError: If input validation fails
```

```python
def xliff_to_html(xliff_content) -> str
```

#### VexyMarkliff.process_parallel

```python
Process parallel source and target documents for alignment.

Args:
    source_content: Source document content
    target_content: Target document content
    mode: Alignment mode

Returns:
    Dictionary containing alignment results

Raises:
    ValidationError: If input validation fails
```

```python
def process_parallel(source_content, target_content, mode) -> dict[str, Any]
```

---

## parser

HTML and Markdown parsing utilities.

### MarkdownParser

Parser for Markdown content using markdown-it-py.

#### MarkdownParser.parse

```python
Parse Markdown content and return structured data.

Args:
    content: Markdown content to parse

Returns:
    Parsed markdown data including tokens, HTML, and metadata

Raises:
    ParsingError: If Markdown parsing fails
```

```python
def parse(content) -> dict[str, Any]
```

#### MarkdownParser.render_html

```python
Render Markdown content to HTML.

Args:
    content: Markdown content to render

Returns:
    Rendered HTML string

Raises:
    ParsingError: If rendering fails
```

```python
def render_html(content) -> str
```

### HTMLParser

Parser for HTML content using lxml.

#### HTMLParser.parse

```python
Parse HTML content and return structured data.

Args:
    content: HTML content to parse

Returns:
    Parsed HTML data including tree, elements, and text content

Raises:
    ParsingError: If HTML parsing fails
```

```python
def parse(content) -> dict[str, Any]
```

---

## format_style

Format Style attribute serialization for XLIFF.

### FormatStyleSerializer

Serialize HTML attributes for XLIFF Format Style module.

#### FormatStyleSerializer.escape_value

```python
Escape special characters in attribute values.

Args:
    value: Attribute value to escape

Returns:
    Escaped value
```

```python
def escape_value(value) -> str
```

#### FormatStyleSerializer.unescape_value

```python
Unescape special characters in attribute values.

Args:
    value: Escaped attribute value

Returns:
    Unescaped value
```

```python
def unescape_value(value) -> str
```

#### FormatStyleSerializer.serialize_attributes

```python
Serialize HTML attributes to fs:subFs format.

Format: name1,value1\name2,value2\name3,value3
- Comma separates name from value
- Backslash separates attribute pairs
- Literal commas escaped as \,
- Literal backslashes escaped as \\
- Empty values become name,

Args:
    attributes: Dictionary of attribute name-value pairs

Returns:
    Serialized fs:subFs string

Examples:
    >>> serializer = FormatStyleSerializer()
    >>> serializer.serialize_attributes({"class": "test", "id": "main"})
    'class,test\\id,main'
    >>> serializer.serialize_attributes({"href": "http://example.com", "target": "_blank"})
    'href,http://example.com\\target,_blank'
    >>> serializer.serialize_attributes({"disabled": ""})
    'disabled,'
    >>> serializer.serialize_attributes({})
    ''
```

```python
def serialize_attributes(attributes) -> str
```

#### FormatStyleSerializer.deserialize_attributes

```python
Deserialize fs:subFs format to HTML attributes.

Args:
    subfs: Serialized fs:subFs string

Returns:
    Dictionary of attribute name-value pairs

Examples:
    >>> serializer = FormatStyleSerializer()
    >>> serializer.deserialize_attributes('class,test\\id,main')
    {'class': 'test', 'id': 'main'}
    >>> serializer.deserialize_attributes('href,http://example.com\\target,_blank')
    {'href': 'http://example.com', 'target': '_blank'}
    >>> serializer.deserialize_attributes('disabled,')
    {'disabled': ''}
    >>> serializer.deserialize_attributes('')
    {}
```

```python
def deserialize_attributes(subfs) -> dict[str, str]
```

#### FormatStyleSerializer.format_fs_element

```python
Format an HTML element for XLIFF Format Style attributes.

Args:
    tag_name: HTML element tag name
    attributes: Optional dictionary of HTML attributes

Returns:
    Dictionary with fs:fs and optionally fs:subFs attributes

Raises:
    ValidationError: If input validation fails
```

```python
def format_fs_element(tag_name, attributes) -> dict[str, str]
```

#### FormatStyleSerializer.serialize_inline_attributes

```python
Serialize inline element attributes for mrk elements.

Args:
    tag_name: HTML element tag name
    attributes: Optional dictionary of HTML attributes

Returns:
    Combined fs:fs and fs:subFs value for mrk element
```

```python
def serialize_inline_attributes(tag_name, attributes) -> str
```

#### FormatStyleSerializer.deserialize_inline_attributes

```python
Deserialize combined inline attributes from mrk element.

Args:
    combined: Combined fs:fs#fs:subFs value

Returns:
    Tuple of (tag_name, attributes)
```

```python
def deserialize_inline_attributes(combined) -> tuple[str, dict[str, str]]
```

---

## inline_handler

Inline element handler for XLIFF conversion.

### InlineElement

Represents an inline element for XLIFF conversion.

### InlineHandler

Handle inline elements for XLIFF conversion.

#### InlineHandler.create_mrk_element

```python
Create a <mrk> element for inline content.

Args:
    tag_name: HTML tag name
    attributes: HTML attributes
    content: Text content

Returns:
    XML Element for <mrk>

Examples:
    >>> handler = InlineHandler()
    >>> mrk = handler.create_mrk_element("strong", {"class": "highlight"}, "Important text")
    >>> mrk.get("id")
    'm1'
    >>> mrk.get("fs:fs")
    'strong'
    >>> mrk.text
    'Important text'
```

```python
def create_mrk_element(tag_name, attributes, content) -> Element
```

#### InlineHandler.create_ph_element

```python
Create a <ph> element for void/placeholder content.

Args:
    tag_name: HTML tag name
    attributes: HTML attributes

Returns:
    XML Element for <ph>
```

```python
def create_ph_element(tag_name, attributes) -> Element
```

#### InlineHandler.create_paired_code_elements

```python
Create paired code elements (pc/ec) for inline elements.

Args:
    tag_name: HTML tag name
    attributes: HTML attributes

Returns:
    Tuple of (opening pc element, closing ec element)
```

```python
def create_paired_code_elements(tag_name, attributes) -> tuple[Element, Element]
```

#### InlineHandler.process_inline_content

```python
Process HTML element into inline XLIFF elements.

Args:
    html_element: HTML element to process
    depth: Current recursion depth (for preventing stack overflow)

Returns:
    List of XLIFF inline elements

Raises:
    RecursionError: If maximum recursion depth is exceeded
```

```python
def process_inline_content(html_element, depth) -> list[Element]
```

#### InlineHandler.is_inline_element

```python
Check if element is an inline element.

Args:
    tag_name: HTML tag name

Returns:
    True if inline element
```

```python
def is_inline_element(tag_name) -> bool
```

#### InlineHandler.should_use_mrk

```python
Check if element should use <mrk> wrapper.

Args:
    tag_name: HTML tag name

Returns:
    True if should use <mrk>
```

```python
def should_use_mrk(tag_name) -> bool
```

#### InlineHandler.should_use_ph

```python
Check if element should use <ph> placeholder.

Args:
    tag_name: HTML tag name

Returns:
    True if should use <ph>
```

```python
def should_use_ph(tag_name) -> bool
```

#### InlineHandler.reset

```python
Reset counters for new document.
```

```python
def reset() -> None
```

#### InlineHandler.extract_inline_elements

```python
Extract inline elements from mixed content.

Args:
    text: Plain text content
    elements: List of HTML elements

Returns:
    List of InlineElement objects
```

```python
def extract_inline_elements(text, elements) -> list[InlineElement]
```

#### InlineHandler.wrap_text_with_inline_markers

```python
Wrap text content with inline markers.

Args:
    text: Plain text to wrap
    inline_elements: List of inline elements to insert

Returns:
    XML Element containing text with inline markers
```

```python
def wrap_text_with_inline_markers(text, inline_elements) -> Element
```

---

## element_classifier

HTML element classification for XLIFF conversion.

### ElementCategory

Categories for HTML elements in XLIFF conversion.

### HTMLElementClassifier

Classify HTML elements for XLIFF conversion.

#### HTMLElementClassifier.classify

```python
Classify an HTML element.

Args:
    element_name: Name of the HTML element (lowercase)

Returns:
    ElementCategory for the element

Examples:
    >>> classifier = HTMLElementClassifier()
    >>> classifier.classify("p")
    ElementCategory.FLOW_TEXT
    >>> classifier.classify("div")
    ElementCategory.SECTIONING
    >>> classifier.classify("strong")
    ElementCategory.INLINE
    >>> classifier.classify("img")
    ElementCategory.VOID
```

```python
def classify(element_name) -> ElementCategory
```

#### HTMLElementClassifier.requires_whitespace_preservation

```python
Check if element requires preserving whitespace.

Args:
    element_name: Name of the HTML element

Returns:
    True if whitespace should be preserved
```

```python
def requires_whitespace_preservation(element_name) -> bool
```

#### HTMLElementClassifier.is_translatable_unit

```python
Check if element should become a translation unit.

Args:
    element_name: Name of the HTML element

Returns:
    True if element should become a unit
```

```python
def is_translatable_unit(element_name) -> bool
```

#### HTMLElementClassifier.is_group_element

```python
Check if element should become a group.

Args:
    element_name: Name of the HTML element

Returns:
    True if element should become a group
```

```python
def is_group_element(element_name) -> bool
```

#### HTMLElementClassifier.is_inline_element

```python
Check if element is inline and should become a marker.

Args:
    element_name: Name of the HTML element

Returns:
    True if element should become a marker
```

```python
def is_inline_element(element_name) -> bool
```

#### HTMLElementClassifier.is_void_element

```python
Check if element is void and should become a placeholder.

Args:
    element_name: Name of the HTML element

Returns:
    True if element should become a placeholder
```

```python
def is_void_element(element_name) -> bool
```

#### HTMLElementClassifier.get_xliff_representation

```python
Get the XLIFF representation type for an element.

Args:
    element_name: Name of the HTML element

Returns:
    XLIFF representation type (unit, group, marker, placeholder, skeleton)

Examples:
    >>> classifier = HTMLElementClassifier()
    >>> classifier.get_xliff_representation("p")
    'unit'
    >>> classifier.get_xliff_representation("div")
    'group'
    >>> classifier.get_xliff_representation("strong")
    'marker'
    >>> classifier.get_xliff_representation("img")
    'placeholder'
    >>> classifier.get_xliff_representation("script")
    'skeleton'
```

```python
def get_xliff_representation(element_name) -> str
```

#### HTMLElementClassifier.get_segmentation_strategy

```python
Get the segmentation strategy for an element.

Args:
    element_name: Name of the HTML element

Returns:
    Segmentation strategy (sentence, element, preserve)
```

```python
def get_segmentation_strategy(element_name) -> str
```

#### HTMLElementClassifier.should_extract_attributes

```python
Check if element attributes should be extracted.

Args:
    element_name: Name of the HTML element

Returns:
    True if attributes should be extracted
```

```python
def should_extract_attributes(element_name) -> bool
```

#### HTMLElementClassifier.get_important_attributes

```python
Get list of important attributes for an element.

Args:
    element_name: Name of the HTML element

Returns:
    Tuple of important attribute names (cached as tuple for immutability)
```

```python
def get_important_attributes(element_name) -> tuple[str, ...]
```

---

## logging

Logging utilities for vexy-markliff.

---

## text

Text processing utilities with graceful degradation for optional dependencies.

---

## resilience

Error recovery and resilience patterns for vexy_markliff.

### CircuitState

Circuit breaker states.

### RetryConfig

Configuration for retry mechanisms.

### CircuitBreakerConfig

Configuration for circuit breaker.

### CircuitBreaker

Circuit breaker implementation for fault tolerance.

### EnhancedErrorContext

Enhanced error context for better error messages.

---

## validation

Input validation utilities for vexy-markliff.

---

## xliff

Pydantic models for XLIFF 2.1 documents.

### TranslationUnit

Represents a translation unit in XLIFF.

### SkeletonFile

Represents external skeleton file information.

### XLIFFFile

Represents a file element in XLIFF document.

### XLIFFDocument

Represents a complete XLIFF 2.1 document.

#### XLIFFDocument.add_file

```python
Add a new file to the XLIFF document.
```

```python
def add_file(file_id, source_lang, target_lang, original) -> XLIFFFile
```

#### XLIFFDocument.add_unit

```python
Add a translation unit to a specific file.
```

```python
def add_unit(file_id, unit_id, source, target) -> TranslationUnit
```

#### XLIFFDocument.to_xml

```python
Convert the XLIFF document to XML string.
```

```python
def to_xml() -> str
```

---

## document_pair

Pydantic models for parallel document handling.

### AlignmentMode

Alignment modes for two-document processing.

### AlignmentQuality

Quality indicators for document alignment.

### DocumentSegment

Represents a segment of a document.

### AlignedSegmentPair

Represents a pair of aligned segments from source and target documents.

#### AlignedSegmentPair.validate_alignment_type

```python
Validate alignment type.
```

```python
def validate_alignment_type(cls, v) -> str
```

### TwoDocumentPair

Model for handling parallel source and target documents.

#### TwoDocumentPair.calculate_alignment_quality

```python
Calculate overall alignment quality based on aligned pairs.
```

```python
def calculate_alignment_quality() -> AlignmentQuality
```

#### TwoDocumentPair.add_aligned_pair

```python
Add an aligned segment pair.
```

```python
def add_aligned_pair(source_segment, target_segment, confidence) -> None
```

#### TwoDocumentPair.get_alignment_summary

```python
Get a summary of the alignment.
```

```python
def get_alignment_summary() -> dict[str, Any]
```

### Config

Pydantic config.

---
