#  Copyright (c) 2020 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
This is the Station Client that reads measurements from sensors and reports them to the station monitoring service.
The station client is typically run on a raspberry-pi. One RPi represents one station.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler

import requests
import urllib3


import auth
from constants import SENSOR_BME680, SENSOR_SHT31_D, SENSOR_TSL2591
from sensors.bme680 import BME680
from sensors.sht31d import SHT31D
from sensors.tsl2591 import TSL2591
from settings import log_file, log_max_bytes, log_backup_count, log_level, sensors, station_name, reports_endpoint, timeout

drivers = {
    SENSOR_BME680: BME680,
    SENSOR_SHT31_D: SHT31D,
    SENSOR_TSL2591: TSL2591
}


def main():
    """
    Main entry point for the station client. Reads the connected sensors one by one and submits the measurements reports collected from
    these sensors to the station-monitoring-service.
    """
    try:
        _init_logger()
        logging.info('Running RCM Station Client (%s)', station_name)
        # Disable warnings about unsecure connection, since HTTPS verify is set to False due to self signed certificate.
        urllib3.disable_warnings()
        for sensor in sensors.split(','):
            if sensor not in drivers.keys():
                raise ValueError('Unsupported sensor: ' + sensor)
            driver = drivers[sensor]()
            measurement_report = driver.read()
            _submit(measurement_report)
    except Exception as exception:
        print('Unexpected error: ', exception)
        logging.exception('Unexpected error: ', exc_info=exception)
        sys.exit(1)


def _init_logger():
    logger = logging.getLogger()
    handler = RotatingFileHandler(log_file, maxBytes=log_max_bytes, backupCount=log_backup_count)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)


def _submit(measurement_report):
    logging.debug('Submitting measurement report for station %s to %s', station_name, reports_endpoint)
    payload = {
        'stationName': station_name,
        'measurements': measurement_report
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {auth.get_token()}'
    }
    try:
        response = requests.post(reports_endpoint, json=payload, headers=headers, verify=False, timeout=timeout)
        response.raise_for_status()
    except Exception as exception:
        logging.exception('Failed to submit measurements report', exc_info=exception)
        sys.exit(1)


if __name__ == '__main__':
    main()
