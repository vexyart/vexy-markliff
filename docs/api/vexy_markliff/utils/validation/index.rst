vexy_markliff.utils.validation
==============================

.. py:module:: vexy_markliff.utils.validation

.. autoapi-nested-parse::

   Input validation utilities for vexy-markliff.



Functions
---------

.. autoapisummary::

   vexy_markliff.utils.validation.validate_string_content
   vexy_markliff.utils.validation.validate_language_code
   vexy_markliff.utils.validation.validate_file_path
   vexy_markliff.utils.validation.validate_element_attributes
   vexy_markliff.utils.validation.validate_element_name
   vexy_markliff.utils.validation.validate_positive_integer
   vexy_markliff.utils.validation.validate_boolean
   vexy_markliff.utils.validation.validate_configuration_dict


Module Contents
---------------

.. py:function:: validate_string_content(content: Any, field_name: str, allow_empty: bool = False, max_length: int | None = None) -> str

   Validate string content input.

   :param content: Content to validate
   :param field_name: Name of the field for error messages
   :param allow_empty: Whether to allow empty strings
   :param max_length: Maximum allowed length

   :returns: Validated string content

   :raises ValidationError: If validation fails


.. py:function:: validate_language_code(lang_code: Any, field_name: str = 'language_code') -> str

   Validate language code (ISO 639-1 or 639-3 format).

   :param lang_code: Language code to validate
   :param field_name: Name of the field for error messages

   :returns: Validated language code

   :raises ValidationError: If validation fails


.. py:function:: validate_file_path(file_path: Any, operation: str = 'access', must_exist: bool = False, create_parent_dirs: bool = False) -> pathlib.Path

   Validate file path input.

   :param file_path: File path to validate
   :param operation: Type of operation (read, write, access)
   :param must_exist: Whether the file must already exist
   :param create_parent_dirs: Whether to create parent directories for write operations

   :returns: Validated Path object

   :raises FileOperationError: If validation fails


.. py:function:: validate_element_attributes(attributes: Any, field_name: str = 'attributes') -> dict[str, Any]

   Validate HTML element attributes.

   :param attributes: Attributes to validate
   :param field_name: Name of the field for error messages

   :returns: Validated attributes dictionary

   :raises ValidationError: If validation fails


.. py:function:: validate_element_name(element_name: Any, field_name: str = 'element_name') -> str

   Validate HTML element name.

   :param element_name: Element name to validate
   :param field_name: Name of the field for error messages

   :returns: Validated element name

   :raises ValidationError: If validation fails


.. py:function:: validate_positive_integer(value: Any, field_name: str, allow_zero: bool = False) -> int

   Validate positive integer input.

   :param value: Value to validate
   :param field_name: Name of the field for error messages
   :param allow_zero: Whether to allow zero as valid

   :returns: Validated integer

   :raises ValidationError: If validation fails


.. py:function:: validate_boolean(value: Any, field_name: str) -> bool

   Validate boolean input with flexible conversion.

   :param value: Value to validate
   :param field_name: Name of the field for error messages

   :returns: Validated boolean

   :raises ValidationError: If validation fails


.. py:function:: validate_configuration_dict(config: Any, field_name: str = 'configuration') -> dict[str, Any]

   Validate configuration dictionary.

   :param config: Configuration to validate
   :param field_name: Name of the field for error messages

   :returns: Validated configuration dictionary

   :raises ConfigurationError: If validation fails
