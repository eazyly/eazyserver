#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_live_server
    ~~~~~~~~~~~~

    Run a sample eazyserver based API server.

    :license: GPL-2.0, see LICENSE for more details.
"""

__author__ = """Ashutosh Mishra"""
__email__ = "ashutoshdtu@gmail.com"
__version__ = "0.1.1"

from eazyserver import Eazy

settings = {"DOMAIN": {}}

app = Eazy(__name__, settings=settings)
app.config["SWAGGER_HOST"] = app.config["HOST_NAME"]

app.run(
    host=app.config["HOST"],
    port=app.config["PORT"],
    threaded=app.config["THREADED"],
    debug=app.config["DEBUG"],
)
