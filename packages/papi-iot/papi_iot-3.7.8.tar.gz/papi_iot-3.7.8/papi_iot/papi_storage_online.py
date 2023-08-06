from google.cloud import storage
from papi_iot.papi_exceptions import BlobNotFound, NoBlobsFound
from google.cloud.exceptions import NotFound
import glob

class OnlineStorage:

    def __init__(self):

        self.onlineStorageCredentials = None
        self.onlinePhotoStorageLocation = None
        self.onlineVideoStorageLocation = None
        self.photoBucket = None
        self.videoBucket = None

    def connectToOnlineStorage(self, credentialsFile, photoLocation, videoLocation):
        """

            Instatiates a connection to the Google cloud consol for specified service account
            --------------------------------------------------------------------------------------
            Variables
                credentialsFile -- location of service_account json file obtained from console
                photoLocation -- name of bucket to store photos created in console
                videoLocation -- name of bucket to store videos created in console

        """

        self.onlinePhotoStorageLocation = photoLocation
        self.onlineVideoStorageLocation = videoLocation

        self.onlineStorageCredentials = storage.Client.from_service_account_json(credentialsFile)

        try:
            self.photoBucket = self.onlineStorageCredentials.get_bucket(self.onlinePhotoStorageLocation)
        except NotFound:
            self.photoBucket = self.onlineStorageCredentials.create_bucket(self.onlinePhotoStorageLocation)

        try:
            self.videoBucket = self.onlineStorageCredentials.get_bucket(self.onlineVideoStorageLocation)
        except NotFound:
            self.videoBucket = self.onlineStorageCredentials.create_bucket(self.onlineVideoStorageLocation)

    def setOnlinePhotoStorageLocation(self, photoLocation):
        """

            Change bucket location storing photos
            --------------------------------------
            Variables
                photoLocation -- name of bucket to store photos created in console

        """

        self.onlinePhotoStorageLocation = photoLocation

        try:
            self.photoBucket = self.onlineStorageCredentials.get_bucket(self.onlinePhotoStorageLocation)
        except NotFound:
            self.photoBucket = self.onlineStorageCredentials.create_bucket(self.onlinePhotoStorageLocation)
            
    def setOnlineVideoStorageLocation(self, videoLocation):
        """

            Change bucket location storing videos
            ----------------------------------------------
            Variables
                videoLocation -- name of bucket to store videos created in console

        """
        self.onlineVideoStorageLocation = videoLocation
        try:
            self.videoBucket = self.onlineStorageCredentials.get_bucket(self.onlineVideoStorageLocation)
        except NotFound:
            self.videoBucket = self.onlineStorageCredentials.create_bucket(self.onlineVideoStorageLocation)

    def storeOnlinePhotos(self, folderLocation, picType='.jpg', approvedUser=True):
        """

            Upload all photos in a location to the photoLocation bucket
            --------------------------------------------------------------------
            Variables

                folderLocation -- folder location containing photos to be uploaded
                picType -- default '.jpg' picture file format to be uploaded
                approvedUser -- default True, if True photos marked as approved users if false, photos marked as banned users

        """
        picLocationList = glob.glob(folderLocation + '/*' + picType)
        
        for picLocation in picLocationList:
            self.uploadFile(picLocation, approvedUser=approvedUser) 
        
    def storeOnlineVideos(self, folderLocation, videoType='.h264'):
        """

            Upload all videos in a location to the videoLocation bucket
            -----------------------------------------------------------------
            Variables
                folderLocation -- folder location containing videos to be uploaded
                videoType -- default '.h264' video file format to be uploaded

        """
        vidLocationList = glob.glob(folderLocation + '/*' + videoType)

        for vidLocation in vidLocationList:
            self.uploadFile(vidLocation, photoUpload = False)

    def uploadFile(self, fileLocation, photoUpload=True, approvedUser=True):
        """

            Upload a file to either video or photo bucket
            ----------------------------------------------------
            Variables
                fileLocation -- location containing file to be uploaed e.g. /path/to/file/sample.jpg
                photoUpload -- default True if true uploads to photoLocation bucket else uploads to videoLocation bucket
                approvedUser -- default True if photoUpload is true, this marks file as approved if approvedUser is True else marks file as banned

        """
        blob = None
        fileName = fileLocation.split('/')[-1]

        if photoUpload:
            prepend = 'approved_' if approvedUser else 'banned_'
            blob = self.photoBucket.blob(prepend + fileName)
        else:
            blob = self.videoBucket.blob(fileName)

        blob.upload_from_filename(fileLocation)

    def getOnlinePhoto(self, photoName, destPhotoLocation, approvedUser=True):
        """

            download photo from photoLocation bucket
            ---------------------------------------------
            Variables
                photoName -- name of photo in photoLocation bucket
                destPhotoLocation -- folder to download photo to e.g. path/to/save
                approvedUser -- default True if True searchs in approved user list else searches in banned user list

        """
        prepend = 'approved_' if approvedUser else 'banned_'

        blob = self.photoBucket.get_blob(prepend + photoName)

        if blob != None:
            blob.download_to_filename(destPhotoLocation + '/' + photoName)
        else:
            raise BlobNotFound(photoName)

    def getOnlinePhotos(self, destPhotoLocation, approvedUser=True, startsWith=""):
        """

            download multiple photos from photoLocation bucket
            -----------------------------------------------------
            Variables
                destPhotoLocation -- folder to download photos to e.g. path/to/save
                approvedUser -- default True if True searchs in approved user list else searches in banned user list
                startsWith -- default "" only obtain files that start with given phrase. if "" retrieves all files in bucket

        """
        prepend = ('approved_' if approvedUser else 'banned_')

        blobs = list(self.photoBucket.list_blobs(prefix=prepend + startsWith))

        if len(blobs) > 0:
            for blob in blobs:
                photoName = blob.name.replace(prepend, "")
                blob.download_to_filename(destPhotoLocation + '/' + photoName)

        else:
            raise NoBlobsFound

    def getOnlineVideo(self, videoName, destVideoLocation):
        """

           download a video from the videoLocation bucket
           ---------------------------------------------------
           Variables
                videoName -- name of video in videoLocation bucket
                destVideoLocation -- folder to download video to e.g. path/to/save
        """
        blob = self.videoBucket.get_blob(videoName)

        if blob != None:
            blob.download_to_filename(destVideoLocation + '/' + videoName)

        else:
            raise BlobNotFound(videoName)

    def getOnlineVideos(self, destVideoLocation, startsWith=""):
        """

            download multiple videos from the videoLocation bucket
            -----------------------------------------------------------
            Variables
                destVideoLocation -- folder to download videos to e.g. path/to/save
                startsWith -- default "" only obtain videos that start with given phrase. if "" retrieves all videos in videoLocation bucket
        """
        
        blobs = list(self.videoBucket.list_blobs(prefix=startsWith))

        if len(blobs) > 0:
            for blob in blobs:
                blob.download_to_filename(destVideoLocation + '/' + blob.name)

        else:
            raise NoBlobsFound


