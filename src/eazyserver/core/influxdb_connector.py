# -*- coding: utf-8 -*-

"""
    eazyserver.core.influxdb_connector
    ~~~~~~~~~~~~~~~~~

    Connector for InfluxDB.

    License:
        GPL-2.0, see LICENSE for more details.
"""

import datetime
from flask import current_app as app

from influxdb import InfluxDBClient
import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)


clients = {}


def init_influxdb_client(db):
    """
    Initialize influxdb database.

    Args:
        db (str): InfluxDB database to connect to.
    """
    if db not in clients.keys():
        clients[db] = InfluxDBClient(
            app.config["INFLUX_HOST"],
            app.config["INFLUX_PORT"],
            app.config["INFLUX_USER"],
            app.config["INFLUX_PASSWORD"],
            db,
        )
    return clients


def get_current_time():
    """
    Get current time (formatted: `%Y-%m-%dT%H:%M:%SZ`)

    Returns:
        str: Current time.
    """
    # return datetime.datetime.utcnow().isoformat()
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def write_points(db, measurement, elements):
    """
    Write a data point to influxdb.

    Args:
        db (str): InfluxDB database to write to.
        measurement ([type]): [description]
        elements ([type]): [description]
    """
    init_influxdb_client(db)
    for element in elements:
        if "time" not in element:
            element["time"] = get_current_time()
        element["measurement"] = measurement
    logger.debug("Write points: {0}".format(elements))
    clients[db].write_points(elements)
