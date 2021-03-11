# -*- coding: utf-8 -*-

"""
    eazyserver.eazy
    ~~~~~~~~~~~~
    This module implements the central WSGI application object as a Python Eve
    subclass.

    License:
        GPL-2.0, see LICENSE for more details.

    Raises:
        IOError: Could not read config files.

    Returns:
        Eazy: an eazyserver app.
"""

import os
import sys
import fnmatch

from events import Events
from flask import Config
from eve import Eve
from eve_swagger import get_swagger_blueprint  # , add_documentation
from eve.io.mongo import Mongo, Validator, GridFSMediaStorage

from .rpc import methods
import logging

# from .blueprints import config_bp, health_bp, index_bp, call_rpc, list_rpc


class Eazy(Eve, Events):
    """The main Eazy Class. On initialization it will load Eazy settings, then
    configure and enable the API endpoints using Python Eve.
    The API is launched by executing the code below:::

        app = Eve()
        app.run()

    Args:
        import_name (str, optional): the name of the application package.
            Defaults to `__package__`.
        settings (str, optional): the name of the settings file.
            Can be a dict or string(file name).
            Defaults to "settings.py".
        default_settings (str, optional): the name of the default settings file.
            Applied before settings file. Can only be filename/path.
            Defaults to `None`.
        validator (erberus.Validator, optional): custom validation class. Must be
            a :class:`~cerberus.Validator` subclass.
            Defaults to :class:`eve.io.mongo.Validator`.
        data (eve.io.DataLayer, optional): the data layer class. Must be
            a :class:`~eve.io.DataLayer` subclass. Defaults to :class:`~eve.io.Mongo`.
        auth (eve.auth.BasicAuth, optional): the authentication class used to
            authenticate incoming requests. Must be a :class: `eve.auth.BasicAuth`
            subclass. Defaults to `None`.
        redis (pyredis, optional): the redis (pyredis) instance used by the
            Rate-Limiting feature, if enabled. Defaults to `None`.
        url_converters (dict, optional): dictionary of Flask url_converters to add to
            supported ones (int, float, path, regex). Defaults to `None`.
        json_encoder (JSONEncoder, optional): custom json encoder class. Must be a
            JSONEncoder subclass. You probably want it to be
            as eve.io.base.BaseJSONEncoder subclass. Defaults to `None`.
        media (eve.io.media.MediaStorage, optional): the media storage class.
            Must be a :class:`~eve.io.media.MediaStorage` subclass.
            Defaults to `GridFSMediaStorage`.
        env_prefix (str, optional): Environment variable prefix for config variables.
            Defaults to "APP_".
        logger (logging, optional): Logger. Defaults to None.
        kwargs: optional, standard, Flask parameters.
    Raises:
        IOError: IOError

    Returns:
        Eazy: An eazyserver app.
    """

    methods = methods

    EAZY_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EAZY_DEFAULT_CONFIG_FILE = os.path.join(EAZY_BASE_DIR, "settings.ini")
    with open(os.path.join(EAZY_BASE_DIR, "VERSION")) as version_file:
        EAZY_VERSION = version_file.read().strip()

    def __init__(
        self,
        import_name=__package__,
        settings="settings.py",
        default_settings=None,
        validator=Validator,
        data=Mongo,
        auth=None,
        redis=None,
        url_converters=None,
        json_encoder=None,
        media=GridFSMediaStorage,
        env_prefix="APP_",
        logger=None,
        **kwargs
    ):
        """Eazy main WSGI app is implemented as a Eve subclass. Since we want
        to be able to launch our API by simply invoking Eve's run() method,
        we need to enhance our super-class a little bit.
        """
        if logger:
            self.logger = logger
        else:
            logger = logging.getLogger(import_name)
            self.logger = logger

        settings = self.load_eazy_config(settings, default_settings, env_prefix)

        super(Eazy, self).__init__(import_name, settings=settings, **kwargs)

        self.load_blueprints()

    def load_eazy_config(self, settings, default_settings, env_prefix):
        """
        Loads the config from environment variables and settings file.

        Load Order:
                EAZY_DEFAULT_CONFIG_FILE -> default_settings
                -> ( APP_SETTINGS (env)/ SETTINGS (conf) / settings )
                -> environment variables

        Args:
            settings (str): settings parameter passed to the constructor.
            default_settings (str): default settings file parameter passed to the
                constructor.
            env_prefix (str): Environment variable prefix for app config variables.

        Returns:
            Config: flask app config
        """
        config = self.initialize_config()

        # 1. Loads from settings.ini [Eazy default settings]
        self.logger.info(
            "Loading " + str(self.EAZY_DEFAULT_CONFIG_FILE) + " [default settings]..."
        )
        config = self.load_config_from_file(config, self.EAZY_DEFAULT_CONFIG_FILE)

        # 2. Load default settings for the app.
        if default_settings is not None:
            config = self.load_config_from_file(config, default_settings)

        # 3. if settings is a dict, just load the dict
        if isinstance(settings, dict):
            config.update(settings)

        # 4. Load environment setting for the app.
        # 4.1. if APP_SETTINGS environemt variable exists
        if env_prefix + "SETTINGS" in os.environ:
            config = self.load_config_from_file(
                config, os.environ[env_prefix + "SETTINGS"]
            )
        # 4.2. if SETTINGS key found in config dict
        elif "SETTINGS" in config:
            config = self.load_config_from_file(config, config["SETTINGS"])
        # 4.3. if settings is not None, load the file
        elif isinstance(settings, str):
            config = self.load_config_from_file(config, settings)

        # 5. Finally loads from Environment Variables with prefix env_prefix
        for a in os.environ:
            if a.startswith(env_prefix):
                config[a[len(env_prefix) :]] = os.getenv(a)

        # 6. Set non-changeable config variables
        config["VERSION"] = self.EAZY_VERSION

        return config

    def load_config_from_file(self, config, file_name):
        """Load a config file.

        Args:
            config (Config): Flask config object
            file_name (str): file name of settings file.

        Raises:
            IOError: Could not read file.

        Returns:
            Config: Flask config object
        """
        if os.path.isabs(file_name):
            pyfile = file_name
        else:
            pyfile = self.find_settings_file(file_name)

        if not pyfile:
            raise IOError("Could not load config file: " + str(file_name))

        try:
            self.logger.debug("Loading config from file: " + str(pyfile) + "...")
            config.from_pyfile(pyfile)
        except Exception as e:
            raise e
        return config

    def find_settings_file(self, file_name):
        """Find settings file and return full path.

        Args:
            file_name (str): full path of the settings file.`

        Returns:
            str: full file path
        """
        # check if we can locate the file from sys.argv[0]
        abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
        settings_file = os.path.join(abspath, file_name)
        if os.path.isfile(settings_file):
            return settings_file
        else:
            # try to find settings.py in one of the
            # paths in sys.path
            for p in sys.path:
                for root, dirs, files in os.walk(p):
                    for f in fnmatch.filter(files, file_name):
                        if os.path.isfile(os.path.join(root, f)):
                            return os.path.join(root, file_name)

    def initialize_config(self):
        """Used to create the config attribute by the Eazy constructor."""
        defaults = {}
        return Config("", defaults)

    def load_blueprints(self):
        """
        Load blueprints for common routes like swagger documentation,
        config, health and RPC routes.
        """
        from .blueprints import config_bp, health_bp, index_bp, call_rpc, list_rpc

        if self.config["ENABLE_SWAGGER_ROUTES"]:
            self.logger.debug("Enabling swagger routes...")
            swagger = get_swagger_blueprint()
            self.register_blueprint(swagger)
        if self.config["ENABLE_CONFIG_ROUTES"]:
            self.logger.debug("Enabling config routes...")
            self.register_blueprint(config_bp)
        if self.config["ENABLE_HEALTH_ROUTES"]:
            self.logger.debug("Enabling health routes...")
            self.register_blueprint(health_bp)
        if self.config["ENABLE_JSONRPC_ROUTES"]:
            self.logger.debug("Enabling RPC routes...")
            rpc_route = (
                "/"
                + self.config["API_VERSION"]
                + "/"
                + self.config["RPC_BASE_ROUTE"]
                + "/"
                + self.config["RPC_ROUTE_NAME"]
            )
            self.add_url_rule(
                rpc_route, "call_rpc", view_func=call_rpc, methods=["POST", "OPTIONS"]
            )
            self.add_url_rule(
                rpc_route, "list_rpc", view_func=list_rpc, methods=["GET", "OPTIONS"]
            )
        if self.config["ENABLE_INDEX_ROUTES"]:
            self.logger.debug("Enabling index routes...")
            self.register_blueprint(index_bp)
