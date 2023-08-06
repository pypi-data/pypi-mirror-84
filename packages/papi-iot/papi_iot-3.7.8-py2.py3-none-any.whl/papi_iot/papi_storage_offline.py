import os
import glob
from shutil import copy
from os import listdir
from os import makedirs
from os import path
from matplotlib import image
from papi_iot.papi_exceptions import DirectoryCreationFail

class OfflineStorage (object):
    rootDir = 'home/pi'
    knownFaces = '/knownFaces'
    unknownFaces = '/unknownFaces'

    def __init__(self):
        """
            Initial state of the object by assigning the values of the object’s properties.
            Create knownFaces and unknownFaces folders.
        """
        self.setOfflinePhotoStorageLocation()
        self.setOfflineVideoStorageLocation()
        
    def setOfflinePhotoStorageLocation(self):
        """
            Create the locations/folders for the known faces images and unknown faces images. 
            Paths created are /home/pi/photos/knownFaces and /home/pi/photos/unknownFaces 
        """

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
                print("Directory '%s' created successfully" %pathUknownFaces) 
            except OSError: 
                raise DirectoryCreationFail(pathUknownFaces)

    def getOfflinePhotoStorageLocation(self, category):
        """
            Obtain the path to known and unknown faces based on given category.

            Parameters
            ----------
            category : str
                Path choice. Can either be knownFaces or unknownFaces

            Returns
            -------
            Path : str
                Can either be path to knownFaces or unknownFaces folder
        """
        if category == 'knownFaces':
            return './' + self.rootDir + '/photos' + self.knownFaces
        else: 
            return './' + self.rootDir + '/photos' + self.unknownFaces

    def setOfflineVideoStorageLocation(self):
        """
            Create the locations/folder for videos. Path to video /home/pi/videos
        """
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
                filename : str
                    filename for image
                destination : str
                    location to store image
        """
        copy(filename, destination)

    def storeOfflineVideos(self, filename):
        """
            Store video from pi camera into the given video folder

            args:
                filename : str
                    filename for video
        """
        copy(filename, self.rootDir + '/videos')

    def getOfflinePhoto(self, destination):
        """
            Obtain photo based on destination given.

            args: 
                destination : str
                    filename for image
            
            return:
                image as pixel array
        """
        return image.imread(destination)

    def getOfflinePhotos(self):
        """
            Obtain all photos from both knownFaces and unknownFace folders

            return:
                knownFacesImageList : list
                    known faces image pixel array list
                unknownFacesImageList : list
                    unknown faces image pixel array list
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
        """
            Obtain list of vides in video folder

            Returns
            -------
            videoList : list
                list of videos 
        """
        videoList = list()
        for filename in listdir('./' + self.rootDir + '/videos'):
            videoData = image.imread('./' + self.rootDir + '/videos' + '/' + filename)
            videoList.append(videoData)

        return videoList

    def storeNewKnownUser(self, filename):
        """
            Store the new known person in the knownFaces folder. 
        """
        newFileName = filename.split('/')[-1]
        self.storeOfflinePhotos(filename,self.getOfflinePhotoStorageLocation('knownFaces') + '/' + newFileName)

    def storeNewKnownUsers(self, sourceFolder, picType='.jpg'):
        """

            Store known photos in known Faces folder

        """

        picLocationList = glob.glob(sourceFolder + '/' + picType)

        for picLocation in picLocationList:
            self.storeNewKnownUser(picLocation)


    def storeUnknownPhotos(self, sourceFolder, picType='.jpg'):
        """

            store unknown photos in unknown folder

        """

        picLocationList = glob.glob(sourceFolder + '/*' + picType)

        for picLocation in picLocationList:
            name = picLocation.split('/')[-1]
            newLocation = self.getOfflinePhotoStorageLocation('unknown') + '/' + name
            self.storeOfflinePhotos(picLocation, newLocation)

    def removeKnownUser(self, userName):
        """
            Remove the new known person in the knownFaces folder.

            Parameters
            ----------
            userName : str
                Name of the person to be removed

            Returns
            -------
            filename : bool
                removed file True or False
        """
        fileName = self.getOfflinePhotoStorageLocation('knownFaces') + '/' + userName + '.jpg'
        return self.removeFile(fileName)

    def removeFile(self, fileName):
        """
            Remove the file from given file name

            Parameters
            ----------
            filename : str
                remove file named filename  

            Returns
            -------
            removed : bool
                removed file True or False
        """
        removed = False

        if os.path.exists(fileName):
            os.remove(fileName)
            removed = True

        return removed
        

