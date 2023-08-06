==================
API for IoT Module
==================


.. image:: https://img.shields.io/pypi/v/api_for_iot_module.svg
        :target: https://pypi.python.org/pypi/api_for_iot_module

.. image:: https://img.shields.io/travis/ChezzyBoi/api_for_iot_module.svg
        :target: https://travis-ci.com/ChezzyBoi/api_for_iot_module

.. image:: https://readthedocs.org/projects/api-for-iot-module/badge/?version=latest
        :target: https://api-for-iot-module.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




API for IoT Module contains functions to be used for implementing a API for a camera module 


* Free software: MIT license
* Documentation: https://api-for-iot-module.readthedocs.io.

Run
----

Start virtual environment
python3 -m venv venv
. venv/bin/activate
export FLASK_APP=app.py

Features
--------

The API has features to capture both video and still images from the raspberry pi camera and makes use of picamera methods to do so. The way that this API formats its data is by sending non-image data in the form of JSON objects, while image and video frames are send as JPEG binary objects. 

The API has methods to change various camera settings, which include the following:
 * Frame rate
 * Brightness 
 * Contrast
 * Saturatioin 
 * Sharpness
 * Exposure mode
 * Image effect (such as denoise, negative, cartoon and many other effects)

The API also have a motion detection function, where it compares the data of successive frames in the form of a numpy array and gives a alert when there are signficant changes between frames. 

Issues
-------

There is currently some issues we are facing with the travis builds that we hope to fix in the near future

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
