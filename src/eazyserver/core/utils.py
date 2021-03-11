# -*- coding: utf-8 -*-

"""
    eazyserver.core.utils
    ~~~~~~~~~~~~~~~~~

    Various utility functions for eazyserver.

    License:
        GPL-2.0, see LICENSE for more details.
"""

import json

# import sys

# if sys.version_info[0] >= 3:
#     from html.parser import HTMLParser
# else:
#     import HTMLParser
from bson import json_util

# from bson.son import SON
# from bson.objectid import ObjectId
# from eve.utils import str_to_date, date_to_rfc1123
from flask import current_app as app
import threading
import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)


def bson_to_json(_object):
    """Converts MongoDB BSON object to JSON (Python Object).

    Args:
        _object (BSON): BSON object

    Returns:
        object: Python object
    """
    return json.loads(json.dumps(_object, default=json_util.default))


def json_to_bson(_object):
    """Convert JSON (Python Object) to MongoDB BSON.

    Args:
        _object (object): Python object

    Returns:
        BSON: BSON object
    """
    return json_util.loads(json.dumps(_object))


def toJSON(_object):
    """Convert a python object to JSON.

    Args:
        _object (object): Python object

    Returns:
        str: JSON string.
    """
    return json.dumps(_object, default=lambda o: o.__str__(), sort_keys=True)


def failure_resp(message, code):
    """Generates failure response.

    Args:
        message (str): Failure response message
        code (inte): HTTP response code

    Returns:
        dict: failure response object
    """
    response = {"_status": "ERR", "_error": {"message": message, "code": code}}
    return response


# def unescape(s):
#     h = HTMLParser.HTMLParser()
#     return h.unescape(s)


def get_app_config_as_dict():
    """Get Eazy app config as a python dict.

    Returns:
        dict: app.config dict
    """
    response = {}
    for key in app.config:
        response[key] = app.config[key]
    return response


def list_routes(sort="endpoint", all_methods=False):
    """List all registered routes.

    Args:
        sort (str, optional): Sort routes by. Defaults to "endpoint".
        all_methods (bool, optional): Display all methods. Defaults to False.

    Returns:
        list: list of routes dict `{"title": <>, "href": <>, "methods": []}`
    """
    routes = []
    for rule in app.url_map.iter_rules():
        route = {
            "title": rule.endpoint,
            "href": str(rule.rule),
            "methods": sorted(rule.methods),
        }
        routes.append(route)
    return routes


# Execute a function call in thread
def threaded(call, *args, **kwargs):
    """Execute ``call(*args, **kwargs)`` in a thread.

    Args:
        call (function): function to be run in new thread.

    Returns:
        Thread: thread running the `call` function
    """
    thread = threading.Thread(target=call, args=args, kwargs=kwargs)
    thread.start()
    return thread


def is_main_thread_active():
    """Check if main thread is active

    Returns:
        bool: Returns `True` is main thread is running. `False` otherwise.
    """
    return any((i.name == "MainThread") and i.is_alive() for i in threading.enumerate())
