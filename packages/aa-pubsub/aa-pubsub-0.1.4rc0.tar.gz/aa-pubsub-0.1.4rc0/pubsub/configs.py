import logging
import os

import yaml

INVALID_CONFIG = 'invalid config file: {}'
CANNOT_LOAD = 'can not load config fle: {}'
CUSTOM_CONFIG = 'use custom config file: {}'
SYSTEM_CONFIG = 'use system config file: {}'
INVALID_MODEL = 'invalid config model or model is not configured: {}'
INVALID_PARAM = 'invalid param in config model {} or param is not configured in config model {}: {}'

ROBOT_CONFIGS_PATH = 'ROBOT_CONFIGS'
CONFIG_FILES = 'pubsub.yaml'


class Configs():
    def __init__(self, config_file=None):
        if config_file is None:
            logging.debug(SYSTEM_CONFIG.format(config_file))
            config_file = os.path.join(os.getenv(ROBOT_CONFIGS_PATH),
                                       CONFIG_FILES)
        else:
            logging.debug(CUSTOM_CONFIG.format(config_file))

        self.config_file = config_file
        valid, msg = self.check_config_file()
        if not valid:
            raise Exception(msg)
        configs = self.get_configs()
        if configs is None:
            msg = CANNOT_LOAD.format(self.config_file)
            logging.error(msg)
            raise Exception(msg)
        self.configs = configs

    def check_config_file(self):
        msg = ''
        if not os.path.isfile(self.config_file):
            msg = INVALID_CONFIG.format(self.config_file)
            logging.error(msg)
            return False, msg
        return True, msg

    def get_configs(self):
        config = None
        if os.path.isfile(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f.read(), )
        return config

    def get_config(self, model, param=''):
        res = None
        if model is None or model.strip() == '':
            msg = INVALID_MODEL.format(model)
            logging.error(msg)
            raise Exception(msg)
        try:
            config = self.configs[model]
        except KeyError as e:
            msg = INVALID_MODEL.format(model)
            logging.error(msg)
            logging.error(e.message)
            raise Exception(INVALID_MODEL.format(model))
        if param is None or param.strip() == '':
            res = config
        else:
            try:
                res = config[param]
            except KeyError as e:
                msg = INVALID_PARAM.format(model, model, param)
                logging.error(msg)
                logging.error(e.message)
                raise Exception(INVALID_PARAM.format(model, model, param))

        return res
