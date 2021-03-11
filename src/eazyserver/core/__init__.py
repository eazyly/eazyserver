# -*- coding: utf-8 -*-

"""
    eazyserver.core
    ~~~~~~~~~~~~~~~~~

    Core module of eazyserver.

    This module exports the following submodules:

        - eazyserver.core.function_mapper: Class to build a dict of functions
                                           using decorators.
        - eazyserver.core.influxdb_connector: Connector for InfluxDB.
        - eazyserver.core.utils: Various utility functions for eazyserver.

    License:
        GPL-2.0, see LICENSE for more details.
"""

# from ..core.function_mapper import FunctionMapper
# mongo_pipelines = FunctionMapper()

from .function_mapper import FunctionMapper

# from .utils import *
# from .influxdb_connector import *
import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)
