vexy_markliff.core.skeleton_generator
=====================================

.. py:module:: vexy_markliff.core.skeleton_generator

.. autoapi-nested-parse::

   Skeleton generator for XLIFF document structure preservation.



Attributes
----------

.. autoapisummary::

   vexy_markliff.core.skeleton_generator.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.core.skeleton_generator.SkeletonGenerator


Module Contents
---------------

.. py:data:: logger

.. py:class:: SkeletonGenerator

   Generate XLIFF skeleton files with placeholders for structure preservation.

   Initialize the skeleton generator.


   .. py:attribute:: MAX_ORIGINAL_DATA_ENTRIES
      :value: 10000



   .. py:attribute:: classifier


   .. py:attribute:: format_style


   .. py:attribute:: placeholder_counter
      :value: 0



   .. py:attribute:: data_ref_counter
      :value: 0



   .. py:attribute:: original_data
      :type:  dict[str, str]


   .. py:method:: _ensure_original_data_size_limit() -> None

      Ensure original_data doesn't exceed memory limits.



   .. py:method:: generate_placeholder(element_name: str, attributes: dict[str, Any] | None = None, element_type: str = 'standalone') -> tuple[str, str]

      Generate a placeholder for a void or inline element.

      :param element_name: Name of the HTML element
      :param attributes: Element attributes
      :param element_type: Type of placeholder (standalone, open, close)

      :returns: Tuple of (placeholder ID, data reference ID)

      .. rubric:: Examples

      >>> generator = SkeletonGenerator()
      >>> ph_id, data_id = generator.generate_placeholder("img", {"src": "image.jpg", "alt": "Test"})
      >>> ph_id
      'ph-img001'
      >>> data_id
      'd1'
      >>> generator.original_data[data_id]
      '<img src="image.jpg" alt="Test"/>'



   .. py:method:: _create_html_fragment(element_name: str, attributes: dict[str, Any] | None = None, element_type: str = 'standalone') -> str

      Create HTML fragment for original data.

      :param element_name: Name of the HTML element
      :param attributes: Element attributes
      :param element_type: Type of element

      :returns: HTML fragment string



   .. py:method:: create_skeleton_element(element_name: str, attributes: dict[str, Any] | None = None, content: str | None = None) -> xml.etree.ElementTree.Element

      Create a skeleton element for non-translatable structure.

      :param element_name: Name of the HTML element
      :param attributes: Element attributes
      :param content: Optional text content

      :returns: XML Element for skeleton



   .. py:method:: generate_skeleton_document(html_structure: list[xml.etree.ElementTree.Element]) -> str

      Generate a complete skeleton document.

      :param html_structure: List of skeleton elements

      :returns: Serialized skeleton document



   .. py:method:: create_placeholder_element(placeholder_id: str, data_ref_id: str, can_copy: bool = True, can_delete: bool = False, can_reorder: bool = False, equiv_text: str | None = None) -> xml.etree.ElementTree.Element

      Create a placeholder element for XLIFF.

      :param placeholder_id: Unique ID for the placeholder
      :param data_ref_id: Reference to original data
      :param can_copy: Whether placeholder can be copied
      :param can_delete: Whether placeholder can be deleted
      :param can_reorder: Whether placeholder can be reordered
      :param equiv_text: Equivalent text for accessibility

      :returns: XML Element for placeholder



   .. py:method:: create_original_data_element() -> xml.etree.ElementTree.Element | None

      Create originalData element with all data references.

      :returns: XML Element for originalData or None if no data



   .. py:method:: should_be_skeleton(element_name: str) -> bool

      Check if element should be in skeleton only.

      :param element_name: Name of the HTML element

      :returns: True if element should be skeleton-only



   .. py:method:: should_be_placeholder(element_name: str) -> bool

      Check if element should become a placeholder.

      :param element_name: Name of the HTML element

      :returns: True if element should be a placeholder



   .. py:method:: reset() -> None

      Reset counters and data for new document.



   .. py:method:: generate_inline_code_placeholder(element_name: str, element_type: str, attributes: dict[str, Any] | None = None) -> tuple[xml.etree.ElementTree.Element, str]

      Generate inline code placeholder for paired tags.

      :param element_name: Name of the HTML element
      :param element_type: Type of code (open/close)
      :param attributes: Element attributes (for open tags)

      :returns: Tuple of (placeholder element, data reference ID)
