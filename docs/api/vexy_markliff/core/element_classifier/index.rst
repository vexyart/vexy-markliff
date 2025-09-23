vexy_markliff.core.element_classifier
=====================================

.. py:module:: vexy_markliff.core.element_classifier

.. autoapi-nested-parse::

   HTML element classification for XLIFF conversion.



Attributes
----------

.. autoapisummary::

   vexy_markliff.core.element_classifier.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.core.element_classifier.ElementCategory
   vexy_markliff.core.element_classifier.HTMLElementClassifier


Module Contents
---------------

.. py:data:: logger

.. py:class:: ElementCategory(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Categories for HTML elements in XLIFF conversion.


   .. py:attribute:: SKELETON
      :value: 'skeleton'



   .. py:attribute:: SECTIONING
      :value: 'sectioning'



   .. py:attribute:: LIST
      :value: 'list'



   .. py:attribute:: TABLE
      :value: 'table'



   .. py:attribute:: FLOW_TEXT
      :value: 'flow_text'



   .. py:attribute:: INLINE
      :value: 'inline'



   .. py:attribute:: VOID
      :value: 'void'



   .. py:attribute:: MEDIA
      :value: 'media'



   .. py:attribute:: FORM
      :value: 'form'



   .. py:attribute:: UNKNOWN
      :value: 'unknown'



.. py:class:: HTMLElementClassifier

   Classify HTML elements for XLIFF conversion.

   Initialize the HTML element classifier.


   .. py:attribute:: ELEMENT_CATEGORIES


   .. py:attribute:: PRESERVE_SPACE_ELEMENTS


   .. py:attribute:: UNIT_ELEMENTS


   .. py:attribute:: GROUP_ELEMENTS


   .. py:attribute:: MARKER_ELEMENTS


   .. py:attribute:: PLACEHOLDER_ELEMENTS


   .. py:method:: classify(element_name: str) -> ElementCategory

      Classify an HTML element.

      :param element_name: Name of the HTML element (lowercase)

      :returns: ElementCategory for the element

      .. rubric:: Examples

      >>> classifier = HTMLElementClassifier()
      >>> classifier.classify("p")
      ElementCategory.FLOW_TEXT
      >>> classifier.classify("div")
      ElementCategory.SECTIONING
      >>> classifier.classify("strong")
      ElementCategory.INLINE
      >>> classifier.classify("img")
      ElementCategory.VOID



   .. py:method:: requires_whitespace_preservation(element_name: str) -> bool

      Check if element requires preserving whitespace.

      :param element_name: Name of the HTML element

      :returns: True if whitespace should be preserved



   .. py:method:: is_translatable_unit(element_name: str) -> bool

      Check if element should become a translation unit.

      :param element_name: Name of the HTML element

      :returns: True if element should become a unit



   .. py:method:: is_group_element(element_name: str) -> bool

      Check if element should become a group.

      :param element_name: Name of the HTML element

      :returns: True if element should become a group



   .. py:method:: is_inline_element(element_name: str) -> bool

      Check if element is inline and should become a marker.

      :param element_name: Name of the HTML element

      :returns: True if element should become a marker



   .. py:method:: is_void_element(element_name: str) -> bool

      Check if element is void and should become a placeholder.

      :param element_name: Name of the HTML element

      :returns: True if element should become a placeholder



   .. py:method:: get_xliff_representation(element_name: str) -> str

      Get the XLIFF representation type for an element.

      :param element_name: Name of the HTML element

      :returns: XLIFF representation type (unit, group, marker, placeholder, skeleton)

      .. rubric:: Examples

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



   .. py:method:: get_segmentation_strategy(element_name: str) -> str

      Get the segmentation strategy for an element.

      :param element_name: Name of the HTML element

      :returns: Segmentation strategy (sentence, element, preserve)



   .. py:method:: should_extract_attributes(element_name: str) -> bool

      Check if element attributes should be extracted.

      :param element_name: Name of the HTML element

      :returns: True if attributes should be extracted



   .. py:method:: get_important_attributes(element_name: str) -> tuple[str, Ellipsis]

      Get list of important attributes for an element.

      :param element_name: Name of the HTML element

      :returns: Tuple of important attribute names (cached as tuple for immutability)
