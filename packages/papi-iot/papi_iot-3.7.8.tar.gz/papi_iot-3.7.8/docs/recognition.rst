==============================
Face Recognition Operations
==============================

Instatiating photos in database
---------------------------------

To load unknown faces to categorise::

    papi.offlineStorage.storeUnknownPhotos('/source/folder/location')

To load known faces to database::

    papi.offlineStorage.storeNewKnownUsers('/source/folder/location')

Facial Recognition from photos
-------------------------------

To categorise faces in the unknown faces folder::

    papi.faceRecognition.faceRecognitionFromPhoto()

To compare if the same user is in the same photo::

    papi.faceRecognition.checkSamePerson('/first/photo/location/name1.jpg', '/second/photo/location/name2.jpg')

Facial Recognition from videos
-------------------------------

To recognise faces from a live video feed::

    papi.faceRecognition.faceRecognitionFromVideo()

To recognise faces from a video file::

    papi.faceRecognition.faceRecognitionFromVideoFile('/folder/location/video.mp4')
