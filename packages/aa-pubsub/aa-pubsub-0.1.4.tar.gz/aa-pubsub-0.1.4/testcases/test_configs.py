from pubsub import configs
import unittest
import os
import sys
import logging


class ConfigsTest(unittest.TestCase):
    def setUp(self):
        # use ROBOT_CONFIGS
        _root = sys.path[0]
        logging.debug('run in root: {}'.format(_root))
        os.environ.setdefault(configs.ROBOT_CONFIGS_PATH,os.path.join(_root, 'config')),
        _configs = configs.Configs()
        self.configs = _configs
        self.root = _root

    def testFileNotExist(self):
        _file = os.path.join(self.root, 'config', 'notexist.yaml')
        try:
            config = configs.Configs(_file)
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(e.message, configs.INVALID_CONFIG.format(_file))
    
    def testEmptyFile(self):
        _file = os.path.join(self.root, 'config', 'empty.yaml')
        try:
            _configs = configs.Configs(_file)
            self.assertEqual('a empty file', _file)
        except Exception as e:
            self.assertEqual(e.message, configs.CANNOT_LOAD.format(_file))

    def testCustomFile(self):
        _file = os.path.join(self.root, 'config', 'custom.yaml')
        try:
            _configs = configs.Configs(_file)
            # self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)
    
    def testInvalidModel(self):
        _model = 'nomodel'
        try:
            val = self.configs.get_config(_model)
        except Exception as e:
            self.assertEqual(e.message, configs.INVALID_MODEL.format(_model))

    def testModelisNone(self):
        _model = None
        try:
            val = self.configs.get_config(_model)
        except Exception as e:
            self.assertEqual(e.message, configs.INVALID_MODEL.format(_model))

    def testParamisNone(self):
        _model = 'test'
        _param = None
        # test:
        #     type: "test"
        val = self.configs.get_config(_model, _param)
        self.assertDictEqual(val, {'type': 'test'})

    def testInvalidParam(self):
        _model = 'test'
        _param = 'None'
        # test:
        #     type: "test"
        try:
            val = self.configs.get_config(_model, _param)
            self.assertDictEqual(val, {'type': 'test'})
        except Exception as e:
            self.assertEqual(e.message, configs.INVALID_PARAM.format(_model, _model, _param))
