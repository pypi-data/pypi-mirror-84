import os
import tempfile
from typing import Type, Optional

class ResultFile:
    def __init__(self, file_parameter:Type):
        """Create a new ResultFile() object.

        Keyword arguments:
        file_parameter -- The SoapClient()s native fileParameter object.
        """        
        self.name = file_parameter.fileName
        self.extension = os.path.splitext(file_parameter.fileName)[1]
        self.bytes = file_parameter.content.attachment

    def size(self):
        """Return the file size of the ResultFile.
        """        
        return self.bytes.__sizeof__()

    def store(self, path:Optional[str]=None) -> str:
        """Store the ResultFile to disk and return the storage path.

        Keyword arguments:
        path -- (Optional) String with target path. When omitted, the file will be saved at a temporary directory.
        """                
        if path == None:
            path = tempfile.gettempdir() + os.path.sep + self.name
        with open(path, 'wb') as file:
            file.write(self.bytes)
            file.close()
        return path