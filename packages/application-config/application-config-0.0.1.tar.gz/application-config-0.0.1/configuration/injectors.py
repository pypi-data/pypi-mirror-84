from functools import wraps

from configuration import ConfigurationLoader


def inject_app_config(func):
    config = ConfigurationLoader()

    @wraps(func)
    def wrapper(*args, **kwargs):
        func.__globals__['APP_CONFIG'] = config.app_config
        return func(*args, **kwargs)
    return wrapper


class WithAppConfig:
    def __init__(self, source):
        self.source = source
        self._config = ConfigurationLoader()

    def __call__(self, *args, **kwargs):
        setattr(self.source, 'APP_CONFIG', self._config.app_config)
        return self.source(*args, **kwargs)
