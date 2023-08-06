#  Copyright (c) 2020 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rcm-station-client",
    version="0.0.2",
    author="Pim Hazebroek",
    author_email="rcm@pimhazebroek.nl",
    description="Collects measurement reports from various sensors and send them to the station-monitoring-service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/residential-climate-monitoring/station-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
