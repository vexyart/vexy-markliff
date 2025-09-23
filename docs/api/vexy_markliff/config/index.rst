vexy_markliff.config
====================

.. py:module:: vexy_markliff.config

.. autoapi-nested-parse::

   Configuration management for vexy-markliff.



Attributes
----------

.. autoapisummary::

   vexy_markliff.config.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.config.ConversionMode
   vexy_markliff.config.StorageMode
   vexy_markliff.config.OutputFormat
   vexy_markliff.config.ConversionConfig


Functions
---------

.. autoapisummary::

   vexy_markliff.config.get_default_config
   vexy_markliff.config.load_config_with_env_override


Module Contents
---------------

.. py:data:: logger

.. py:class:: ConversionMode

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Supported conversion modes.

   Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: ONE_DOC
      :value: 'one-doc'



   .. py:attribute:: TWO_DOC
      :value: 'two-doc'



.. py:class:: StorageMode

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Supported storage modes.

   Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: SOURCE
      :value: 'source'



   .. py:attribute:: TARGET
      :value: 'target'



   .. py:attribute:: BOTH
      :value: 'both'



.. py:class:: OutputFormat

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Supported output formats.

   Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: XLIFF
      :value: 'xliff'



   .. py:attribute:: HTML
      :value: 'html'



   .. py:attribute:: MARKDOWN
      :value: 'markdown'



.. py:class:: ConversionConfig(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Configuration for conversion operations with comprehensive validation.

   This model provides secure configuration management with validation
   for language codes, file paths, and all conversion settings.

   .. rubric:: Examples

   >>> config = ConversionConfig()
   >>> config.source_language
   'en'

   >>> config = ConversionConfig(
   ...     source_language="fr",
   ...     target_language="de",
   ...     mode=ConversionMode.TWO_DOC
   ... )
   >>> config.mode
   'two-doc'

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: model_config

      Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].


   .. py:attribute:: source_language
      :type:  str
      :value: None



   .. py:attribute:: target_language
      :type:  str
      :value: None



   .. py:attribute:: mode
      :type:  ConversionMode
      :value: None



   .. py:attribute:: storage
      :type:  StorageMode
      :value: None



   .. py:attribute:: split_sentences
      :type:  bool
      :value: None



   .. py:attribute:: preserve_whitespace
      :type:  bool
      :value: None



   .. py:attribute:: output_format
      :type:  OutputFormat
      :value: None



   .. py:attribute:: skeleton_dir
      :type:  Optional[pathlib.Path]
      :value: None



   .. py:attribute:: output_dir
      :type:  Optional[pathlib.Path]
      :value: None



   .. py:attribute:: markdown_extensions
      :type:  List[str]
      :value: None



   .. py:attribute:: max_file_size_mb
      :type:  int
      :value: None



   .. py:method:: validate_language_code(v: str) -> str
      :classmethod:


      Validate language codes using ISO 639-1 pattern.

      :param v: Language code to validate

      :returns: Validated language code

      :raises ValueError: If language code is invalid



   .. py:method:: validate_directory_path(v: Optional[pathlib.Path]) -> Optional[pathlib.Path]
      :classmethod:


      Validate directory paths for security.

      :param v: Directory path to validate

      :returns: Validated Path object

      :raises ValueError: If path is insecure or invalid



   .. py:method:: validate_markdown_extensions(v: List[str]) -> List[str]
      :classmethod:


      Validate markdown extensions.

      :param v: List of extension names

      :returns: Validated extension list

      :raises ValueError: If extension is not supported



   .. py:method:: validate_configuration_consistency() -> ConversionConfig

      Validate configuration consistency.

      :returns: Validated configuration

      :raises ValueError: If configuration is inconsistent



   .. py:method:: from_file(config_path: pathlib.Path) -> ConversionConfig
      :classmethod:


      Load configuration from YAML file.

      :param config_path: Path to configuration file

      :returns: Configuration instance

      :raises ConfigurationError: If file cannot be loaded or is invalid

      .. rubric:: Examples

      >>> config = ConversionConfig.from_file(Path("config.yaml"))



   .. py:method:: to_file(config_path: pathlib.Path) -> None

      Save configuration to YAML file.

      :param config_path: Path where to save configuration

      :raises ConfigurationError: If file cannot be written



   .. py:method:: validate_file_path(file_path: pathlib.Path) -> pathlib.Path

      Validate a file path for security.

      :param file_path: File path to validate

      :returns: Validated and resolved path

      :raises ConfigurationError: If path is insecure



.. py:function:: get_default_config() -> ConversionConfig

   Get default configuration with sensible defaults.

   :returns: Default configuration instance


.. py:function:: load_config_with_env_override(config_path: Optional[pathlib.Path] = None) -> ConversionConfig

   Load configuration with environment variable overrides.

   :param config_path: Optional path to configuration file

   :returns: Configuration with environment overrides applied

   Environment Variables:
       VEXY_SOURCE_LANG: Override source language
       VEXY_TARGET_LANG: Override target language
       VEXY_MODE: Override conversion mode
       VEXY_STORAGE: Override storage mode
       VEXY_OUTPUT_FORMAT: Override output format
       VEXY_MAX_FILE_SIZE_MB: Override max file size
