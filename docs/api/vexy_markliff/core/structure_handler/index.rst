vexy_markliff.core.structure_handler
====================================

.. py:module:: vexy_markliff.core.structure_handler

.. autoapi-nested-parse::

   Complex structure handler for tables, forms, and media elements.



Attributes
----------

.. autoapisummary::

   vexy_markliff.core.structure_handler.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.core.structure_handler.StructureType
   vexy_markliff.core.structure_handler.ComplexStructure
   vexy_markliff.core.structure_handler.StructureHandler


Module Contents
---------------

.. py:data:: logger

.. py:class:: StructureType(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Types of complex structures.


   .. py:attribute:: TABLE
      :value: 'table'



   .. py:attribute:: FORM
      :value: 'form'



   .. py:attribute:: MEDIA
      :value: 'media'



   .. py:attribute:: CONTAINER
      :value: 'container'



.. py:class:: ComplexStructure

   Represents a complex HTML structure.


   .. py:attribute:: element_type
      :type:  StructureType


   .. py:attribute:: tag_name
      :type:  str


   .. py:attribute:: attributes
      :type:  dict[str, Any]


   .. py:attribute:: content
      :type:  str
      :value: ''



   .. py:attribute:: preserve_space
      :type:  bool
      :value: True



   .. py:attribute:: unit_id
      :type:  str
      :value: ''



   .. py:attribute:: children
      :type:  list[Any]
      :value: []



.. py:class:: StructureHandler

   Handle complex structures for XLIFF conversion.

   Initialize the structure handler.


   .. py:attribute:: TABLE_ELEMENTS


   .. py:attribute:: FORM_ELEMENTS


   .. py:attribute:: MEDIA_ELEMENTS


   .. py:attribute:: classifier


   .. py:attribute:: format_style


   .. py:attribute:: skeleton_generator


   .. py:attribute:: inline_handler


   .. py:attribute:: unit_counter
      :value: 0



   .. py:attribute:: group_counter
      :value: 0



   .. py:method:: classify_structure(tag_name: str) -> StructureType | None

      Classify the structure type of an element.

      :param tag_name: HTML tag name

      :returns: StructureType or None if not a complex structure



   .. py:method:: create_unit_element(tag_name: str, attributes: dict[str, Any] | None = None, content: str | None = None, preserve_space: bool = True, use_cdata: bool = False) -> xml.etree.ElementTree.Element

      Create a <unit> element for complex structure.

      :param tag_name: HTML tag name
      :param attributes: HTML attributes
      :param content: HTML content
      :param preserve_space: Whether to preserve whitespace
      :param use_cdata: Whether to use CDATA for content

      :returns: XML Element for <unit>



   .. py:method:: create_group_element(tag_name: str, attributes: dict[str, Any] | None = None) -> xml.etree.ElementTree.Element

      Create a <group> element for nested structures.

      :param tag_name: HTML tag name
      :param attributes: HTML attributes

      :returns: XML Element for <group>



   .. py:method:: process_table_structure(html_element: Any, cell_by_cell: bool = False) -> xml.etree.ElementTree.Element

      Process a table structure for XLIFF.

      :param html_element: HTML table element
      :param cell_by_cell: Whether to break down by cells

      :returns: XML Element for table structure



   .. py:method:: process_form_structure(html_element: Any) -> xml.etree.ElementTree.Element

      Process a form structure for XLIFF.

      :param html_element: HTML form element

      :returns: XML Element for form structure



   .. py:method:: process_media_structure(html_element: Any) -> xml.etree.ElementTree.Element

      Process a media structure for XLIFF.

      :param html_element: HTML media element

      :returns: XML Element for media structure



   .. py:method:: _generate_unit_id(tag_name: str) -> str

      Generate a unit ID based on tag name.

      :param tag_name: HTML tag name

      :returns: Unit ID string



   .. py:method:: _serialize_html_element(element: Any) -> str

      Serialize HTML element to string.

      :param element: HTML element

      :returns: Serialized HTML string



   .. py:method:: _process_table_cells(table_element: Any, parent: xml.etree.ElementTree.Element) -> None

      Process table cells as individual units.

      :param table_element: HTML table element
      :param parent: Parent XLIFF element



   .. py:method:: _extract_form_text(form_element: Any, parent: xml.etree.ElementTree.Element) -> None

      Extract translatable text from form elements.

      :param form_element: HTML form element
      :param parent: Parent XLIFF element



   .. py:method:: _process_media_children(media_element: Any, parent: xml.etree.ElementTree.Element) -> None

      Process media children as placeholders.

      :param media_element: HTML media element
      :param parent: Parent XLIFF element



   .. py:method:: should_preserve_structure(tag_name: str) -> bool

      Check if element should preserve its structure.

      :param tag_name: HTML tag name

      :returns: True if structure should be preserved



   .. py:method:: reset() -> None

      Reset counters for new document.
