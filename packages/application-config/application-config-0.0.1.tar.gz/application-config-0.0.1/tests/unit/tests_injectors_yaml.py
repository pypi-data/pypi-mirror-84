import os
import unittest

import pytest

from configuration import ConfigurationLoader
from configuration.injectors import inject_app_config, WithAppConfig


@pytest.fixture(autouse=True)
def setup():
    os.environ['APPLICATION_CONFIG'] = 'tests/resources/application.yaml'
    yield


@inject_app_config
def function_a(a, b, c):
    return APP_CONFIG['key1']


@WithAppConfig
class TestClass:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def a_method(self):
        test_key = self.APP_CONFIG['key1']
        return test_key

    def another_method(self):
        return self.a + self.b


@inject_app_config
def function_b(a, b, c):
    return APP_CONFIG['key1']


@WithAppConfig
class TestClassA:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def a_method(self):
        test_key = self.APP_CONFIG['key1']
        return test_key

    def another_method(self):
        return self.a + self.b


class InjectorsYaml(unittest.TestCase):
    def test_config_injected_into_function_scope(self):
        test = function_a(1, 2, 3)

        self.assertEqual(test, 'value1')

    def test_other_fields_not_modified(self):
        test_class = TestClass('a', 'b', 'c')

        self.assertEqual(test_class.a, 'a')
        self.assertEqual(test_class.b, 'b')
        self.assertEqual(test_class.c, 'c')

    def test_config_loaded_correctly(self):
        test_class = TestClass(1, 2, 3)
        config = ConfigurationLoader().app_config

        self.assertEqual(config, test_class.APP_CONFIG)

    def test_config_gets_flattened_correctly(self):
        test_class = TestClass('a', 'b', 'c')
        flat_config = {'key1': 'value1',
                       'key2_key3_key4': 'value2',
                       'key2_key5': ['value3',
                                     'value4',
                                     'value5'],
                       'key2_key6': ['value6',
                                     'value7',
                                     {'key7': ['value8',
                                               'value9',
                                               {'value10': 'key'}]},
                                     'value11',
                                     'value12']}

        self.assertEqual(flat_config, test_class.APP_CONFIG)


if __name__ == '__main__':
    unittest.main()
