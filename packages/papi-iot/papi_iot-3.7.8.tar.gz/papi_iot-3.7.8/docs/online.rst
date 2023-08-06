===========================
Online Storage Operations
===========================

To optionally setup online storage, download the `Google Cloud service account json`_ and execute::

    papi.onlineStorage.connectToOnlineStorage("json/sevice/account/file/","photoStorageBucketName", "videoStorageBucketName")

To change photo storage location::

    papi.onlineStorage.setOnlinePhotoStorageLocation("newPhotoBucketLocation")

To change video storage location::

    papi.onlineStorage.setOnlineVideoStorageLocation("newVideoStorageLocation")

To store photos online::

    papi.onlineStorage.storeOnlinePhotos("/photo/storage/folder")

To store videos online::

    papi.onlineStorage.storeOnlineVideos("/video/storage/folder")

To get a photo from online storage::

    papi.onlineStorage.getOnlinePhoto("photoname", "/dest/folder/location")

To get multiple photos from online storage::

    papi.onlineStorage.getOnlinePhotos("/dest/folder/location", startsWith="starting letters")

To get a video from online storage::

    papi.onlineStorage.getOnlineVideo("videoname", "/dest/folder/location")

To get multiple videos from online storage::

    papi.onlineStorage.getOnlineVideos("/dest/folder/location", startsWith="starting letters")

.. _`Google Cloud service account json`: https://cloud.google.com/storage/docs/reference/libraries