# -*- coding: utf-8 -*-

"""
    eazyserver.rpc
    ~~~~~~~~~~~~~~~~~

    Common RPC routes to enable for the Eazy app.

    This modle exports the following submodules:
        - eazyserver.rpc.exceptions: RPC calls exceptions
        - eazyserver.rpc.influxdb : RPC calls for InfluxDB read/write
        - eazyserver.rpc.meta: RPC calls to get info about the RPC service.

    License:
        GPL-2.0, see LICENSE for more details.
"""

import logging

from jsonrpcserver import methods

from .exceptions import (
    JsonRpcServerError,
    ParseError,
    InvalidRequest,
    MethodNotFound,
    InvalidParams,
    ServerError,
)

# from .influxdb import *
# from .meta import *

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)
