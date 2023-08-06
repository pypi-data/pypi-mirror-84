from time import sleep
from picamera import PiCamera

class PapiCameraVideo:
    
    # Class attributes here testing content
    def __init__ (self): 
        """ 
    
        Initial state of the object by assigning the values of the object properties
        
        """
        
        self.camera = PiCamera()

        self.cameraMode = False
        self.videoMode = False
        
   
    def setCameraMode (self, resolution=(1024, 768)): 
        """ 
        
        Switch the camera to photo mode instead of video
        ---------------------------------------------------------------------
        Variables:
        resolution: default (1024, 768) sets aspect ratio of photo taken
        
        """

        if self.videoMode:
            self.camera.stop_recording()
            self.videoMode = False

        self.camera.resolution = resolution
        self.camera.start_preview()

        #camera warm-up time
        sleep(2)

        self.cameraMode = True
        
    def setLowLightMode (self, alternateISO=False): 
        """
        
        Switch the camera mode to low light mode
        -----------------------------------------------------------------------------
        Variables:
        alternateISO: chooses between two ISO values for Normal light conditions,
                      if true, ISO set to 800 if false, ISO set to 400. The lower ISO
                      means a lower sensitivity to light
        
        """
        
        self.autoAdjustToLight()

        # Set ISO to low light values
        self.camera.iso = 800 if alternateISO else 400 

        # wait for the automatic gain control to settle
        sleep(2)

        # now fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        
        gain = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = gain
    
    def setNormalLightMode (self, alternateISO=False): 
        """
        
        Switch the camera mode to normal light mode
        --------------------------------------------------------------------------------
        Variables:
        alternateISO: chooses between two ISO values for Normal light conditions,
                      if true, ISO set to 200 if false, ISO set to 100. The lower ISO
                      means a lower sensitivity to light
        
        """

        self.autoAdjustToLight()

        # Set ISO to low light values
        self.camera.iso = 200 if alternateISO else 100 

        # wait for the automatic gain control to settle
        sleep(2)

        # now fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        
        gain = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = gain
        
    
    def autoAdjustToLight (self): 
        """
        
        Automatically adjust the camera lighting according to light conditions at the time
        
        """

        self.camera.iso = 0
        self.camera.exposure_mode = 'auto'
        self.shutter_speed = 0
        self.camera.awb_mode = 'auto'
        
        # wait for automatic gain control to settle
        sleep(2)
        
        
    
    def takePhoto (self, name): 
        """ 
        
        Capture the image of face in camera field of view. Note, assumes setCameraMode has been run
        before running this function and all images are saved as jpg
        -------------------------------------------------------------------------------------------
        Variables:
        name: chosen name and path location of photo taken e.g. /path/to/save/to/testImage

        """
        name = name + '.jpg'
        self.camera.capture(name)
        
    
    def recordVideoFor (self, name, length = 60, resolution = (640, 480), videoType='.h264'): 
        """
        
        Capture the footage of face in camera field of view for a limited time
        -----------------------------------------------------------------------------------------------
        Variables:
        name: chosen name and path location of video recorded e.g /path/to/save/to/testVideo
        length: default 60,  seconds of recording you want to record for
        resolution: default (640, 480) aspect ratio of recorded video
        videoType: default .h264 video encording. Supported encording '.h264', '.mjpeg'

        """

        if self.cameraMode:
            self.camera.stop_preview()
            self.cameraMode = False

        self.videoMode = True

        self.camera.start_recording(name + videoType)
        self.camera.wait_recording(length)
        self.camera.stop_recording()

        self.videoMode = False
        
    
    def recordVideo (self, name, resolution = (640, 480), videoType='.h264'): 
        """
        
        Capture the footage of face in camera field of view
        -----------------------------------------------------------------------------------------------
        Variables:
        name: chosen name and path location of video recorded e.g /path/to/save/to/testVideo
        resolution: default (640, 480) aspect ratio of recorded video
        videoType: default .h264 video encording. Supported encording '.h264', '.mjpeg'
        
        """
        
        if self.cameraMode:
            self.camera.stop_preview()
            self.cameraMode = False

        self.videoMode = True

        self.camera.start_recording(name + videoType)
        self.camera.wait_recording()
    
    def stopVideoRecording (self): 
        """
        
        Stop the video recording
        
        """

        if self.videoMode:
            self.videoMode = False
            self.camera.stop_recording()
