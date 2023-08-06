==========================
Camera Video Operations
==========================

To auto-adjust to light::

    papi.cameraVideo.autoAdjustToLight()

To set to camera mode::

    papi.cameraVideo.setCameraMode()

To take photo::

    papi.cameraVideo.takePhoto('/dest/folder/location/photoName')

To record a video for a certain time::

    papi.cameraVideo.recordVideoFor("/dest/folder/location/videoName", length=60#) #length in seconds

To record continuously::

    papi.cameraVideo.recordVideo("/dest/folder/location/videoname")

To stop recording::

    papi.cameraVideo.stopVideoRecording()