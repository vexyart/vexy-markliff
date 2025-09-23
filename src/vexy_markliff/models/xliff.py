"""Simple Pydantic models for XLIFF 2.1 documents."""
# this_file: src/vexy_markliff/models/xliff.py

from typing import Any, Dict, List, Optional

from lxml import etree
from pydantic import BaseModel, Field

from vexy_markliff.exceptions import ValidationError
from vexy_markliff.utils import get_logger

logger = get_logger(__name__)


class TranslationUnit(BaseModel):
    """Represents a translation unit in XLIFF."""

    id: str = Field(..., description="Unique identifier for the translation unit")
    source: str = Field(..., description="Source text content")
    target: str | None = Field(None, description="Target text content")
    state: str = Field("new", description="Translation state")


class XLIFFFile(BaseModel):
    """Represents a file element in XLIFF document."""

    id: str = Field(..., description="File identifier")
    source_language: str = Field(..., description="Source language code")
    target_language: str = Field(..., description="Target language code")
    units: list[TranslationUnit] = Field(default_factory=list, description="Translation units")


class XLIFFDocument(BaseModel):
    """Represents complete XLIFF 2.1 document."""

    version: str = Field("2.1", description="XLIFF version")
    files: list[XLIFFFile] = Field(default_factory=list, description="XLIFF files")

    def __init__(self, source_lang: str = "en", target_lang: str = "es", content: dict[str, Any] | None = None, **data):
        """Initialize XLIFF document with content.

        Args:
            source_lang: Source language code
            target_lang: Target language code
            content: Parsed content from parser
            **data: Additional data for Pydantic
        """
        super().__init__(**data)

        if content:
            # Create translation units from parsed content
            units = []
            segments = content.get("segments", [])

            for i, segment in enumerate(segments):
                if segment.get("translatable", True):
                    unit = TranslationUnit(id=f"unit_{i + 1}", source=segment["content"], state="new")
                    units.append(unit)

            # Create file
            xliff_file = XLIFFFile(id="file_1", source_language=source_lang, target_language=target_lang, units=units)
            self.files = [xliff_file]

    @classmethod
    def from_xml(cls, xml_content: str) -> "XLIFFDocument":
        """Create XLIFF document from XML string.

        Args:
            xml_content: XLIFF XML content

        Returns:
            XLIFFDocument instance

        Raises:
            ValidationError: If XML is invalid
        """
        try:
            root = etree.fromstring(xml_content.encode("utf-8"))

            # Define namespace
            ns = {"xliff": "urn:oasis:names:tc:xliff:document:2.1"}

            # Extract basic XLIFF structure
            files = []
            for file_elem in root.xpath("//xliff:file", namespaces=ns):
                source_lang = file_elem.get("source-language", "en")
                target_lang = file_elem.get("target-language", "es")

                units = []
                for unit_elem in file_elem.xpath(".//xliff:trans-unit", namespaces=ns):
                    unit_id = unit_elem.get("id", f"unit_{len(units) + 1}")

                    source_elem = unit_elem.find("xliff:source", namespaces=ns)
                    target_elem = unit_elem.find("xliff:target", namespaces=ns)

                    source_text = source_elem.text if source_elem is not None else ""
                    target_text = target_elem.text if target_elem is not None else None

                    unit = TranslationUnit(
                        id=unit_id, source=source_text, target=target_text, state=unit_elem.get("state", "new")
                    )
                    units.append(unit)

                xliff_file = XLIFFFile(
                    id=file_elem.get("id", "file_1"),
                    source_language=source_lang,
                    target_language=target_lang,
                    units=units,
                )
                files.append(xliff_file)

            return cls(files=files)

        except Exception as e:
            logger.error(f"Failed to parse XLIFF XML: {e}")
            msg = f"Invalid XLIFF XML: {e}"
            raise ValidationError(msg)

    def to_xml(self) -> str:
        """Convert XLIFF document to XML string.

        Returns:
            XLIFF 2.1 compliant XML string
        """
        try:
            # Create XLIFF root element
            xliff = etree.Element("xliff")
            xliff.set("version", self.version)
            xliff.set("xmlns", "urn:oasis:names:tc:xliff:document:2.1")

            # Add files
            for xliff_file in self.files:
                file_elem = etree.SubElement(xliff, "file")
                file_elem.set("id", xliff_file.id)
                file_elem.set("source-language", xliff_file.source_language)
                file_elem.set("target-language", xliff_file.target_language)

                # Add units
                for unit in xliff_file.units:
                    unit_elem = etree.SubElement(file_elem, "trans-unit")
                    unit_elem.set("id", unit.id)
                    unit_elem.set("state", unit.state)

                    # Add source
                    source_elem = etree.SubElement(unit_elem, "source")
                    source_elem.text = unit.source

                    # Add target if present
                    if unit.target:
                        target_elem = etree.SubElement(unit_elem, "target")
                        target_elem.text = unit.target

            # Convert to string
            return etree.tostring(xliff, encoding="unicode", pretty_print=True)

        except Exception as e:
            logger.error(f"Failed to generate XLIFF XML: {e}")
            msg = f"Failed to create XLIFF XML: {e}"
            raise ValidationError(msg)

    @property
    def content(self) -> dict[str, Any]:
        """Get structured content representation for compatibility.

        Returns:
            Structured content dict
        """
        segments = []
        for xliff_file in self.files:
            for unit in xliff_file.units:
                segments.append({"content": unit.source, "translatable": True, "element": "text"})

        return {
            "segments": segments,
            "structure": {"tag": "document", "attributes": {}, "children_count": len(segments)},
        }
