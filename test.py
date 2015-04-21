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
        test_results = []
        for test_name, test_class in tests:
            print('Running test: %s' % test_name)
            try:
                result = test_class.run()
            except:
                result = False
            if result:
                print('Test PASSED!')
            else:
                print('Test FAILED!')
            test_results.append((test_name, result))
    print("P:F = %d:%d" % (len(filter(lambda x: x[1], test_results)),
                           len(filter(lambda x: not x[1], test_results))))
    print('yay!')
