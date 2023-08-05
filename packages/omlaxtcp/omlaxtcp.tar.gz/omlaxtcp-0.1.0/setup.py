#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Aadam Abrahams",
    author_email='aadam1999@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="This API provides functions for the configuration and operation of the Parallax 555-28027 PIR sensor and the Omron D6T-1A-02 temperature sensor. The data read from these modules may then be relayed via TCP protocols, from many clients to a single server, using a simplified rendition of the integrated Python Socket package.",
    entry_points={
        'console_scripts': [
            'omlaxtcp=omlaxtcp.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='omlaxtcp',
    name='omlaxtcp',
    packages=find_packages(include=['omlaxtcp']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AadamAbrahams/omlaxtcp',
    version='0.1.0',
    zip_safe=False,
)
