============================
Offline Storage Operations
============================

To add new user to offline storage::

    papi.offlineStorage.storeNewKnownUser('/photo/location/name.jpg')

To remove user from offline storage::

    papi.offlineStorage.removeKnownUser('name')

To get storage locations of photos and videoStorageBucketName::

    known_dir = papi.offlineStorage.getOfflinePhotoStorageLocation('knownFaces')
    unknown_dir = papi.offlineStorage.getOfflinePhotoStorageLocation('unknownFaces')
    vid_dir = papi.offlineStorage.getOfflineVideoStorageLocation()

To remove known users::

    papi.offlineStorage.removeKnownUser('name')