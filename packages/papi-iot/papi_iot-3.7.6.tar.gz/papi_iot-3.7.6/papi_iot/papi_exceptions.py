class BlobNotFound(Exception):
    """

        Exception raised when a file is not found in the google storage bucket

        Attributes
            fileName -- name of file not located
    """

    def __init__(self, fileName):
        self.message = fileName + ' Not found in storage bucket'

        super().__init__(self.message)

class MultipleBlobsFound(Exception):
    """
        Exception raised when multiple files are not found in the google storage bucket

        Attributes
            fileNames -- array containing missed files

    """

    def __init__(self, fileNames):
        self.message = ", ".join(fileNames) + ' Not found in storage bucket'

        super().__init__(self.message)

class NoBlobsFound(Exception):
    """

        Exception raised when no files are found in the google storage bucket
        
    """

    def __init__(self):
        self.message = "No files found in storage bucket"

        super().__init__(self.message)

class DirectoryCreationFail(Exception):
    """
        Exception raised when folder creation failed

    """

    def __init__(self, dir):
        self.message = "Directory '{}' can not be created".format(dir)

        super().__init__(self.message)