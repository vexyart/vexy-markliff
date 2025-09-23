vexy_markliff.models.document_pair
==================================

.. py:module:: vexy_markliff.models.document_pair

.. autoapi-nested-parse::

   Pydantic models for parallel document handling.



Classes
-------

.. autoapisummary::

   vexy_markliff.models.document_pair.AlignmentMode
   vexy_markliff.models.document_pair.AlignmentQuality
   vexy_markliff.models.document_pair.DocumentSegment
   vexy_markliff.models.document_pair.AlignedSegmentPair
   vexy_markliff.models.document_pair.TwoDocumentPair


Module Contents
---------------

.. py:class:: AlignmentMode

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Alignment modes for two-document processing.

   Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: PARAGRAPH
      :value: 'paragraph'



   .. py:attribute:: SENTENCE
      :value: 'sentence'



   .. py:attribute:: HEADING
      :value: 'heading'



   .. py:attribute:: AUTO
      :value: 'auto'



.. py:class:: AlignmentQuality

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Quality indicators for document alignment.

   Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: PERFECT
      :value: 'perfect'



   .. py:attribute:: HIGH
      :value: 'high'



   .. py:attribute:: MEDIUM
      :value: 'medium'



   .. py:attribute:: LOW
      :value: 'low'



   .. py:attribute:: FAILED
      :value: 'failed'



.. py:class:: DocumentSegment(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents a segment of a document.

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: id
      :type:  str
      :value: None



   .. py:attribute:: content
      :type:  str
      :value: None



   .. py:attribute:: type
      :type:  str
      :value: None



   .. py:attribute:: level
      :type:  int
      :value: None



   .. py:attribute:: metadata
      :type:  dict[str, Any]
      :value: None



.. py:class:: AlignedSegmentPair(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents a pair of aligned segments from source and target documents.

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: source_segment
      :type:  DocumentSegment | None
      :value: None



   .. py:attribute:: target_segment
      :type:  DocumentSegment | None
      :value: None



   .. py:attribute:: alignment_confidence
      :type:  float
      :value: None



   .. py:attribute:: alignment_type
      :type:  str
      :value: None



   .. py:method:: validate_alignment_type(v: str) -> str
      :classmethod:


      Validate alignment type.



.. py:class:: TwoDocumentPair(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Model for handling parallel source and target documents.

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: source_lang
      :type:  str
      :value: None



   .. py:attribute:: target_lang
      :type:  str
      :value: None



   .. py:attribute:: source_content
      :type:  str
      :value: None



   .. py:attribute:: target_content
      :type:  str
      :value: None



   .. py:attribute:: source_format
      :type:  str
      :value: None



   .. py:attribute:: target_format
      :type:  str
      :value: None



   .. py:attribute:: alignment_mode
      :type:  AlignmentMode
      :value: None



   .. py:attribute:: source_segments
      :type:  list[DocumentSegment]
      :value: None



   .. py:attribute:: target_segments
      :type:  list[DocumentSegment]
      :value: None



   .. py:attribute:: aligned_pairs
      :type:  list[AlignedSegmentPair]
      :value: None



   .. py:attribute:: alignment_quality
      :type:  AlignmentQuality
      :value: None



   .. py:attribute:: alignment_stats
      :type:  dict[str, Any]
      :value: None



   .. py:class:: Config

      Pydantic config.


      .. py:attribute:: extra
         :value: 'allow'



      .. py:attribute:: use_enum_values
         :value: True




   .. py:method:: calculate_alignment_quality() -> AlignmentQuality

      Calculate overall alignment quality based on aligned pairs.



   .. py:method:: add_aligned_pair(source_segment: DocumentSegment | None, target_segment: DocumentSegment | None, confidence: float = 1.0) -> None

      Add an aligned segment pair.



   .. py:method:: get_alignment_summary() -> dict[str, Any]

      Get a summary of the alignment.
