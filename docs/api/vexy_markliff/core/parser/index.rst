vexy_markliff.core.parser
=========================

.. py:module:: vexy_markliff.core.parser

.. autoapi-nested-parse::

   HTML and Markdown parsing utilities.



Attributes
----------

.. autoapisummary::

   vexy_markliff.core.parser.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.core.parser.MarkdownParser
   vexy_markliff.core.parser.HTMLParser


Module Contents
---------------

.. py:data:: logger

.. py:class:: MarkdownParser(enable_plugins: bool = True)

   Parser for Markdown content using markdown-it-py.

   Initialize the Markdown parser with plugins.

   :param enable_plugins: Whether to enable additional plugins for extended Markdown support.


   .. py:attribute:: MAX_TOKEN_DEPTH
      :value: 200



   .. py:attribute:: md


   .. py:method:: parse(content: str) -> dict[str, Any]

      Parse Markdown content and return structured data.

      :param content: Markdown content to parse

      :returns: Parsed markdown data including tokens, HTML, and metadata

      :raises ParsingError: If Markdown parsing fails



   .. py:method:: _token_to_dict(token: Any, depth: int = 0) -> dict[str, Any]

      Convert a markdown-it token to a dictionary.

      :param token: Markdown token to convert
      :param depth: Current recursion depth (for preventing stack overflow)

      :returns: Dictionary representation of token

      :raises RecursionError: If maximum token depth is exceeded



   .. py:method:: _extract_front_matter(tokens: list[Any]) -> dict[str, Any] | None

      Extract front matter data from tokens.



   .. py:method:: _has_feature(tokens: list[Any], feature_type: str) -> bool

      Check if tokens contain a specific feature type.



   .. py:method:: render_html(content: str) -> str

      Render Markdown content to HTML.

      :param content: Markdown content to render

      :returns: Rendered HTML string

      :raises ParsingError: If rendering fails



.. py:class:: HTMLParser

   Parser for HTML content using lxml.


   .. py:method:: parse(content: str) -> dict[str, Any]

      Parse HTML content and return structured data.

      :param content: HTML content to parse

      :returns: Parsed HTML data including tree, elements, and text content

      :raises ParsingError: If HTML parsing fails



   .. py:method:: _extract_elements(element: Any) -> list[dict[str, Any]]

      Extract elements from HTML tree.
