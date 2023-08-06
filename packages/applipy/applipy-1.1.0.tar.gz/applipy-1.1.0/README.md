[![pipeline status](https://gitlab.com/applipy/applipy/badges/master/pipeline.svg)](https://gitlab.com/applipy/applipy/-/pipelines?scope=branches&ref=master)
[![coverage report](https://gitlab.com/applipy/applipy/badges/master/coverage.svg)](https://gitlab.com/applipy/applipy/-/graphs/master/charts)
[![PyPI Status](https://img.shields.io/pypi/status/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI Version](https://img.shields.io/pypi/v/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI Python](https://img.shields.io/pypi/pyversions/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI License](https://img.shields.io/pypi/l/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI Format](https://img.shields.io/pypi/format/applipy.svg)](https://pypi.org/project/applipy/)

# Applipy

    pip install applipy

Applipy lets you:
 - implement self-contained or interdependant [`Module`s](#modules) that you
   can tell applipy to load for the application through the config file
 - implement [`AppHandle`s](#apphandle): instances that implement application
   lifecycle methods
 - modules can register multiple `AppHandle`s that will be run concurrently
 - load your application from a configuration file
 - you can have multiple configuration file (i.e. one per environment: local,
   dev, prod, staging, etc.)
 - tell applipy which environment to load through an environment variable
   `APPLIPY_ENV`
 - applipy will gracefully manage the lifecycle of your application
 - define [protocol
   handlers](https://gitlab.com/applipy/applipy/-/blob/master/docs/config.md#config-protocols)
   for a given URI scheme in configuration values. With these you can implement
   [secrets](https://gitlab.com/applipy/applipy/-/blob/master/docs/config.md#applipyconfigprotocolsdockersecrets)
   that can be accessed by the application through the configuration.

## Usage

An application can be defined by using a JSON (or YAML, if `pyyaml` is
installed).

```yaml
# dev.yaml
app:
  name: demo
  modules:
    - applipy_http.HttpModule
    - applipy_prometheus.PrometheusModule

logging.level: DEBUG

http:
  host: 0.0.0.0
  port: 8080
```

Save a file `dev.yaml` with the contents in the snipet above and run the
following commands:
```
$ pip install pyyaml applipy applipy_http applipy_prometheus
$ python -m applipy
```

The configuration file above defines an application named `demo` that installs
the applipy web module and the Prometheus module.

You can try it by going to [http://localhost:8080](http://localhost:8080). To
see some metrics you have to call at least twice on the
http://0.0.0.0:8080/metrics endpoint.

Applipy will search for a configuration file named
`${APPLIPY_CONFIG_PATH}/${APPLIPY_ENV}.json` (and
`${APPLIPY_CONFIG_PATH}/${APPLIPY_ENV}.yaml`, if `pyyaml` is installed). The
default values are: `APPLIPY_ENV=dev` and `APPLIPY_CONFIG_PATH=.`

## AppHandle

AppHandle is the interface through wich applipy manages the lifecycle of the
application. An AppHandle implementation looks like this:

```python
# demo_app.py

from applipy import AppHandle


class MyDemoApp(AppHandle):

    async def on_init(self):
        print('initialize resources')

    async def on_start(self):
        print('run long lived application here')
        while True:
            await sleep(3600)

    async def on_shutdown(self):
        print('close and release resources')
```

As you can see above there is three methods exposed by AppHandles that let
applipy run your application.

Applipy is capable of running multiple concurrent AppHandles concurrently,
taking advantage of async in python.

Simplifying a lot, applipy will run your AppHandles like this:

```python
try:
    await all_app_handles.on_init()
    await all_app_handles.on_start()
finally:
    await allapp_handles.on_shutdown()
```

Generally, AppHandle implementations are added to the applipy application by
including the modules they are part of and registering the AppHandle in the
module `configure()` function.

## Modules

In applipy, modules are the building blocks of an application. They allow to
bind instances/classes/providers to types by exposing the an
[`applipy_inject.Injector`](https://gitlab.com/applipy/applipy_inject)'s
`bind()` function, register application handles by exposing the Application's
`register()` function and define dependencies across modules.

An example of a module implementation looks like this:
```python
# mymodule.py

from applipy import Config, Module, LoggingModule
from logging import Logger
from demo_app import MyDemoApp


class MyModule(Module):

    def __init__(self, config: Config):
        self._config = config

    def configure(self, bind, register):
        bind(str, 'ModuleDemo')
        register(MyDemoApp)

    @classmethod
    def depends_on(cls):
        return (LoggingModule,)
```

The way you add modules to an application is through the configuration file by
defining a list of fully qualified names of Module implementations with
the key `app.modules`:

```yaml
app:
  modules:
    - applipy_http.HttpModule
    - applipy_prometheus.PrometheusModule
    - mymodule.MyModule
```

Modules can only receive one parameter in their constructor and it is a
`Config` instance, as shown in the code above. If your module does not need
access to the configuration, you can just not implement a `__init__` or have it
not have arguments (other than `self`).

The `configure()` method is run by the applipy `Application` when it is started
and its purpose is to allow for binding types and registering application
handles. Check the extended `Module` documentation in
[`/docs/module.md`](https://gitlab.com/applipy/applipy/-/blob/master/docs/module.md).

Finally, the `depends_on()` class method returns a tuple of the module types the
module depends on. In the example above, because the application handle
registered by the module requires a `logging.Logger`, the module declares a dependency
with the `LoggingModule` because we know that it binds the `logging.Logger` type.

## More

For a deeper dive on the features and details feel free to check the
[`/docs`](https://gitlab.com/applipy/applipy/-/blob/master/docs/README.md)
subdirectory and the code itself!
