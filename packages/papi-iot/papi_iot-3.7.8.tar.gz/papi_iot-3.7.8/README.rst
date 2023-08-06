========
PAPI IOT
========


.. image:: https://img.shields.io/pypi/v/papi_iot.svg
        :target: https://pypi.python.org/pypi/papi_iot

.. image:: https://img.shields.io/travis/Stelele/papi_iot.svg
        :target: https://travis-ci.com/Stelele/papi_iot

.. image:: https://readthedocs.org/projects/papi-iot/badge/?version=latest
        :target: https://papi-iot.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/Stelele/papi_iot/shield.svg
     :target: https://pyup.io/repos/github/Stelele/papi_iot/
     :alt: Updates

An API for home security system using raspberry Pi with Pi IR camera and facial recognition.

* Github repo: PAPI IOT
* Free software: MIT license
* Documentation: https://papi-iot.readthedocs.io.


Features
--------

* Face recognition from photos
* Face recognition from videos
* Pi camera  feature controls
* Storage Management: SD card memory and Google cloud storage


Quick Start
-----------

Pre-requisite
^^^^^^^^^^^^^^^^

* Minimum Raspberry Pi 0 w, 2GB is recommended for optimal Face recognition performance
* OpenCV_
* Dlib_
* face-recognition_ 
* `Raspberry Pi V2 Camera Module`_ 
* `Google Cloud Storage Severice Account`_ After this, download the service account json file for use with onlineStorage module
* `picamera Library`_
* Python>= 3.6 recommended.

Upon finishing up the above steps, download the requirements_ file and execute::

        $ pip install -r requirements.txt

to install the remaining dependancies.

Test module by running 
^^^^^^^^^^^^^^^^^^^^^^^^^

Test module by executing::

    >>> from papi_iot.papi_face_recognition import PapiFaceRecognition
    >>> test = PapiFaceRecognition()
    >>> test.faceRecognitionFromVideo()

This Tests storage management and face recognition from videos

To end program use 'Ctl'+'C' command

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _face-recognition: https://github.com/ageitgey/face_recognition
.. _Dlib: https://www.pyimagesearch.com/2017/05/01/install-dlib-raspberry-pi/
.. _OpenCV: https://www.learnopencv.com/install-opencv-4-on-raspberry-pi/
.. _`Raspberry Pi V2 Camera Module`: https://za.rs-online.com/web/p/raspberry-pi-cameras/9132673/
.. _`Google Cloud Storage Severice Account`: https://cloud.google.com/storage/docs/reference/libraries
.. _requirements: https://github.com/Stelele/papi_iot/blob/master/requirements.txt
.. _`picamera Library`: https://picamera.readthedocs.io/en/release-1.13/