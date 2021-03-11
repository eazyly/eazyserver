# -*- coding: utf-8 -*-

"""
    eazyserver.blueprints.indexroute
    ~~~~~~~~~~~~~~~~~

    Flask Blueprints for `index` API routes.

    License:
        GPL-2.0, see LICENSE for more details.
"""

import os

# import operator

from eazyserver.core.utils import list_routes  # toJSON, get_app_config_as_dict

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


index_bp = Blueprint("index", __name__)
"""Flask Blueprint with index route "/" displaying list of registered routes.
"""


@index_bp.route("/", methods=["GET"])
def index():
    """Index route.

    Returns:
        str: json with list of all routes registered on this app.
    """
    response = {
        "_links": {"all": list_routes()},
        "_meta": {"build": {"href": os.environ.get("CI_BUILD_LINK", "-")}},
    }
    return jsonify(response)
