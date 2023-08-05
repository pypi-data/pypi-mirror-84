from .result_file import ResultFile
from typing import Type

class Result:
    def __init__(self, native:Type):
        """Create a new Result() object.

        Keyword arguments:
        native -- The SoapClient()s native result object.
        """        
        self.values = { e['name']: e['value'] for e in native.job.parameter }
        self.files = [ResultFile(fp) for fp in native.job.fileParameter]
        self.return_code = native.job.returnCode        