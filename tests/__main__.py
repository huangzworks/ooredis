#! /usr/bin/env python2.7
# coding: utf-8

import unittest

# client

from test_client import TestClient
from test_type_case import TestTypeCase

# mix 
from mix.key.test_key import TestKey

from mix.dict.test_dict import TestDict
from mix.dict.test_type_case_dict import TestTypeCaseDict

from mix.list.test_list import TestList
from mix.list.test_type_case_list import TestTypeCaseList

from mix.set.test_set import TestSet
from mix.set.test_type_case_set import TestTypeCaseSet

from mix.sorted_set.test_sorted_set import TestSortedSet
from mix.sorted_set.test_type_case_sorted_set import TestTypeCaseSortedSet

from mix.single_value.test_single_value import TestSingleValue
from mix.single_value.test_counter import TestCounter
from mix.single_value.test_type_case_single_value import TestTypeCaseSingleValue

# server

from test_server import TestServer

def all_tests():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestClient))
    suite.addTest(unittest.makeSuite(TestTypeCase))

    suite.addTest(unittest.makeSuite(TestKey))

    suite.addTest(unittest.makeSuite(TestDict))
    suite.addTest(unittest.makeSuite(TestTypeCaseDict))

    suite.addTest(unittest.makeSuite(TestList))
    suite.addTest(unittest.makeSuite(TestTypeCaseList))

    suite.addTest(unittest.makeSuite(TestSet))
    suite.addTest(unittest.makeSuite(TestTypeCaseSet))

    suite.addTest(unittest.makeSuite(TestSortedSet))
    suite.addTest(unittest.makeSuite(TestTypeCaseSortedSet))

    suite.addTest(unittest.makeSuite(TestSingleValue))
    suite.addTest(unittest.makeSuite(TestCounter))
    suite.addTest(unittest.makeSuite(TestTypeCaseSingleValue))

    suite.addTest(unittest.makeSuite(TestServer))

    return suite

def run_test():
    tests = all_tests()
    result = unittest.TextTestRunner().run(tests)

if __name__ == "__main__":
    run_test()
