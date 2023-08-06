import os
from shutil import copy
from os import listdir
from os import makedirs
from os import path
from matplotlib import image
from papi_iot.papi_exceptions import DirectoryCreationFail

class OfflineStorage (object):
    rootDir = 'home/pi'
    knownFaces = '/knownFaces'
    # nameLabel = '/name'
    unknownFaces = '/unknownFaces'

    def __init__(self):
        """
            Initial state of the object by assigning the values of the object’s properties.
            Create knownFaces and unknownFaces folders.
        """
        self.setOfflinePhotoStorageLocation()
        self.setOfflineVideoStorageLocation()
        
    def setOfflinePhotoStorageLocation(self):
        pathKnownFaces = self.rootDir + '/photos' +  self.knownFaces
        pathUknownFaces = self.rootDir + '/photos' +  self.unknownFaces
        
        if (path.isdir(pathKnownFaces) == False):
            try: 
                makedirs(pathKnownFaces,exist_ok = True)
            except OSError: 
                raise DirectoryCreationFail(pathKnownFaces)

        if (path.isdir(pathUknownFaces) == False):
            try: 
                makedirs(pathUknownFaces,exist_ok = True)
            except OSError: 
                raise DirectoryCreationFail(pathUknownFaces)

    def getOfflinePhotoStorageLocation(self, category):
        if category == 'knownFaces':
            return './' + self.rootDir + '/photos' + self.knownFaces
        else: 
            return './' + self.rootDir + '/photos' + self.unknownFaces

    def setOfflineVideoStorageLocation(self):
        pathVideos = self.rootDir + '/videos'
        if (path.isdir(pathVideos) == False):
            try: 
                makedirs(pathVideos, exist_ok = True)
            except OSError as error: 
                raise DirectoryCreationFail(pathVideos)
    
    def getOfflineVideoStorageLocation(self):
        return self.rootDir + '/videos'

    def storeOfflinePhotos(self, filename, destination):
        """
            Store photos from pi camera into the given folder

            args:
                filename (string): filename for image
                destination (string): location to store image
        """
        copy(filename, destination)

    def storeOfflineVideos(self, filename):
        """
            Store video from pi camera into the given video folder

            args:
                filename (string): filename for video
        """
        copy(filename, self.rootDir + '/videos')

    def getOfflinePhoto(self, destination):
        """
            Obtain photo based on destination given.

            args: 
                destination (string): filename for image
            
            return:
                image as pixel array
        """
        return image.imread(destination)

    def getOfflinePhotos(self):
        """
            Obtain all photos from both knownFaces and unknownFace folders

            return:
                knownFacesImageList (list): known faces image pixel array list
                unknownFacesImageList (list): unknown faces image pixel array list
        """
        knownFacesImageList = list()
        unknownFacesImageList = list()
        for filename in listdir('./' + self.rootDir + '/photos' +  self.knownFaces):
            imgData = image.imread('./' + self.rootDir + '/photos' +  self.knownFaces + '/' + filename)
            knownFacesImageList.append(imgData)

        for filename in listdir('./' + self.rootDir + '/photos' +  self.unknownFaces):
            imgData = image.imread('./' + self.rootDir + '/photos' +  self.unknownFaces + '/' + filename)
            unknownFacesImageList.append(imgData)

        return knownFacesImageList, unknownFacesImageList

    def getOfflinesVideo(self):
        videoList = list()
        for filename in listdir('./' + self.rootDir + '/videos'):
            videoData = image.imread('./' + self.rootDir + '/videos' + '/' + filename)
            videoList.append(videoData)

        return videoList

    def storeNewKnownUser(self, filename):
        self.storeOfflinePhotos(filename,self.getOfflinePhotoStorageLocation('knownFaces') + '/' + filename)

    def removeKnownUser(self, userName):
        fileName = self.getOfflinePhotoStorageLocation('knownFaces') + '/' + userName + '.jpg'
        return self.removeFile(fileName)

    def removeFile(self, fileName):
        removed = False

        if os.path.exists(fileName):
            os.remove(fileName)
            removed = True

        return removed
        

