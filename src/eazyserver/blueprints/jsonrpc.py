# -*- coding: utf-8 -*-

"""
    eazyserver.blueprints.jsonrpc
    ~~~~~~~~~~~~~~~~~

    Flask Blueprints for `jsonrpc` API routes.

    License:
        GPL-2.0, see LICENSE for more details.
"""

# import os
# import operator

from eazyserver.rpc.meta import __list_methods

from flask import (
    # Blueprint,
    jsonify,
    Response,
    # make_response,
    request,
    current_app as app,
)
import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)


# jsonrpc_bp = Blueprint('eazy_jsonrpc_routes', __name__)

# @jsonrpc_bp.route(
#   '/' + app.config["API_VERSION"] +
#   '/' + app.config["RPC_BASE_ROUTE"] +
#   '/' + app.config["RPC_ROUTE_NAME"],
#   methods=['POST'])
def call_rpc():
    """Calls a RPC method registered in app.methods object.

    Returns:
        str: JSON response in JSON-RPC 2.0 format
            (https://www.jsonrpc.org/specification)
    """
    req = request.get_data().decode()
    response = app.methods.dispatch(req)
    return Response(str(response), response.http_status, mimetype="application/json")


# @jsonrpc_bp.route(
#   '/' + app.config["API_VERSION"] +
#   '/' + app.config["RPC_BASE_ROUTE"] +
#   '/' + app.config["RPC_ROUTE_NAME"],
#   methods=['GET'])
def list_rpc():
    """Lists all the registered RPC methods in app.methods object.

    Returns:
        str: JSON response containing list of methods. Example:
             {"methods": ["method1", "method2"]}
    """
    response = {"methods": __list_methods()}
    return jsonify(response)
