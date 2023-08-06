#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Base application module."""
from argparse import ArgumentParser, Namespace
from os import makedirs, getenv
from os.path import isdir, join, dirname
import json
from configparser import ConfigParser
import importlib
import cherrypy
from jinja2 import Environment, FileSystemLoader
from .satool import SATool
from .saplugin import SAEnginePlugin
from .config import common_config
from .root import Root


def error_page_default(**kwargs):
    """Error page when something goes wrong."""
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return bytes(json.dumps(kwargs), 'utf-8')


def session_commit():
    """Commit the user session to the database."""
    # pylint: disable=no-member
    cherrypy.session.save()


def check_sa_module_class(sa_module, sa_class):
    """Check the combination of module and class."""
    try:
        sa_module = importlib.import_module('social_core.backends.{}'.format(sa_module))
    except ImportError as ex:
        raise ValueError('Module {} is not a social core backend'.format(sa_module)) from ex
    if not getattr(sa_module, sa_class, None):
        raise ValueError('Social core backend module {} has no class {}'.format(sa_module, sa_class))


def pacifica_auth_arguments(parser):
    """Add Pacifica authentication command line arguments."""
    parser.add_argument(
        '-c', '--config', metavar='CONFIG', type=str,
        default=getenv('CONFIG_FILE', 'config.ini'), dest='config', help='ingest config file'
    )


def social_settings(configparser: ConfigParser, user_class, user_import_path):
    """Setup the social settings for pacifica auth."""
    def load_user():
        """Load the user into the request."""
        # pylint: disable=no-member
        user_id = cherrypy.session.get('user_id')
        if user_id:
            cherrypy.request.user = cherrypy.request.db.query(user_class).get(user_id)
        else:
            cherrypy.request.user = None
    cherrypy.config.update({
        'SOCIAL_AUTH_USER_MODEL': user_import_path,
        'SOCIAL_AUTH_LOGIN_URL': '/login',
        'SOCIAL_AUTH_LOGIN_REDIRECT_URL': '/',
        'SOCIAL_AUTH_TRAILING_SLASH': True,
        'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': (
            'social_core.backends.{}.{}'.format(
                configparser.get('cherrypy', 'social_module'),
                configparser.get('cherrypy', 'social_class')
            ),
        )
    })
    for key in configparser.options('social_settings'):
        cherrypy.config.update({
            'SOCIAL_AUTH_{}'.format(key.upper()): configparser.get('social_settings', key)
        })
    check_sa_module_class(
        configparser.get('cherrypy', 'social_module'),
        configparser.get('cherrypy', 'social_class')
    )
    SAEnginePlugin(cherrypy.engine, configparser.get('database', 'db_url')).subscribe()
    if not isdir(configparser.get('cherrypy', 'session_dir')):
        makedirs(configparser.get('cherrypy', 'session_dir'))
    cherrypy.config.update({
        'server.socket_host': configparser.get('cherrypy', 'host'),
        'server.socket_port': configparser.getint('cherrypy', 'port'),
        'tools.sessions.on': True,
        'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
        'tools.sessions.storage_path': configparser.get('cherrypy', 'session_dir'),
        'tools.sessions.timeout': 60,
        'tools.db.on': True,
        'tools.authenticate.on': True,
    })
    for ssl_config_key in ['ssl_private_key', 'ssl_certificate', 'ssl_certificate_chain']:
        if configparser.get('cherrypy', ssl_config_key):
            cherrypy.config.update({
                'server.{}'.format(ssl_config_key): configparser.get('cherrypy', ssl_config_key)
            })
    cherrypy.tools.jinja2env = Environment(
        loader=FileSystemLoader(join(dirname(__file__), 'templates'))
    )
    cherrypy.tools.db = SATool()
    cherrypy.tools.authenticate = cherrypy.Tool('before_handler', load_user)
    cherrypy.tools.session = cherrypy.Tool('on_end_resource', session_commit)


def create_configparser(args: Namespace, config_callback=None):
    """Create the config parser and return it calling callback if given."""
    configparser = ConfigParser()
    common_config(configparser)
    if callable(config_callback):
        config_callback(configparser)
    configparser.read(args.config)
    return configparser


def create_argparser(description, parser_callback=None):
    """Create the argparser and return it."""
    parser = ArgumentParser(description=description)
    pacifica_auth_arguments(parser)
    if callable(parser_callback):
        parser_callback(parser)
    return parser


# pylint: disable=too-many-arguments
def command_setup(argv, description, user_class, user_import_path, config_callback=None, parser_callback=None):
    """Common setup for commands to execute."""
    parser = create_argparser(description, parser_callback)
    args = parser.parse_args(argv)
    configparser = create_configparser(args, config_callback)
    social_settings(configparser, user_class, user_import_path)
    return configparser


# pylint: disable=too-many-arguments
def quickstart(
    argv, description, user_class, user_import_path,
    swagger_path, config_callback=None, parser_callback=None
):
    """Simple wrapper around cherrypy quickstart."""
    configparser = command_setup(argv, description, user_class, user_import_path, config_callback, parser_callback)
    cherrypy.quickstart(
        Root(configparser.get('cherrypy', 'social_module'), configparser.get('cherrypy', 'app_dir')),
        '/',
        config={
            '/': {},
            '/swagger.yaml': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': join(
                    swagger_path, 'swagger.yaml'
                ),
            },
        }
    )
