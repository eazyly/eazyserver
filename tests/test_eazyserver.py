#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_eazyserver
    ~~~~~~~~~~~~

    Tests for `eazyserver` package.

    :license: GPL-2.0, see LICENSE for more details.
"""


import unittest
from eazyserver import Eazy

# from pymongo import MongoClient

# from eazyserver import cli
# from click.testing import CliRunner


class TestEazyserver(unittest.TestCase):
    """Tests for `eazyserver` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        settings = {"DOMAIN": {}}
        self.app = Eazy(__name__, settings=settings)
        self.test_client = self.app.test_client()
        self.app.config["SWAGGER_HOST"] = self.app.config["HOST_NAME"]

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.app

    def test_000_something(self):
        """Test something."""
        resp = self.test_client.get(
            "/" + self.app.config["API_VERSION"] + "/", content_type="application_json"
        )
        self.assert200(resp.status_code)  # resp.get_json()

    def assert200(self, status):
        self.assertEqual(status, 200)

    # def dropDB(self):
    #     self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
    #     self.connection.drop_database(MONGO_DBNAME)
    #     self.connection.close()

    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.cli, ['run'])
    #     assert result.exit_code == 0
    #     assert 'eazyserver.cli.cli.run' in result.output
    #     help_result = runner.invoke(cli.cli, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
