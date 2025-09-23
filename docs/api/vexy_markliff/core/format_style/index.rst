vexy_markliff.core.format_style
===============================

.. py:module:: vexy_markliff.core.format_style

.. autoapi-nested-parse::

   Format Style attribute serialization for XLIFF.



Attributes
----------

.. autoapisummary::

   vexy_markliff.core.format_style.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.core.format_style.FormatStyleSerializer


Module Contents
---------------

.. py:data:: logger

.. py:class:: FormatStyleSerializer

   Serialize HTML attributes for XLIFF Format Style module.


   .. py:method:: escape_value(value: str) -> str
      :staticmethod:


      Escape special characters in attribute values.

      :param value: Attribute value to escape

      :returns: Escaped value



   .. py:method:: unescape_value(value: str) -> str
      :staticmethod:


      Unescape special characters in attribute values.

      :param value: Escaped attribute value

      :returns: Unescaped value



   .. py:method:: serialize_attributes(attributes: dict[str, Any]) -> str

      Serialize HTML attributes to fs:subFs format.

      Format: name1,value1\name2,value2\name3,value3
      - Comma separates name from value
      - Backslash separates attribute pairs
      - Literal commas escaped as \,
      - Literal backslashes escaped as \\
      - Empty values become name,

      :param attributes: Dictionary of attribute name-value pairs

      :returns: subFs string
      :rtype: Serialized fs

      .. rubric:: Examples

      >>> serializer = FormatStyleSerializer()
      >>> serializer.serialize_attributes({"class": "test", "id": "main"})
      'class,test\\id,main'
      >>> serializer.serialize_attributes({"href": "http://example.com", "target": "_blank"})
      'href,http://example.com\\target,_blank'
      >>> serializer.serialize_attributes({"disabled": ""})
      'disabled,'
      >>> serializer.serialize_attributes({})
      ''



   .. py:method:: deserialize_attributes(subfs: str) -> dict[str, str]

      Deserialize fs:subFs format to HTML attributes.

      :param subfs: Serialized fs:subFs string

      :returns: Dictionary of attribute name-value pairs

      .. rubric:: Examples

      >>> serializer = FormatStyleSerializer()
      >>> serializer.deserialize_attributes('class,test\\id,main')
      {'class': 'test', 'id': 'main'}
      >>> serializer.deserialize_attributes('href,http://example.com\\target,_blank')
      {'href': 'http://example.com', 'target': '_blank'}
      >>> serializer.deserialize_attributes('disabled,')
      {'disabled': ''}
      >>> serializer.deserialize_attributes('')
      {}



   .. py:method:: _split_attribute_pairs(text: str) -> list[str]

      Split fs:subFs string into attribute pairs.

      Handles special cases:
      - \, is an escaped comma (not a separator)
      - \\ is an escaped backslash (not a separator)
      - \ followed by anything else is a separator

      :param text: fs:subFs string to split

      :returns: List of attribute pairs



   .. py:method:: _split_unescaped(text: str, delimiter: str, max_split: int = -1) -> list[str]

      Split text by unescaped delimiter.

      :param text: Text to split
      :param delimiter: Delimiter character
      :param max_split: Maximum number of splits (-1 for unlimited)

      :returns: List of split parts



   .. py:method:: format_fs_element(tag_name: str, attributes: dict[str, Any] | None = None) -> dict[str, str]

      Format an HTML element for XLIFF Format Style attributes.

      :param tag_name: HTML element tag name
      :param attributes: Optional dictionary of HTML attributes

      :returns: fs and optionally fs:subFs attributes
      :rtype: Dictionary with fs

      :raises ValidationError: If input validation fails



   .. py:method:: serialize_inline_attributes(tag_name: str, attributes: dict[str, Any] | None = None) -> str

      Serialize inline element attributes for mrk elements.

      :param tag_name: HTML element tag name
      :param attributes: Optional dictionary of HTML attributes

      :returns: fs and fs:subFs value for mrk element
      :rtype: Combined fs



   .. py:method:: deserialize_inline_attributes(combined: str) -> tuple[str, dict[str, str]]

      Deserialize combined inline attributes from mrk element.

      :param combined: Combined fs:fs#fs:subFs value

      :returns: Tuple of (tag_name, attributes)
