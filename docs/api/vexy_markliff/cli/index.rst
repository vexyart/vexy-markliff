vexy_markliff.cli
=================

.. py:module:: vexy_markliff.cli

.. autoapi-nested-parse::

   Fire CLI interface for vexy-markliff.



Attributes
----------

.. autoapisummary::

   vexy_markliff.cli.console
   vexy_markliff.cli.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.cli.VexyMarkliffCLI


Functions
---------

.. autoapisummary::

   vexy_markliff.cli.main


Module Contents
---------------

.. py:data:: console

.. py:data:: logger

.. py:class:: VexyMarkliffCLI(verbose: bool = False, log_file: str | None = None)

   Command-line interface for Vexy Markliff conversion tools.

   Global options:
       --verbose: Enable verbose debug logging
       --log-file: Path to log file for debug output

   Initialize CLI with optional logging configuration.

   :param verbose: Enable verbose debug logging
   :param log_file: Optional log file path


   .. py:method:: md2xliff(input_file: str, output_file: str, source_lang: str = 'en', target_lang: str = 'es', **kwargs: Any) -> None

      Convert Markdown to XLIFF format.

      :param input_file: Path to input Markdown file
      :param output_file: Path to output XLIFF file
      :param source_lang: Source language code (default: en)
      :param target_lang: Target language code (default: es)



   .. py:method:: html2xliff(input_file: str, output_file: str, source_lang: str = 'en', target_lang: str = 'es', **kwargs: Any) -> None

      Convert HTML to XLIFF format.

      :param input_file: Path to input HTML file
      :param output_file: Path to output XLIFF file
      :param source_lang: Source language code (default: en)
      :param target_lang: Target language code (default: es)



   .. py:method:: xliff2md(input_file: str, output_file: str, **kwargs: Any) -> None

      Convert XLIFF to Markdown format.

      :param input_file: Path to input XLIFF file
      :param output_file: Path to output Markdown file



   .. py:method:: xliff2html(input_file: str, output_file: str, **kwargs: Any) -> None

      Convert XLIFF to HTML format.

      :param input_file: Path to input XLIFF file
      :param output_file: Path to output HTML file



.. py:function:: main() -> None

   Main entry point for the CLI.
