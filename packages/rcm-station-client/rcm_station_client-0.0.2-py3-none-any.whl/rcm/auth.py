#  Copyright (c) 2020 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
Auth0 authentication
======================

When authentication is enabled, M2M access tokens are required in order for the station client to be able to submit measurement reports to
the station monitoring service.
When a token is requested, it will attempt to read the token from the cache and check if it hasn't expired yet.
Once the token is expired or if the token does not exist in cache, a request is made to Auth0 to obtain an new access token. The token is
written to a file along with the timestamp when it expires.
"""
import os.path
import sys

import logging
import time
import requests
from constants import LINE_SEP, MODE_READ, MODE_WRITE, SIXTY_SECONDS
from settings import timeout, auth_enabled, token_endpoint, client_id, client_secret, audience, token_file

_GRANT_TYPE_CLIENT_CREDENTIALS = 'client_credentials'
_ACCESS_TOKEN = 'access_token'
_EXPIRES_IN = 'expires_in'


def get_token():
    """
    Retrieve the access token for M2M authentication on the station monitoring service.
    Access tokens are 'cached' by writing them to a file locally.
    The file also contains the timestamp when the token expires. If the token was expired a new token will be retrieved.
    Returns None if authentication is disabled.
    """
    if not auth_enabled:
        logging.debug('Skipping authentication because it is disabled')
        return None

    token = _read_token()
    if token is None:
        token = _request_token()

    return token


def _request_token():
    """
    Make request to the Auth0 server to request a new M2M access token.
    When a token is successfully obtained it will be stored in cache for future reference.
    :return: the freshly obtained access token.
    """
    logging.debug('Requesting new access token')
    payload = {
        'grant_type': _GRANT_TYPE_CLIENT_CREDENTIALS,
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': audience
    }

    try:
        response = requests.post(token_endpoint, data=payload, timeout=timeout)
        logging.debug('Received token-endpoint response: %s', response)
        response.raise_for_status()
        data = response.json()
        token = data[_ACCESS_TOKEN]
        expires_in = data[_EXPIRES_IN]
    except Exception as exception:
        logging.exception('Failed to request token', exc_info=exception)
        sys.exit(1)

    _write_token(token, expires_in)
    return token


def _read_token():
    """Read token from cache and return it. Returns None if token was not present or has expired."""
    logging.debug('Reading token from cache')
    if not os.path.isfile(token_file):
        logging.debug('Token file does not exist')
        return None

    try:
        with open(token_file, MODE_READ) as file:
            content = file.read().splitlines()
            token = content[0]
            expires_at = float(content[1])
    except Exception as exception:
        logging.exception('Failed to read token from file', exc_info=exception)
        return None

    if expires_at <= time.time():
        logging.debug('Token expired')
        return None

    return token


def _write_token(access_token: str, expires_in: float):
    """
    Writes the token to the token file so it can be used for the next time until it expires.
    The access token is written to the first line. The timestamp when it expires is written to the second line.
    The timestamp is reduced with one minute so it will be renewed on time.

    :param access_token: The access token, excluding 'Bearer ' prefix
    :param expires_in: The number of seconds until the token will expire.
    """
    try:
        with open(token_file, MODE_WRITE) as file:
            token = access_token + LINE_SEP
            expires_at = str(time.time() + expires_in - SIXTY_SECONDS)
            file.writelines([token, expires_at])
    except Exception as exception:
        logging.exception('Failed to write token to file', exc_info=exception)
        sys.exit(1)
