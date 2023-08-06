#!/usr/bin/env python

"""The setup script."""

import pathlib
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


test_requirements = ['pytest>=3', ]

HERE = pathlib.Path(__file__).parent
README = (HERE/"README.rst").read_text()

setup(
    author="Zidaan Habib, Fraser Montandon",
    author_email='hbbzid001@myuct.ac.za',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="An API to facilitate interaction with an agriculture tech sensor kit.",
    entry_points={
        'console_scripts': [
            'agro_kit=agro_kit.__main__:main',
        ],
    },
    install_requires=["Adafruit_GPIO",
        "Adafruit_MCP3008",
        "file-read-backwards",
        "requests",
        "pynmea2",
        "adafruit-circuitpython-tcs34725",
        "RPi.GPIO",
        "Adafruit-Blinka"
        ],
    license="GNU General Public License v3",
    long_description=README,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords='agro_kit',
    name='agro_kit',
    #packages=find_packages(include=['agro_kit', 'agro_kit.*']),
    packages=["agro_kit", "moisture_sensor", "light_sensor", "gps"],
    #setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=["pytest"],
    url='https://github.com/ZidaanHabib/agro_kit',
    version='1.0.1',
    zip_safe=False,
)
