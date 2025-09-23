#!/usr/bin/env python3
"""
HTML to XLIFF Conversion Demo

This script demonstrates how to use the vexy-markliff library to convert
HTML content to XLIFF 2.1 format for translation workflows.

Usage:
    python html_to_xliff_demo.py
"""
# this_file: examples/html_to_xliff_demo.py

from vexy_markliff.core.element_classifier import HTMLElementClassifier
from vexy_markliff.core.format_style import FormatStyleSerializer
from vexy_markliff.core.inline_handler import InlineHandler
from vexy_markliff.core.skeleton_generator import SkeletonGenerator
from vexy_markliff.core.structure_handler import StructureHandler


def demo_element_classification():
    """Demonstrate HTML element classification."""

    classifier = HTMLElementClassifier()

    # Test various HTML elements
    test_elements = ["p", "div", "strong", "img", "table", "script", "h1"]

    for element in test_elements:
        classifier.classify(element)
        classifier.get_xliff_representation(element)


def demo_format_style_serialization():
    """Demonstrate Format Style attribute serialization."""

    serializer = FormatStyleSerializer()

    # Test attribute serialization
    test_attributes = {
        "class": "highlight important",
        "id": "main-content",
        "data-toggle": "tooltip",
        "href": "https://example.com?param=value",
        "disabled": "",
    }

    # Serialize attributes
    serialized = serializer.serialize_attributes(test_attributes)

    # Deserialize back
    serializer.deserialize_attributes(serialized)


def demo_skeleton_generation():
    """Demonstrate skeleton generation for XLIFF."""

    generator = SkeletonGenerator()

    # Generate placeholders for void elements
    img_ph_id, img_data_id = generator.generate_placeholder(
        "img", {"src": "image.jpg", "alt": "Sample image", "class": "responsive"}
    )

    br_ph_id, br_data_id = generator.generate_placeholder("br")


def demo_inline_element_handling():
    """Demonstrate inline element handling with markers."""

    handler = InlineHandler()

    # Create marker elements for inline content
    handler.create_mrk_element("strong", {"class": "emphasis"}, "Important text")

    # Create placeholder for void element
    handler.create_ph_element("img", {"src": "icon.png", "alt": "Icon"})


def demo_structure_preservation():
    """Demonstrate complex structure preservation."""

    handler = StructureHandler()

    # Classify different structure types
    structure_elements = ["table", "form", "video", "div"]

    for element in structure_elements:
        handler.classify_structure(element)
        handler.should_preserve_structure(element)


def demo_complete_workflow():
    """Demonstrate a complete HTML to XLIFF workflow."""

    # Sample HTML content

    # Initialize processors
    classifier = HTMLElementClassifier()
    serializer = FormatStyleSerializer()
    skeleton_gen = SkeletonGenerator()
    inline_handler = InlineHandler()
    structure_handler = StructureHandler()

    # Simulate processing workflow
    elements_found = ["article", "h1", "p", "strong", "img", "ul", "li", "em", "blockquote", "br"]
    for element in elements_found:
        classifier.classify(element)
        classifier.get_xliff_representation(element)

    structure_elements = ["article", "ul", "blockquote"]
    for element in structure_elements:
        structure_handler.should_preserve_structure(element)

    sample_attrs = {"class": "blog-post", "id": "post-1"}
    serializer.format_fs_element("article", sample_attrs)

    img_ph_id, img_data_id = skeleton_gen.generate_placeholder(
        "img", {"src": "xliff-diagram.png", "alt": "XLIFF workflow diagram", "class": "responsive"}
    )
    br_ph_id, br_data_id = skeleton_gen.generate_placeholder("br")

    inline_handler.create_mrk_element("strong", None, "powerful standard")
    inline_handler.create_mrk_element("em", None, "inline formatting")


def main():
    """Run all demonstration functions."""

    try:
        demo_element_classification()
        demo_format_style_serialization()
        demo_skeleton_generation()
        demo_inline_element_handling()
        demo_structure_preservation()
        demo_complete_workflow()

    except Exception:
        raise


if __name__ == "__main__":
    main()
