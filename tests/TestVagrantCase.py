from unittest import TestCase

__author__ = 'drews'

class TestVagrantCase(TestCase):

    def assertHasAttr(self, object, attribute):
        if not hasattr(object, attribute):
            raise AssertionError("'{}' does not have attribute '{}'".format(object, attribute))


    def assertKeyInDict(self, key, dictionary):
        if key not in dictionary:
            raise AssertionError("'{}' does not have key '{}'".format(dictionary, key))