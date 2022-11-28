# `csle-collector`

This library contains scripts and programs for collecting data from the emulation. 

<p align="center">
<img src="docs/data_collection_1.png" width="600">
</p>

[![PyPI version](https://badge.fury.io/py/csle-collector.svg)](https://badge.fury.io/py/csle-collector)
![PyPI - Downloads](https://img.shields.io/pypi/dm/csle-collector)

## Re-generate gRPC files

To re-generate the gRPC files, run: 
```bash
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/client_manager/. ./protos/client_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/kafka_manager/. ./protos/kafka_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/elk_manager/. ./protos/elk_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/docker_stats_manager/. ./protos/docker_stats_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/snort_ids_manager/. ./protos/snort_ids_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/host_manager/. ./protos/host_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/ossec_ids_manager/. ./protos/ossec_ids_manager.proto
python -m grpc_tools.protoc -I./protos/ --python_out=./csle_collector/. --grpc_python_out=./csle_collector/traffic_manager/. ./protos/traffic_manager.proto
```

## Requirements

- Python 3.8+
- `grpcio` (for the collector API)
- `grpcio-tools` (for the collector API)
- `scipy` (for statistical models of client processes)
- `confluent-kafka` (for interacting with Kafka)
- `docker` (for interacting with Docker)

## Development Requirements

- Python 3.8+
- `flake8` (for linting)
- `tox` (for automated testing)
- `pytest` (for unit tests)
- `pytest-cov` (for unit test coverage)
- `mypy` (for static typing)
- `sphinx` (for API documentation)
- `sphinxcontrib-napoleon` (for API documentation)
- `sphinx-rtd-theme` (for API documentation)

## Installation

```bash
# install from pip
pip install csle-collector==<version>
# local install from source
$ pip install -e csle-collector
# force upgrade deps
$ pip install -e csle-collector --upgrade

# git clone and install from source
git clone https://github.com/Limmen/csle
cd csle/simulation-system/libs/csle-collector
pip3 install -e .
```

### Development tools

Install the Python build tool
```bash
pip install -q build
```

Install `twine` for publishing the package to PyPi:
```bash
python3 -m pip install --upgrade twine
```

Install the `flake8` linter:
```bash
python -m pip install flake8
```

Install the mypy for static type checking:
```bash
python3 -m pip install -U mypy
```

Install `pytest` and `mock` for unit tests:
```bash
pip install -U pytest mock pytest-mock pytest-cov
```

Install Sphinx to automatically generate API documentation from docstrings:
```bash
pip install sphinx sphinxcontrib-napoleon sphinx-rtd-theme
```

Install tox for automatically running tests in different python environments:
```bash
pip install tox
```

## API documentation

This section contains instructions for generating API documentation using `sphinx`.

### Latest Documentation

The latest documentation is available at [https://limmen.dev/csle/docs/csle-collector](https://limmen.dev/csle/docs/csle-collector)

### Generate API Documentation

First make sure that the `CSLE_HOME` environment variable is set:
```bash
echo $CSLE_HOME
```
Then generate the documentation with the commands:
```bash
cd docs
sphinx-apidoc -f -o source/ ../csle_collector/
make html
```
To update the official documentation at [https://limmen.dev/csle](https://limmen.dev/csle), copy the generated HTML files to the documentation folder:
```bash
cp -r build/html ../../../../docs/_docs/csle-collector
```

## Static code analysis

To run the Python linter, execute the following command:
```
flake8 .
```

To run the mypy type checker, execute the following command:
```
mypy .
```

## Unit tests

To run the unit tests, execute the following command:
```
pytest
```

To generate a coverage report, execute the following command:
```
pytest --cov=csle_collector
```

## Run tests and code analysis in different python environments

To run tests and code analysis in different python environemnts, execute the following command:

```bash
tox
```

## Create a new release and publish to PyPi

First build the package by executing:
```bash
python3 -m build
```
After running the command above, the built package is available at `./dist`.

Push the built package to PyPi by running:
```bash
python3 -m twine upload dist/*
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar