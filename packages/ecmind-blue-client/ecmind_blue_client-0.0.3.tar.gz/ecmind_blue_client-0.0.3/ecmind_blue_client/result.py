from .result_file import ResultFile
from typing import List

class Result:
    def __init__(self, values:dict, files:List[ResultFile], return_code:int):
        """Create a new Result() object.

        Keyword arguments:
        values -- Dictionary of output parameters.
        files -- List of ResultFile() output file parameters.
        return_code -- Integer representation of the job result.
        """
        self.values = values
        self.files = files
        self.return_code = return_code