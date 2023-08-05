========
OmlaxTCP
========


.. image:: https://img.shields.io/pypi/v/omlaxtcp.svg
        :target: https://pypi.python.org/pypi/omlaxtcp

.. image:: https://img.shields.io/travis/AadamAbrahams/omlaxtcp.svg
        :target: https://travis-ci.com/AadamAbrahams/omlaxtcp

.. image:: https://readthedocs.org/projects/omlaxtcp/badge/?version=latest
        :target: https://omlaxtcp.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




This Raspberry Pi-Python API provides functions for the configuration and operation of the Parallax 555-28027 PIR sensor and the Omron D6T-1A-02 temperature sensor. The data read from these modules may then be relayed via TCP protocols, from many clients to a single server, using a simplified rendition of the integrated Python Socket package.


* Free software: MIT license
* Documentation: https://omlaxtcp.readthedocs.io.


Features
--------

**Basic configuration and operation of:**
    * The Parallax 555-28027 PIR motion sensor.
    * The Omron D6T-1A-02 temperature sensor using I2C communication protocols.
    * TCP network protocols using a simplified rendition of the integrated Python Socket package.
	
**Additional functionality includes:**
	* Speed detection through the use of two PIR motion sensors seperated by a specified distance. 
	* Direction detection through the use of two PIR motion sensors opposing one another, such that one is triggered prior to the other.
	* Fever detection through the use of a single temperature sensor and a given maximum temperature boundary. (Can be used to determine if anything produces a temperature above a given maximum, not specifically human temperatures.)
    
Hardware and Software Prerequisites
-----------------------------------
A majority of the functions contained within this API may require a certain hardware module attached and/or a specific set of python libraries installed to operate as intended. However, in all instances that a hardware module is required, a Raspberry Pi (Any version) is necessary. 

To make use of any of the functions contained in motionSensor.py_, a Parallax 555-28027 PIR motion sensor is required and may be connected to a GPIO pin of choice. However, it would be possible to use any PIR motion sensor that has a single output pin, and that outputs 1 when triggered and 0 while untriggered.  
Note: Functions direc_detect_with_BuzzandTemp(motion_out, motion_in) and def init_trig_with_BuzzandTemp(motion) require that an Omron D6T-1A-02 temperature sensor is connected as well as a buzzer. 

To make use of any of the functions contained in tempSensor.py_, an Omron D6T-1A-02 temperature sensor is required and must be connected to the relevant I2C specific pins to allow for complete communication. The python packages pigpio, smbus2 and crcmod are essential and needed to be installed as follows::

    pip install pigpio smbus2 crcmod

It is also required, on Linux-based machines, that when a program that makes use of these functions is executed for the first time, the following line is asserted in the command line::

    sudo pigpiod

The functions defined in TCP.py_ do not require any additional hardware modules, it merely requires that the device implementing the subpackage be connected to a router. Such that, at a minimum, devices may communicate over the Local Area Network. If the user wishes to exchange data between devices over the internet, the device acting as the server is required to have its router port forwarding, on the relevant socket port, to the device in question.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _motionSensor.py: https://github.com/AadamAbrahams/OmlaxTCP/blob/master/omlaxtcp/motionSensor.py
.. _tempSensor.py: https://github.com/AadamAbrahams/OmlaxTCP/blob/master/omlaxtcp/tempSensor.py
.. _TCP.py: https://github.com/AadamAbrahams/OmlaxTCP/blob/master/omlaxtcp/TCP.py

