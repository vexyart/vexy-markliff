vexy_markliff.core.converter
============================

.. py:module:: vexy_markliff.core.converter

.. autoapi-nested-parse::

   Main conversion orchestrator.



Classes
-------

.. autoapisummary::

   vexy_markliff.core.converter.VexyMarkliff


Module Contents
---------------

.. py:class:: VexyMarkliff(config: vexy_markliff.config.ConversionConfig | None = None)

   Main converter class for handling bidirectional Markdown/HTML to XLIFF conversion.

   Initialize the converter with optional configuration.


   .. py:attribute:: config


   .. py:method:: markdown_to_xliff(markdown_content: str, source_lang: str = 'en', target_lang: str = 'es') -> str

      Convert Markdown content to XLIFF format.

      :param markdown_content: Markdown content to convert
      :param source_lang: Source language code
      :param target_lang: Target language code

      :returns: XLIFF formatted string

      :raises ValidationError: If input validation fails



   .. py:method:: html_to_xliff(html_content: str, source_lang: str = 'en', target_lang: str = 'es') -> str

      Convert HTML content to XLIFF format.

      :param html_content: HTML content to convert
      :param source_lang: Source language code
      :param target_lang: Target language code

      :returns: XLIFF formatted string

      :raises ValidationError: If input validation fails



   .. py:method:: xliff_to_markdown(xliff_content: str) -> str

      Convert XLIFF content back to Markdown format.

      :param xliff_content: XLIFF content to convert

      :returns: Markdown formatted string

      :raises ValidationError: If input validation fails



   .. py:method:: xliff_to_html(xliff_content: str) -> str

      Convert XLIFF content back to HTML format.

      :param xliff_content: XLIFF content to convert

      :returns: HTML formatted string

      :raises ValidationError: If input validation fails



   .. py:method:: process_parallel(source_content: str, target_content: str, mode: str = 'aligned') -> dict[str, Any]

      Process parallel source and target documents for alignment.

      :param source_content: Source document content
      :param target_content: Target document content
      :param mode: Alignment mode

      :returns: Dictionary containing alignment results

      :raises ValidationError: If input validation fails
