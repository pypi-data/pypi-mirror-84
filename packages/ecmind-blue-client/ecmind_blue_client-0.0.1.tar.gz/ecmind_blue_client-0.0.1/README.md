# ECMind blue client

A client wrapper for blue.

## Installation

`pip install ecmind_blue_client`

## Usage

The workflow consists roughly of the following:

- Create a new Client() connection using a client implementation. 
    - Currently there is only one client implementation available: SoapClient()
- Create a new Job() with a job name and provide/add job input parameters and optional job input file parameters
- Execute the Job() with the Client() instance and consume the result 
   - result.result_code returns the blue result code
   - result.values is a dict of output parameters
   - result.files is a list of output file parameters

```
>>> client = Client(SoapClient(self.endpoint, 'TestApp', 'root', 'optimal'))
>>> test_job = Job('krn.GetServerInfo', Flags=0, Info=6)
>>> result = client.execute(test_job)
>>> print(result.values['Value'])
oxtrodbc.dll
```