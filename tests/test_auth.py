"""Tests for the basicauth authenticator."""

from argparse import ArgumentParser
from contextlib import contextmanager
from os import environ, path, remove

import pytest
from pypiserver_basicauth.authenticator import HTTPBasicAuthenticator


def req(login, pw):
    """Create a mock request with the proper auth property."""
    return GenericNamespace(auth=(login, pw))

@pytest.fixture
def auth_server():
    """Use w3.org demo server to avoid setting up a server here"""
    return "https://jigsaw.w3.org/HTTP/Basic/"


@pytest.fixture
def valid_login():
    return req('guest','guest')


@pytest.fixture
def invalid_login():
    return req('guest','wrongpass')



@contextmanager
def update_env(**kwargs):
    """Update environment and then set it back."""
    start = environ.copy()
    environ.update(**kwargs)
    yield
    environ.clear()
    environ.update(**start)


class GenericNamespace(object):
    """A simple namespace object."""

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)




def test_authenticate_basicauth(auth_server,valid_login):
    """Test authenticating against auth server"""
    conf = GenericNamespace(basic_auth_url=auth_server)
    assert HTTPBasicAuthenticator(conf).authenticate(valid_login)


def test_authenticate_basicauth_fail(auth_server,invalid_login):
    """Test failing to authenticate against auth server."""
    conf = GenericNamespace(basic_auth_url=auth_server)
    assert not HTTPBasicAuthenticator(conf).authenticate(invalid_login)


def test_authenticate_none(invalid_login):
    """Test overriding auth."""
    conf = GenericNamespace(basic_auth_url='.')
    assert HTTPBasicAuthenticator(conf).authenticate(invalid_login)


class TestConfig(object):
    """Test config updates."""

    def test_updating_parser(self):
        """Test the updating of the argument parser."""
        parser = ArgumentParser()
        HTTPBasicAuthenticator.update_parser(parser)
        assert parser.parse_args().basic_auth_url is None

    def test_pull_from_env(self):
        """Test pulling from the environment."""
        with update_env(PYPISERVER_BASIC_AUTH_URL='foo'):
            parser = ArgumentParser()
            HTTPBasicAuthenticator.update_parser(parser)
            assert parser.parse_args().basic_auth_url == 'foo'

    def test_direct_specification(self):
        """Test specifying the password file directly."""
        parser = ArgumentParser()
        HTTPBasicAuthenticator.update_parser(parser)
        assert parser.parse_args(
            ['--http-basic-auth', 'bar']
        ).basic_auth_url == 'bar'
