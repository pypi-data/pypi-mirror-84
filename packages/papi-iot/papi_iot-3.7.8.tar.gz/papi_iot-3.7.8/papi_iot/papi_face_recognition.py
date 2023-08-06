import face_recognition
import os
import cv2
import time
import numpy as np
from papi_iot.papi_storage_offline import OfflineStorage
import random

class PapiFaceRecognition (object):
    def __init__ (self):
        """
            Initial state of the object by assigning the values of the object’s properties
        """

        offlineStorage = OfflineStorage ()
        self.known_faces_dir = offlineStorage.getOfflinePhotoStorageLocation('knownFaces')  
        self.unknown_faces_dir = offlineStorage.getOfflinePhotoStorageLocation('unknownFaces')  
        self.tolerance = 0.6
        self.frame_thickness = 3
        self.font_thickness = 2
        self.model = 'cnn'
        self.video = cv2.VideoCapture(0)
        self.known_names = []
        self.known_faces = []
        self.known_face_encodings = [] 
        self.locations = []
        self.encodings = []
        self.face_names = []
        self.process_this_frame = 0
        
        self.loadImages ()

    def nameToColor (self, name):
        """
        Get color by name. Take 3 first letters, tolower(). Lowercased character ord() value rage is 97 to 122, 
        substract 97, multiply by 8.

        Parameters
        ----------
        name : str
            name of known face

        Returns
        -------
        color : str
            color based on the name of known person
        """
        color = [(ord(c.lower()) - 97) * 8 for c in name[:3]]
        return color
    
    def faceRecognitionFromPhoto (self):
        """
        Perform facial recognition from photos
        """
        print('Loading known faces...')
        # We oranize known faces as subfolders of known_faces_dir
        # Each subfolder's name becomes our label (name)
        # Next we load every file of faces of known person
        for file in os.listdir(self.known_faces_dir):
            # print(file)
            # Load an image
            self.known_names.append(file.replace(".jpg", ""))
            file = os.path.join(self.known_faces_dir + "/", file)
            image = face_recognition.load_image_file(file)

            # Get 128-dimension face encoding
            # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
            encoding = face_recognition.face_encodings(image)[0]
            # Append encodings
            self.known_faces.append(encoding)

        print('Processing unknown faces...')
        # Now let's loop over a folder of faces we want to label
        for file in os.listdir(self.unknown_faces_dir):

            # Load image
            print(f'file {file}', end='')
            image = face_recognition.load_image_file(f'{self.unknown_faces_dir}/{file}')

            # This time we first grab face locations - we'll need them to draw boxes
            locations = face_recognition.face_locations(image, model=self.model)

            # Now since we know loctions, we can pass them to face_encodings as second argument
            # Without that it will search for faces once again slowing down whole process
            encodings = face_recognition.face_encodings(image, locations)

            # We passed our image through face_locations and face_encodings, so we can modify it
            # First we need to convert it from RGB to BGR as we are going to work with cv2
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # But this time we assume that there might be more faces in an image - we can find faces of dirrerent people
            print(f', found {len(encodings)} face(s)')
            for face_encoding, face_location in zip(encodings, locations):

                # We use compare_faces (but might use face_distance as well)
                # Returns array of True/False values in order of passed known_faces
                results = face_recognition.compare_faces(self.known_faces, face_encoding, self.tolerance)

                # Since order is being preserved, we check if any face was found then grab index
                # then label (name) of first matching known face withing a tolerance
                match = None
                if True in results:  # If at least one is true, get a name of first of found labels
                    match = self.known_names[results.index(True)]
                    print(f' - {match} from {results}')

                    # Each location contains positions in order: top, right, bottom, left
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])

                    # Get color by name using our fancy function
                    color = self.nameToColor(match)

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, self.frame_thickness)

                    # Now we need smaller, filled grame below for a name
                    # This time we use bottom in both corners - to start from bottom and move 50 pixels down
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

                    # Wite a name
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), self.font_thickness)

            # Show image
            cv2.imshow(file, image)
            cv2.waitKey(0)
            cv2.destroyWindow(file)

    def loadImages (self):
        """
        Add images fron known faces folder to the known names and known faces lists
        """
        #Loop to add images in friends folder
        for file in os.listdir(self.known_faces_dir):
            try:
                #Extracting person name from the image file eg: david.jpg
                self.known_names.append(file.replace(".jpg", ""))
                file=os.path.join(self.known_faces_dir + "/", file)
                self.known_faces = face_recognition.load_image_file(file)
                #print(face_recognition.face_encodings(known_faces)[0])
                self.known_face_encodings.append(face_recognition.face_encodings(self.known_faces)[0])
                #print(known_face_encodings)

            except Exception as e:
                pass

    def getFrame (self, processEvery=5):
        """
        Compute facial recognition on image frame. Draw box around target face and label the face. 

        Returns
        -------
        jpeg.tobytes() : bytestring
            images memory buffer
        image : img
            compressed image
        unknownPhotoName : str
            label of unknown person face
        """

        success, image = self.video.read()
        unknownPhotoName = None
        #self.process_this_frame = True
        
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Only process every other frame of video to save time
        if self.process_this_frame % processEvery == 0:
            # Find all the faces and face encodings in the current frame of video
            self.locations = face_recognition.face_locations(rgb_small_frame)
            self.encodings = face_recognition.face_encodings(rgb_small_frame, self.locations)

            global name_gui;
            #face_names = []
            i = 0
            for face_encoding in self.encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)
                name = "Unknown"
                
                #print(face_encoding)
                print(matches)

                if len(matches) >0:
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]

                print(name)
                # This is how I SAVE face profiles from unknown people
                # This is where the logic for notification should be inserted I believe
                
                if name == "Unknown":
                    unknownPhotoName = '{dst}/{index}.jpg'.format(dst = self.unknown_faces_dir, index = i)
                    cv2.imwrite(unknownPhotoName, image)
                    print('Saved {}'.format(unknownPhotoName))
                    i += 1
                    
                #print(face_locations)
                self.face_names.append(name)
        
                name_gui = name

        self.process_this_frame += 1 #not self.process_this_frame
            
        # Display the results
        for (top, right, bottom, left), name in zip(self.locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (255, 255, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name_gui, (left + 10, bottom - 10), font, 1.0, (0, 0, 0), 1)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(), image, unknownPhotoName

    def faceRecognitionFromVideo (self):
        """
        Compute facial recognition from video.
        """
        try:
            while True:
                ret, frame, unknownPhotoName = self.getFrame ()
                # Display the resulting image
                cv2.imshow('video', frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            pass
        finally:
            # Release handle to the webcam
            self.video.release()
            cv2.destroyAllWindows()

    def faceRecognitionFromVideoFile(self, fileLocation):
        self.video = cv2.VideoCapture(fileLocation)

        try:
            while self.video.isOpened():
                ret, frame, unknownPhotoName = self.getFrame ()
                # Display the resulting image
                cv2.imshow('video', frame)

                # Hit 'q' on the keyboard to quit!
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except KeyboardInterrupt:
            pass
        finally:
            # Release handle to the webcam
            self.video.release()
            cv2.destroyAllWindows()

    def checkSamePerson(self, photoOneLocation, photoTwoLocation):
        """

            This method checks if the same person appears in two photos

        """

        result = False

        imageOne = face_recognition.load_image_file(photoOneLocation)
        imageTwo = face_recognition.load_image_file(photoTwoLocation)

        oneEncording = face_recognition.face_encodings(imageOne)
        twoEncording = face_recognition.face_encodings(imageTwo)

        if(len(oneEncording)>0 and len(twoEncording)> 0):
            oneEncording = oneEncording[0]
            twoEncording = twoEncording[0]
            results = face_recognition.compare_faces([oneEncording], twoEncording)

            result = True in results

        return result

