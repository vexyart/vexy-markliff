vexy_markliff.core.inline_handler
=================================

.. py:module:: vexy_markliff.core.inline_handler

.. autoapi-nested-parse::

   Inline element handler for XLIFF conversion.



Attributes
----------

.. autoapisummary::

   vexy_markliff.core.inline_handler.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.core.inline_handler.InlineElement
   vexy_markliff.core.inline_handler.InlineHandler


Module Contents
---------------

.. py:data:: logger

.. py:class:: InlineElement

   Represents an inline element for XLIFF conversion.


   .. py:attribute:: tag_name
      :type:  str


   .. py:attribute:: attributes
      :type:  dict[str, Any]


   .. py:attribute:: content
      :type:  str
      :value: ''



   .. py:attribute:: element_id
      :type:  str
      :value: ''



   .. py:attribute:: is_paired
      :type:  bool
      :value: True



.. py:class:: InlineHandler

   Handle inline elements for XLIFF conversion.

   Initialize the inline handler.


   .. py:attribute:: MAX_RECURSION_DEPTH
      :value: 100



   .. py:attribute:: classifier


   .. py:attribute:: format_style


   .. py:attribute:: skeleton_generator


   .. py:attribute:: mrk_counter
      :value: 0



   .. py:attribute:: pc_counter
      :value: 0



   .. py:method:: create_mrk_element(tag_name: str, attributes: dict[str, Any] | None = None, content: str | None = None) -> xml.etree.ElementTree.Element

      Create a <mrk> element for inline content.

      :param tag_name: HTML tag name
      :param attributes: HTML attributes
      :param content: Text content

      :returns: XML Element for <mrk>

      .. rubric:: Examples

      >>> handler = InlineHandler()
      >>> mrk = handler.create_mrk_element("strong", {"class": "highlight"}, "Important text")
      >>> mrk.get("id")
      'm1'
      >>> mrk.get("fs:fs")
      'strong'
      >>> mrk.text
      'Important text'



   .. py:method:: create_ph_element(tag_name: str, attributes: dict[str, Any] | None = None) -> xml.etree.ElementTree.Element

      Create a <ph> element for void/placeholder content.

      :param tag_name: HTML tag name
      :param attributes: HTML attributes

      :returns: XML Element for <ph>



   .. py:method:: create_paired_code_elements(tag_name: str, attributes: dict[str, Any] | None = None) -> tuple[xml.etree.ElementTree.Element, xml.etree.ElementTree.Element]

      Create paired code elements (pc/ec) for inline elements.

      :param tag_name: HTML tag name
      :param attributes: HTML attributes

      :returns: Tuple of (opening pc element, closing ec element)



   .. py:method:: process_inline_content(html_element: Any, depth: int = 0) -> list[xml.etree.ElementTree.Element]

      Process HTML element into inline XLIFF elements.

      :param html_element: HTML element to process
      :param depth: Current recursion depth (for preventing stack overflow)

      :returns: List of XLIFF inline elements

      :raises RecursionError: If maximum recursion depth is exceeded



   .. py:method:: _get_equiv_text(tag_name: str, attributes: dict[str, Any] | None) -> str | None

      Get equivalent text for placeholder elements.

      :param tag_name: HTML tag name
      :param attributes: HTML attributes

      :returns: Equivalent text or None



   .. py:method:: is_inline_element(tag_name: str) -> bool

      Check if element is an inline element.

      :param tag_name: HTML tag name

      :returns: True if inline element



   .. py:method:: should_use_mrk(tag_name: str) -> bool

      Check if element should use <mrk> wrapper.

      :param tag_name: HTML tag name

      :returns: True if should use <mrk>



   .. py:method:: should_use_ph(tag_name: str) -> bool

      Check if element should use <ph> placeholder.

      :param tag_name: HTML tag name

      :returns: True if should use <ph>



   .. py:method:: reset() -> None

      Reset counters for new document.



   .. py:method:: extract_inline_elements(text: str, elements: list[Any]) -> list[InlineElement]

      Extract inline elements from mixed content.

      :param text: Plain text content
      :param elements: List of HTML elements

      :returns: List of InlineElement objects



   .. py:method:: wrap_text_with_inline_markers(text: str, inline_elements: list[InlineElement]) -> xml.etree.ElementTree.Element

      Wrap text content with inline markers.

      :param text: Plain text to wrap
      :param inline_elements: List of inline elements to insert

      :returns: XML Element containing text with inline markers
