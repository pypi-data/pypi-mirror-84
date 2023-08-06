#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import sys


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo-shared{0}tests{0}pattoo_shared_'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from pattoo_shared import data
from pattoo_shared.constants import (
    DATA_INT, DATA_FLOAT, DATA_COUNT64, DATA_COUNT64)
from tests.libraries.configuration import UnittestConfig


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_hashstring(self):
        """Testing function hashstring."""
        # Test
        value = 'unittest'

        # sha256
        result = data.hashstring(value)
        expected = '''\
df08227309c92f2f3f030b423009e697445371283d89352a26d064d39fb73c36'''
        self.assertEqual(result, expected)
        result = data.hashstring(value, sha=256)
        self.assertEqual(result, expected)

        # sha1
        result = data.hashstring(value, sha=1)
        expected = '''\
94e060874450b5ea724bb6ce5ca7be4f6a73416b'''
        self.assertEqual(result, expected)

        # sha1 UTF8
        result = data.hashstring(value, sha=1, utf8=True)
        expected = b'94e060874450b5ea724bb6ce5ca7be4f6a73416b'
        self.assertEqual(result, expected)

        # sha384
        result = data.hashstring(value, sha=384)
        expected = '''\
99ec86e99be2d6a9d9ad4947cb7a3aa43df85667a5a2839aeb3cedf0baa132a852381f94c70bb\
a8576b7df11a2d3b819'''
        self.assertEqual(result, expected)

        # sha512
        result = data.hashstring(value, sha=512)
        expected = '''\
def51cb07699f90b1613d0f4da13574e415323b2fcb98c1f072218a8ba82a44432da79bdf90ebf\
82581d933dc4128e83bda0c9f9f7b8b32e41b8ee8bb16be531'''
        self.assertEqual(result, expected)

    def test_is_numeric(self):
        """Testing function is_numeric."""
        # Test False
        items = [None, True, False, 'False']
        for item in items:
            result = data.is_numeric(item)
            self.assertFalse(result)

        # Test True
        items = [1, 1.1, '1.1']
        for item in items:
            result = data.is_numeric(item)
            self.assertTrue(result)

    def test_is_data_type_numeric(self):
        """Testing function is_data_type_numeric."""
        # Test False
        items = [None, True, False, 'False', 20, 30, 40]
        for item in items:
            result = data.is_data_type_numeric(item)
            self.assertFalse(result)

        # Test True
        items = [
            99, 101, 32, 64, DATA_INT, DATA_FLOAT, DATA_COUNT64, DATA_COUNT64]
        for item in items:
            result = data.is_data_type_numeric(item)
            self.assertTrue(result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
