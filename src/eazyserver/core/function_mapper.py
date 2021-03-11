# -*- coding: utf-8 -*-

"""
    eazyserver.core.function_mapper
    ~~~~~~~~~~~~~~~~~

    Class to build a dict of functions using decorators.

    License:
        GPL-2.0, see LICENSE for more details.
"""

import logging

logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)


class FunctionMapper:
    """
    FunctionMapper class to map functions to a str tag using decorators.
    """

    def __init__(self):
        """Initialize FunctionMapper class with no routes."""
        self.routes = {}

    def add(self, route_str):
        """Add a route to the Function Map.

        Args:
            route_str (str): route to be added to the map.
        """

        def decorator(f):
            self.routes[route_str] = f
            return f

        return decorator

    def get(self, path):
        """Get a function from the Function Map.

        Args:
            path (str): path of Function to be fetched.

        Raises:
            ValueError: ValueError

        Returns:
            function: function
        """
        view_function = self.routes.get(path)
        if view_function:
            return view_function
        else:
            raise ValueError('Route "{}"" has not been registered'.format(path))

    def _routes(self):
        """List routes

        Returns:
            list: List of routes
        """
        return self.routes.keys()
