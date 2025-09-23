vexy_markliff
=============

.. py:module:: vexy_markliff

.. autoapi-nested-parse::

   Top-level package for vexy_markliff.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /api/vexy_markliff/__version__/index
   /api/vexy_markliff/cli/index
   /api/vexy_markliff/config/index
   /api/vexy_markliff/core/index
   /api/vexy_markliff/exceptions/index
   /api/vexy_markliff/models/index
   /api/vexy_markliff/utils/index
   /api/vexy_markliff/vexy_markliff/index


Attributes
----------

.. autoapisummary::

   vexy_markliff.__version__


Classes
-------

.. autoapisummary::

   vexy_markliff.Config


Functions
---------

.. autoapisummary::

   vexy_markliff.main
   vexy_markliff.process_data


Package Contents
----------------

.. py:data:: __version__
   :type:  str

.. py:class:: Config

   Minimal configuration container used by ``process_data``.


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: value
      :type:  str | int | float


   .. py:attribute:: options
      :type:  dict[str, Any] | None
      :value: None



.. py:function:: main() -> None

   Main entry point for vexy_markliff.


.. py:function:: process_data(data: Any, config: Config | None = None, *, debug: bool = False) -> dict[str, Any]

   Normalize list data and provide a lightweight summary.
