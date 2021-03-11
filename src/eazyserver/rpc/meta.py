# -*- coding: utf-8 -*-

"""
    eazyserver.rpc.meta
    ~~~~~~~~~~~~~~~~~

    RPC routes to get meta-information regarding the RPC service.

    License:
        GPL-2.0, see LICENSE for more details.
"""

from ..rpc import methods
import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)


@methods.add
def __list_methods():
    """
    List all RPC methods registered.

    Returns:
        string[]: array of string listing all the RPC methods
    """
    result = []
    for method in methods:
        result.append(str(method))
    return result


@methods.add
def __ping():
    """Ping RPC.

    Returns:
        string: "pong"
    """
    logger.debug("Inside Ping Pong")
    return "pong"
