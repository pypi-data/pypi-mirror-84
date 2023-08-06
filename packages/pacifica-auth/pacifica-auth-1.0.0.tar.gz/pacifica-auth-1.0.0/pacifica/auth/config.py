#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Configuration reading and validation module."""
from os import getenv
from configparser import ConfigParser


def common_config(configparser: ConfigParser):
    """Append common config to the parser."""
    configparser.add_section('cherrypy')
    configparser.set('cherrypy', 'host', getenv(
        'CHERRYPY_HOST', '0.0.0.0'))
    configparser.set('cherrypy', 'port', getenv(
        'CHERRYPY_PORT', '8080'))
    configparser.set('cherrypy', 'session_dir', getenv(
        'CHERRYPY_SESSION_DIR', 'sessions'))
    configparser.set('cherrypy', 'app_dir', getenv(
        'CHERRYPY_APP_DIR', ''))
    configparser.set('cherrypy', 'ssl_private_key', getenv(
        'CHERRYPY_SSL_PRIVATE_KEY', ''))
    configparser.set('cherrypy', 'ssl_certificate', getenv(
        'CHERRYPY_SSL_CERTIFICATE', ''))
    configparser.set('cherrypy', 'ssl_certificate_chain', getenv(
        'CHERRYPY_SSL_CERTIFICATE_CHAIN', ''))
    configparser.set('cherrypy', 'social_module', getenv(
        'CHERRYPY_SOCIAL_MODULE', 'github'))
    configparser.set('cherrypy', 'social_class', getenv(
        'CHERRYPY_SOCIAL_CLASS', 'GithubOAuth2'))
    configparser.add_section('social_settings')
    configparser.add_section('database')
    configparser.set('database', 'db_url', getenv(
        'DATABASE_CONNECT_URL', 'sqlite:///db.sqlite3'))
    configparser.set('database', 'connect_attempts', getenv(
        'DATABASE_CONNECT_ATTEMPTS', '10'))
    configparser.set('database', 'connect_wait', getenv(
        'DATABASE_CONNECT_WAIT', '20'))
    configparser.add_section('celery')
    configparser.set('celery', 'broker_url', getenv(
        'BROKER_URL', 'filesystem://'))
    configparser.set('celery', 'backend_url', getenv(
        'BACKEND_URL', 'rpc://'))
    configparser.set('celery', 'filesystem_broker_dir', getenv(
        'FILESYSTEM_BROKER_DIR', '/var/tmp'))
