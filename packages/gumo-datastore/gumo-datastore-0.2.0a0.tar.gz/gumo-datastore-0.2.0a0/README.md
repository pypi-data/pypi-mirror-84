# gumo-datastore

[![CircleCI](https://circleci.com/gh/gumo-py/gumo-datastore.svg?style=svg)](https://circleci.com/gh/gumo-py/gumo-datastore)

## Configuration

```python
from gumo.core import configure as core_configure
from gumo.datastore import configure as datastore_configure

core_configure(
    google_cloud_project='<Google Cloud Platform Project Name>',
    google_cloud_location='<Project Main Location (Region)>',
)

datastore_configure(
    use_local_emulator=True,
    emulator_host='datastore_emulator:8081',
    namespace=None,
)
```

If you need to load environment variables of app.yaml:

```python
import os
import flask
from gumo.core import MockAppEngineEnvironment
# from gumo.core import configure as core_configure
# from gumo.datastore import configure as datastore_configure


# The call to MockAppEngineEnvironment must precede any other initialization code.
if __name__ == '__main__':
    app_yaml_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'app.yaml'
    )
    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml_path)

# core_configure(...)
# datastore_configure(...)

# Application Configurations ...
app = flask.Flask(__name__)

# TODO: Add a sample of Repository implementation using DatastoreRepositoryMixin.

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

## Setup Development Environment

```sh
$ git clone https://github.com/gumo-py/gumo-core.git
$ cd gumo-core

$ make setup
```

## Build and Test

```sh
$ make build

$ make test
```
