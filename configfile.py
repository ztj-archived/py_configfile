# -*- coding: utf-8 -*-
# Author: ZhangTianJie


import json
import os.path
import time

import yaml


class ConfigFile(object):
    """config file module"""
    config_dir = os.path.abspath('')

    def is_app_exist(self, sign, suffix):
        """check the app configuration file exists"""
        file_path = os.path.join(self.config_dir, '.'.join([sign, suffix]))
        if not os.path.isfile(file_path):
            return False
        else:
            return file_path

    def load_app(self, sign):
        """load app configuration file"""
        if self.is_app_exist(sign, 'yaml'):
            return self.load_app_yaml(sign)
        elif self.is_app_exist(sign, 'json'):
            return self.load_app_json(sign)
        return None

    @staticmethod
    def load_out(file_path):
        """load outside configuration file"""
        suffix = file_path.split('.')[-1]
        method = 'load_out_' + suffix
        if hasattr(ConfigFile, method):
            return getattr(ConfigFile, method)(file_path)
        else:
            return False

    def load_app_json(self, sign):
        """load_ dynamic configuration file"""
        file_path = self.is_app_exist(sign, 'json')
        return self.load_out_json(file_path)

    @staticmethod
    def load_out_json(file_path):
        """load outside configuration json file"""
        if not os.path.isfile(file_path):
            return False
        with open(file_path) as f:
            return json.loads(f.read())

    def load_dynamic_json(self, sign, callback, expires=3600):
        """load dynamic configuration json file"""
        file_path = self.is_app_exist(sign, 'dynamic.json')
        # file does not exist
        if not file_path:
            file_path = os.path.join(self.config_dir, '.'.join([sign, 'dynamic', 'json']))
            with open(file_path, 'w') as f:
                f.write(callback())
        # file expired
        st_m_time = os.stat(file_path).st_mtime
        if time.time() > (st_m_time + expires):
            with open(file_path, 'w') as f:
                f.write(callback())
        # load file
        return self.load_app_json(sign + '.dynamic')

    def load_app_yaml(self, sign):
        """load app configuration yaml file"""
        file_path = self.is_app_exist(sign, 'yaml')
        return self.load_out_yaml(file_path)

    @staticmethod
    def load_out_yaml(file_path):
        """load outside configuration yaml file"""
        if not os.path.isfile(file_path):
            return False
        with open(file_path, 'rb') as f:
            return yaml.load(f.read())