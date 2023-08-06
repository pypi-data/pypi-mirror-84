#!/usr/bin/env python

"""Tests for `papi_iot` package."""

import pytest
import sys
import fake_rpi
from os import path

sys.modules['picamera'] = fake_rpi.picamera
from papi_iot.papi_iot import PAPIIOT

def test_photo_dir_creation():
    papi = PAPIIOT()

    papi.storageManager.offlineStorage.setOfflinePhotoStorageLocation()
   
    assert path.isdir(papi.storageManager.offlineStorage.getOfflinePhotoStorageLocation('knownFaces')) == True
    assert path.isdir(papi.storageManager.offlineStorage.getOfflinePhotoStorageLocation('unkownFaces')) == True

def test_video_dir_creation():
    papi = PAPIIOT()
    papi.storageManager.offlineStorage.setOfflineVideoStorageLocation()
    assert path.isdir(papi.storageManager.offlineStorage.getOfflineVideoStorageLocation()) == True




