vexy_markliff.utils.logging
===========================

.. py:module:: vexy_markliff.utils.logging

.. autoapi-nested-parse::

   Logging utilities for vexy-markliff.



Attributes
----------

.. autoapisummary::

   vexy_markliff.utils.logging.debug
   vexy_markliff.utils.logging.info
   vexy_markliff.utils.logging.warning
   vexy_markliff.utils.logging.error
   vexy_markliff.utils.logging.critical
   vexy_markliff.utils.logging.exception


Functions
---------

.. autoapisummary::

   vexy_markliff.utils.logging.setup_logging
   vexy_markliff.utils.logging.get_logger


Module Contents
---------------

.. py:function:: setup_logging(level: str = 'INFO', verbose: bool = False, log_file: str | None = None) -> None

   Set up logging configuration.

   :param level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   :param verbose: Enable verbose debug logging
   :param log_file: Optional log file path


.. py:function:: get_logger(name: str | None = None) -> Any

   Get a logger instance.

   :param name: Logger name (module name typically)

   :returns: Logger instance


.. py:data:: debug

.. py:data:: info

.. py:data:: warning

.. py:data:: error

.. py:data:: critical

.. py:data:: exception
