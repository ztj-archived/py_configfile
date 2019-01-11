# -*- coding: utf-8 -*-
# Author: ZhangTianJie

import json
import os.path
import time
import unittest

from configfile import ConfigFile

timestamp1 = time.time()
timestamp2 = False


def callback():
    global timestamp1
    global timestamp2
    if timestamp2 is False:
        timestamp2 = timestamp1
    else:
        timestamp2 = time.time()
    return json.dumps({"timestamp": timestamp2})


class TestConfigFile(unittest.TestCase):
    configfile = None

    def setUp(self):
        # 创建对象
        config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))
        self.configfile = ConfigFile(config_dir)

    def test_is_app_exist(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files', 'config.json'))
        self.assertEqual(self.configfile.is_app_exist('config', 'json'), file_path)
        self.assertEqual(self.configfile.is_app_exist('config', 'None'), False)

    def test_load_app(self):
        self.assertEqual(self.configfile.load_app('config'), {"file": "yaml"})
        self.assertEqual(self.configfile.load_app('None'), None)

    def test_load_out(self):
        file_path = os.path.join(os.path.dirname(__file__), 'files', 'config.yaml')
        self.assertEqual(ConfigFile.load_out(file_path), {"file": "yaml"})
        file_path = os.path.join(os.path.dirname(__file__), 'files', 'config.json')
        self.assertEqual(ConfigFile.load_out(file_path), {"file": "json"})

    def test_load_app_json(self):
        self.assertEqual(self.configfile.load_app_json('config'), {"file": "json"})

    def test_load_dynamic_json(self):
        self.assertEqual(self.configfile.load_dynamic_json('config', callback, 3), {"timestamp": timestamp1})
        time.sleep(1)
        self.assertEqual(self.configfile.load_dynamic_json('config', callback, 3), {"timestamp": timestamp1})
        time.sleep(3)
        self.assertNotEqual(self.configfile.load_dynamic_json('config', callback, 3), {"timestamp": timestamp1})


if __name__ == '__main__':
    unittest.main()
