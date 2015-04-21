#!/usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import print_function
from importlib import import_module
import sys
import os
import glob

if __name__ == '__main__':
    modules = glob.glob(os.path.join(os.path.dirname(__file__), 'test', '*_test.py'))
    for module in modules:
        module_name = module[2:-3].replace('/', '.')
        print('Importing module: %s' % module_name)
        mod = import_module(module_name, '')
        print('Running module: %s' % module_name)
        tests = getattr(mod, 'tests')
        for test_name, test_class in tests:
            print('Running test: %s' % test_name)
            result = test_class.run()
            if result:
                print('Test PASSED!')
            else:
                print('Test FAILED!')
    print('yay!')
