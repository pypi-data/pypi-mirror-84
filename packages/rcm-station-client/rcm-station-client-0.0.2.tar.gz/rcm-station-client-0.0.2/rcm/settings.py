#  Copyright (c) 2020 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.
"""Application wide settings that are shared across multiple modules"""

import os
import sys
from distutils.util import strtobool

from dotenv import load_dotenv

from constants import ONE_MB, DEFAULT_GAIN, DEFAULT_IT_TIME

try:
    load_dotenv()

    # Logging
    log_file = os.getenv('log-file', '/home/pi/rcm-station-client.log')
    log_level = os.getenv('log-level', 'WARN')
    log_max_bytes = int(os.getenv('log-max-bytes', ONE_MB))
    log_backup_count = int(os.getenv('log-backup-count', '5'))

    # Requests
    timeout = int(os.getenv('requests-timeout', '5'))

    # RCM specific
    reports_endpoint = os.getenv('measurements-report-endpoint', 'https://localhost:8080/measurement-reports')
    station_name = os.getenv('station-name')
    sensors = os.getenv('sensors')

    gain = os.getenv('tsl2591-gain', DEFAULT_GAIN)
    integration_time = os.getenv('tsl2591-integration-time', DEFAULT_IT_TIME)

    # Security
    # pylint: disable=invalid-name
    auth_enabled = bool(strtobool(os.getenv('auth-enabled', 'true')))
    token_endpoint = os.getenv('auth-token-endpoint')
    client_id = os.getenv('auth-client-id')
    client_secret = os.getenv('auth-client-secret')
    audience = os.getenv('auth-audience')
    token_file = os.getenv('token-file', 'token.txt')

    # Validation
    if sensors is None:
        raise ValueError('No sensors configured. Please specify at least one sensor in "sensors" in the .env file')
    if auth_enabled and (token_endpoint is None or client_id is None or client_secret is None or audience is None):
        raise ValueError('Auth is not configured properly, please double check settings')
except Exception as exception:
    print('Invalid configuration', exception)
    sys.exit(1)
