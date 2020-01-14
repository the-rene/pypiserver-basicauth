"""Authentication based on an htpasswd file."""

from os import environ
from textwrap import dedent
import requests
from pypiserver.plugins.authenticators.interface import AuthenticatorInterface


class HTTPBasicAuthenticator(AuthenticatorInterface):
    """Authenticate using requests and a server with HTTP basic Auth"""

    plugin_name = 'HTTP Basic  Authenticator'
    plugin_help = 'Authenticate using a server with HTTP basic Auth'

    def __init__(self, config):
        """Instantiate the authenticator."""
        self.config = config

    @classmethod
    def update_parser(cls, parser):
        """Add basicauth arguments to the config parser.

        :param argparse.ArgumentParser parser: the config parser
        """
        parser.add_argument(
            '--http-basic-auth',
            dest='basic_auth_url',
            default=environ.get('PYPISERVER_BASIC_AUTH_URL'),
            help=dedent('''\
                configure http server with basic auth to set usernames &
                passwords when authenticating certain actions (see -a option).
                Set to "." to disable password authentication.
            ''')
        )

    def authenticate(self, request):
        """Authenticate the provided request."""
        if (self.config.basic_auth_url is None or
                self.config.basic_auth_url == '.'):
            return True
        response = requests.get(auth_url, auth=(user, password))
        # user is authenticated, if status code is 2xx
        return response.status_code in range(200, 299)
