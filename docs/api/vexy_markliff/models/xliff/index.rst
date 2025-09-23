vexy_markliff.models.xliff
==========================

.. py:module:: vexy_markliff.models.xliff

.. autoapi-nested-parse::

   Pydantic models for XLIFF 2.1 documents.



Classes
-------

.. autoapisummary::

   vexy_markliff.models.xliff.TranslationUnit
   vexy_markliff.models.xliff.SkeletonFile
   vexy_markliff.models.xliff.XLIFFFile
   vexy_markliff.models.xliff.XLIFFDocument


Module Contents
---------------

.. py:class:: TranslationUnit(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents a translation unit in XLIFF.

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: model_config

      Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].


   .. py:attribute:: id
      :type:  str
      :value: None



   .. py:attribute:: source
      :type:  str
      :value: None



   .. py:attribute:: target
      :type:  str | None
      :value: None



   .. py:attribute:: state
      :type:  str
      :value: None



   .. py:attribute:: fs_fs
      :type:  str | None
      :value: None



   .. py:attribute:: fs_subfs
      :type:  str | None
      :value: None



.. py:class:: SkeletonFile(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents external skeleton file information.

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: model_config

      Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].


   .. py:attribute:: href
      :type:  str
      :value: None



   .. py:attribute:: content
      :type:  str | None
      :value: None



.. py:class:: XLIFFFile(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents a file element in XLIFF document.

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: model_config

      Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].


   .. py:attribute:: id
      :type:  str
      :value: None



   .. py:attribute:: source_language
      :type:  str
      :value: None



   .. py:attribute:: target_language
      :type:  str | None
      :value: None



   .. py:attribute:: original
      :type:  str
      :value: None



   .. py:attribute:: units
      :type:  list[TranslationUnit]
      :value: None



   .. py:attribute:: skeleton
      :type:  SkeletonFile | None
      :value: None



.. py:class:: XLIFFDocument(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents a complete XLIFF 2.1 document.

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: model_config

      Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].


   .. py:attribute:: version
      :type:  str
      :value: None



   .. py:attribute:: xmlns
      :type:  str
      :value: None



   .. py:attribute:: xmlns_fs
      :type:  str
      :value: None



   .. py:attribute:: files
      :type:  list[XLIFFFile]
      :value: None



   .. py:attribute:: metadata
      :type:  dict[str, Any]
      :value: None



   .. py:method:: add_file(file_id: str, source_lang: str, target_lang: str | None = None, original: str = 'document') -> XLIFFFile

      Add a new file to the XLIFF document.



   .. py:method:: add_unit(file_id: str, unit_id: str, source: str, target: str | None = None, **kwargs: Any) -> TranslationUnit

      Add a translation unit to a specific file.



   .. py:method:: to_xml() -> str

      Convert the XLIFF document to XML string.
