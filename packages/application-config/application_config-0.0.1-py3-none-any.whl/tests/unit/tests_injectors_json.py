import os
import unittest

import pytest

from configuration.injectors import *
from configuration import ConfigurationLoader


@pytest.fixture(autouse=True)
def setup():
    os.environ['APPLICATION_CONFIG'] = 'tests/resources/application.json'
    yield


@inject_app_config
def json_function_a(a, b, c):
    return APP_CONFIG['key1']


@WithAppConfig
class JsonTestClass:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def a_method(self):
        test_key = self.APP_CONFIG['key1']
        return test_key

    def another_method(self):
        return self.a + self.b


class InjectorsJson(unittest.TestCase):
    def test_json_config_loads(self):
        test = ConfigurationLoader()

        self.assertEqual(test._is_json(), True)

    def test_json_config_injected_into_function_scope(self):
        test = json_function_a(1, 2, 3)

        self.assertEqual(test, 'abc')

    def test_other_fields_not_modified(self):
        test_class = JsonTestClass('a', 'b', 'c')

        self.assertEqual(test_class.a, 'a')
        self.assertEqual(test_class.b, 'b')
        self.assertEqual(test_class.c, 'c')

    def test_config_loaded_correctly(self):
        test_class = JsonTestClass(1, 2, 3)
        config = ConfigurationLoader().app_config

        self.assertEqual(config, test_class.APP_CONFIG)

    def test_config_gets_flattened_correctly(self):
        test_class = JsonTestClass('a', 'b', 'c')
        flat_config = {'key1': 'abc',
                       'key2_key3_key4': 'def',
                       'key2_key5': ['ghi',
                                     'jkl',
                                     'mno'],
                       'key2_key6': ['pqr',
                                     'stu',
                                     {'key7': ['vwx',
                                               'yza',
                                               {'value10': 'bcd'}]},
                                     'efg',
                                     'hij']}

        self.assertEqual(flat_config, test_class.APP_CONFIG)


if __name__ == '__main__':
    unittest.main()
