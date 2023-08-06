"""Main module."""
from papi_iot.papi_face_recognition import PapiFaceRecognition
from papi_iot.papi_storage_manager import StorageManager
from papi_iot.papi_camera_video import PapiCameraVideo

class PAPIIOT:
    def __init__(self):
        self.faceRecognition = PapiFaceRecognition()
        self.storageManager = StorageManager()
        self.cameraVideo = PapiCameraVideo()


