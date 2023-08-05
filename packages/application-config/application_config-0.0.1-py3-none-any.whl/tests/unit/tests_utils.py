import unittest

from configuration import ConfigurationLoader


class TestUtils(unittest.TestCase):
    def test_flatten_is_equal_for_json_and_yaml(self):
        flat_json = ConfigurationLoader('tests/resources/test.json').app_config
        flat_yaml = ConfigurationLoader('tests/resources/application.yaml').app_config

        self.assertEqual(flat_json, flat_yaml)


if __name__ == '__main__':
    unittest.main()
