# -*- coding: utf-8 -*-

"""
    eazyserver.blueprints.healthz
    ~~~~~~~~~~~~~~~~~

    Flask Blueprints for `health` API routes.

    License:
        GPL-2.0, see LICENSE for more details.
"""

# import os
# import operator

from flask import (
    Blueprint,
    jsonify,
    # Response,
    # make_response,
    # request,
    # current_app as app,
)
import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)


health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    response = {"status": "UP", "checks": []}
    return jsonify(response)


@health_bp.route("/ready", methods=["GET"])
def ready():
    response = {"status": "UP", "checks": []}
    return jsonify(response)
