#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the example module."""
from os import getenv, unlink
from os.path import isfile
from sqlalchemy import create_engine
import cherrypy
from cherrypy.test import helper
import requests
from pacifica.auth import auth_session, error_page_default, command_setup
from pacifica.auth.user_model import User, Base
from pacifica.auth.root import Root


# pylint: disable=too-few-public-methods
class HelloWorld:
    """Example cherrypy hello world app."""

    exposed = True

    @cherrypy.tools.json_out()
    @auth_session
    # pylint: disable=no-self-use
    # pylint: disable=invalid-name
    def GET(self, error=None):
        """Example get method."""
        if error:
            raise cherrypy.HTTPError(500, error)
        return {'message': 'Hello World!'}


class TestExampleAuth(helper.CPWebCase):
    """Test the example class."""

    PORT = 8080
    HOST = '127.0.0.1'
    url = 'http://{0}:{1}'.format(HOST, PORT)

    @classmethod
    def setup_server(cls):
        """Setup the server configs."""
        cherrypy.tree.mount(HelloWorld(), '/hello', config={
            '/': {
                'error_page.default': error_page_default,
                'request.dispatch': cherrypy.dispatch.MethodDispatcher()
            }
        })
        configparser = command_setup([], 'Some Test Description', User, 'pacifica.auth.user_model.User')
        configparser.set('social_settings', 'github_key', getenv('PA_TESTING_GITHUB_KEY', ''))
        configparser.set('social_settings', 'github_secret', getenv('PA_TESTING_GITHUB_SECRET', ''))
        cherrypy.tree.mount(Root(configparser.get('cherrypy', 'social_module'),
                                 configparser.get('cherrypy', 'app_dir')), '/', config={'/': {}})
        cls._configparser = configparser

    def setUp(self) -> None:
        """Setup the test by creating database schema."""
        engine = create_engine(self._configparser.get('database', 'db_url'))
        Base.metadata.create_all(engine)
        # this needs to be imported after cherrypy settings are applied.
        # pylint: disable=import-outside-toplevel
        from social_cherrypy.models import SocialBase
        SocialBase.metadata.create_all(engine)

    def tearDown(self) -> None:
        """Tear down the test by deleting the database."""
        if isfile('database.sqlite3'):
            unlink('database.sqlite3')

    def test_main(self):
        """Test the add method in example class."""
        resp = requests.get('{}/hello'.format(self.url), allow_redirects=False)
        self.assertEqual(resp.status_code, 303)
        self.assertEqual(resp.headers['Location'], '{}/'.format(self.url))
        resp = requests.get(resp.headers['Location'], allow_redirects=False)
        self.assertEqual(resp.status_code, 303)
        self.assertEqual(resp.headers['Location'], '{}/login/github'.format(self.url))
        resp = requests.get(resp.headers['Location'], allow_redirects=False)
        self.assertEqual(resp.status_code, 303)
        self.assertTrue('https://github.com/login/oauth/authorize' in resp.headers['Location'])
