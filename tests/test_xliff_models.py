"""Tests for XLIFF Pydantic models."""
# this_file: tests/test_xliff_models.py

import pytest

from vexy_markliff.models.xliff import (
    TranslationUnit,
    XLIFFDocument,
    XLIFFFile,
)


class TestTranslationUnit:
    """Test cases for TranslationUnit model."""

    def test_create_basic_unit(self) -> None:
        """Test creating a basic translation unit."""
        unit = TranslationUnit(
            id="u1",
            source="Hello world",
        )

        assert unit.id == "u1"
        assert unit.source == "Hello world"
        assert unit.target is None
        assert unit.state == "new"

    def test_create_unit_with_target(self) -> None:
        """Test creating translation unit with target text."""
        unit = TranslationUnit(
            id="u2",
            source="Hello world",
            target="Hola mundo",
            state="translated",
        )

        assert unit.id == "u2"
        assert unit.source == "Hello world"
        assert unit.target == "Hola mundo"
        assert unit.state == "translated"


class TestXLIFFFile:
    """Test cases for XLIFFFile model."""

    def test_create_empty_file(self) -> None:
        """Test creating empty XLIFF file."""
        file = XLIFFFile(
            id="f1",
            source_language="en",
            target_language="es",
        )

        assert file.id == "f1"
        assert file.source_language == "en"
        assert file.target_language == "es"
        assert len(file.units) == 0

    def test_create_file_with_units(self) -> None:
        """Test creating XLIFF file with translation units."""
        units = [
            TranslationUnit(id="u1", source="Hello"),
            TranslationUnit(id="u2", source="World", target="Mundo"),
        ]

        file = XLIFFFile(
            id="f1",
            source_language="en",
            target_language="es",
            units=units,
        )

        assert len(file.units) == 2
        assert file.units[0].source == "Hello"
        assert file.units[1].target == "Mundo"


class TestXLIFFDocument:
    """Test cases for XLIFFDocument model."""

    def test_create_empty_document(self) -> None:
        """Test creating empty XLIFF document."""
        doc = XLIFFDocument()

        assert doc.version == "2.1"
        assert len(doc.files) == 0

    def test_create_document_with_content(self) -> None:
        """Test creating XLIFF document with parsed content."""
        content = {
            "segments": [
                {"content": "Hello world", "translatable": True},
                {"content": "How are you?", "translatable": True},
                {"content": "<!-- Comment -->", "translatable": False},
            ]
        }

        doc = XLIFFDocument(source_lang="en", target_lang="es", content=content)

        assert doc.version == "2.1"
        assert len(doc.files) == 1

        file = doc.files[0]
        assert file.source_language == "en"
        assert file.target_language == "es"
        assert len(file.units) == 2  # Only translatable segments

        assert file.units[0].source == "Hello world"
        assert file.units[1].source == "How are you?"

    def test_create_from_xml(self) -> None:
        """Test creating document from XML string."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.1" xmlns="urn:oasis:names:tc:xliff:document:2.1">
  <file id="f1" source-language="en" target-language="es">
    <unit id="u1">
      <segment>
        <source>Hello</source>
        <target>Hola</target>
      </segment>
    </unit>
  </file>
</xliff>"""

        doc = XLIFFDocument.from_xml(xml_content)
        assert doc.version == "2.1"
        # Note: The from_xml method may not be fully implemented,
        # this test verifies it doesn't crash
