import collections
import json
import os
import pathlib

import yaml


def _flatten(d, parent_key=''):
    items = []

    for k, v in d.items():
        new_key = parent_key + '_' + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(_flatten(v, new_key).items())
        else:
            items.append((new_key, v))

    return dict(items)


class ConfigurationLoader:
    def __init__(self, file='application.yaml'):
        self._file = file
        self._app_config = None

    @property
    def file(self):
        return self._file

    @file.getter
    def file(self):
        if 'APPLICATION_CONFIG' in os.environ:
            parent_dir = pathlib.Path.cwd()
            self.file = parent_dir / os.environ['APPLICATION_CONFIG']
        return self._file

    @file.setter
    def file(self, new_file):
        if str(new_file).endswith('.json') or str(new_file).endswith('.yaml') or str(new_file).endswith('.yml'):
            parent_dir = pathlib.Path.cwd()
            self._file = parent_dir / new_file
        else:
            raise AttributeError

    @property
    def app_config(self):
        return self._app_config

    @app_config.getter
    def app_config(self):
        return self._load()

    @app_config.setter
    def app_config(self, other_config):
        self._app_config = other_config

    def _is_json(self):
        return str(self.file).endswith('.json')

    def _load_yaml_config(self):
        with open(self.file, 'r') as file:
            application_config = yaml.load(file, Loader=yaml.SafeLoader)
        config_vars = _flatten(application_config)

        return config_vars

    def _load_json_config(self):
        with open(self.file, 'r') as file:
            application_config = json.load(file)
        config_vars = _flatten(application_config)

        return config_vars

    def _load(self):
        if self._is_json():
            config_vars = self._load_json_config()
        else:
            config_vars = self._load_yaml_config()

        for value in config_vars.keys():
            if value in os.environ:
                config_vars[value] = os.environ[value]

        return config_vars
