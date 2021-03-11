# -*- coding: utf-8 -*-

"""
    eazyserver.blueprints
    ~~~~~~~~~~~~~~~~~

    Flask blueprints for Commonly used routes like health, config, index etc.

    This modle exports the following submodules:
        - eazyserver.blueprints.config: Blueprints for `config` API routes.
        - eazyserver.blueprints.healthz : Blueprints for `health` API routes.
        - eazyserver.blueprints.indexroute: Blueprints for `index` API route.

    License:
        GPL-2.0, see LICENSE for more details.
"""

from .config import config_bp
from .healthz import health_bp
from .indexroute import index_bp
from .jsonrpc import call_rpc, list_rpc

import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)
