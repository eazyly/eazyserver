# -*- coding: utf-8 -*-

"""
    eazyserver.rpc.influxdb
    ~~~~~~~~~~~~~~~~~

    RPC routes to read/write from InfluxDB.

    License:
        GPL-2.0, see LICENSE for more details.
"""

from ..rpc import methods
from eazyserver.core.influxdb_connector import write_points
import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)


@methods.add
def __write_to_influx(db, measurement, elements):
    """Write a data point to influxdb.

    Args:
        db (str): InfluxDB database to write to.
        measurement ([type]): [description]
        elements ([type]): [description]
    """
    write_points(db, measurement, elements)
