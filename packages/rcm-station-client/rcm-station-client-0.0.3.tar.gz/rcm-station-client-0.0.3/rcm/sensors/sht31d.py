#  Copyright (c) 2020 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
The SHT31-D sensor - High precision Temperature & Humidity sensor
=================================================================

See https://www.adafruit.com/product/2857
"""
import logging

import adafruit_sht31d
from sensors.sensor import Sensor


class SHT31D(Sensor):
    """
    Concrete implementation of SHT31-D sensor.
    """
    def read(self):
        """
        Reads the temperature and relative humidity.
        """
        logging.info('Reading SHT31-D sensor')
        sensor = adafruit_sht31d.SHT31D(super().i2c)
        measurements = {
            'temperature': sensor.temperature,
            'humidity': sensor.relative_humidity
        }
        logging.info('Measurement: %s', measurements)
        return measurements
