vexy_markliff.exceptions
========================

.. py:module:: vexy_markliff.exceptions

.. autoapi-nested-parse::

   Custom exceptions for vexy-markliff.



Exceptions
----------

.. autoapisummary::

   vexy_markliff.exceptions.VexyMarkliffError
   vexy_markliff.exceptions.ParsingError
   vexy_markliff.exceptions.ValidationError
   vexy_markliff.exceptions.XLIFFValidationError
   vexy_markliff.exceptions.ConversionError
   vexy_markliff.exceptions.AlignmentError
   vexy_markliff.exceptions.ConfigurationError
   vexy_markliff.exceptions.FileOperationError


Module Contents
---------------

.. py:exception:: VexyMarkliffError

   Bases: :py:obj:`Exception`


   Base exception for all vexy-markliff errors.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ParsingError(message: str, source_type: str = 'unknown')

   Bases: :py:obj:`VexyMarkliffError`


   Raised when document parsing fails.

   Initialize parsing error.

   :param message: Error description
   :param source_type: Type of source that failed to parse (markdown, html, xliff)


   .. py:attribute:: source_type
      :value: 'unknown'



.. py:exception:: ValidationError

   Bases: :py:obj:`VexyMarkliffError`


   Raised when document validation fails.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: XLIFFValidationError(message: str, element: str | None = None)

   Bases: :py:obj:`ValidationError`


   Raised when XLIFF document validation fails.

   Initialize XLIFF validation error.

   :param message: Error description
   :param element: XLIFF element that failed validation


   .. py:attribute:: element
      :value: None



.. py:exception:: ConversionError(message: str, from_format: str = '', to_format: str = '')

   Bases: :py:obj:`VexyMarkliffError`


   Raised when document conversion fails.

   Initialize conversion error.

   :param message: Error description
   :param from_format: Source format
   :param to_format: Target format


   .. py:attribute:: from_format
      :value: ''



   .. py:attribute:: to_format
      :value: ''



.. py:exception:: AlignmentError(message: str, source_segments: int = 0, target_segments: int = 0)

   Bases: :py:obj:`VexyMarkliffError`


   Raised when document alignment fails.

   Initialize alignment error.

   :param message: Error description
   :param source_segments: Number of source segments
   :param target_segments: Number of target segments


   .. py:attribute:: source_segments
      :value: 0



   .. py:attribute:: target_segments
      :value: 0



.. py:exception:: ConfigurationError(message: str, parameter: str | None = None)

   Bases: :py:obj:`VexyMarkliffError`


   Raised when configuration is invalid.

   Initialize configuration error.

   :param message: Error description
   :param parameter: Configuration parameter that is invalid


   .. py:attribute:: parameter
      :value: None



.. py:exception:: FileOperationError(message: str, file_path: str | None = None, operation: str = 'access')

   Bases: :py:obj:`VexyMarkliffError`


   Raised when file operations fail.

   Initialize file operation error.

   :param message: Error description
   :param file_path: Path to the file
   :param operation: Operation that failed (read, write, create, etc.)


   .. py:attribute:: file_path
      :value: None



   .. py:attribute:: operation
      :value: 'access'
