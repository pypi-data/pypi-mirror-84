# Dyson-client
Dyson python grpc client implementation

## Dyson client package
Dyson client package contains the client object and all relevant data objects.
Package can be found [here](https://pypi.org/project/dysonclient/)
### Installation
```commandline
pip install dysonclient
```
### Using dyson client 
```python
with DysonClient() as client:
    client.log_event([your_event])
```
### Examples

| Example 	| Read me file           	|
|---------	|------------------------	|
| From JSON file     	| [examples/from_json_file/README.md](examples/from_json_file/README.md) 	|
| Load test     	| [examples/load_test/README.md](examples/load_test/README.md) 	|


### API updates
[log_pb2.py](dysonclient/log_pb2.py) and [log_pb2_grpc.py](dysonclient/log_pb2_grpc.py) are auto generated and should not modified manually.
On any change in [log.proto](https://github.com/smore-inc/dyson/blob/master/src/protos/log.proto) use the following command in order to generate no files ([setuptools](https://pypi.org/project/setuptools/) package is required).
```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. log.proto 
```
