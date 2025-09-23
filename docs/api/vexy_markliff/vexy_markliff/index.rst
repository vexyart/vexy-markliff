vexy_markliff.vexy_markliff
===========================

.. py:module:: vexy_markliff.vexy_markliff

.. autoapi-nested-parse::

   Core helpers for the vexy_markliff package.



Attributes
----------

.. autoapisummary::

   vexy_markliff.vexy_markliff.logger


Classes
-------

.. autoapisummary::

   vexy_markliff.vexy_markliff.Config


Functions
---------

.. autoapisummary::

   vexy_markliff.vexy_markliff.process_data
   vexy_markliff.vexy_markliff.main


Module Contents
---------------

.. py:data:: logger

.. py:class:: Config

   Minimal configuration container used by ``process_data``.


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: value
      :type:  str | int | float


   .. py:attribute:: options
      :type:  dict[str, Any] | None
      :value: None



.. py:function:: process_data(data: Any, config: Config | None = None, *, debug: bool = False) -> dict[str, Any]

   Normalize list data and provide a lightweight summary.


.. py:function:: main() -> None

   Main entry point for vexy_markliff.
