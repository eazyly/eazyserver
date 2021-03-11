# -*- coding: utf-8 -*-

"""
    eazyserver.rpc.exceptions
    ~~~~~~~~~~~~~~~~~

    Exceptions that can be thrown by RPC calls.

    License:
        GPL-2.0, see LICENSE for more details.
"""

from jsonrpcserver.exceptions import (
    JsonRpcServerError,
    ParseError,
    InvalidRequest,
    MethodNotFound,
    InvalidParams,
    ServerError,
)
