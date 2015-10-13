from unittest import TestCase
from pyvagrantconfig import PY_VERSION

__author__ = 'drews'


class TestVagrantCase(TestCase):
    def assertHasAttr(self, object, attribute):
        if not hasattr(object, attribute):
            raise AssertionError("'{0}' does not have attribute '{1}'".format(object, attribute))

    def assertKeyInDict(self, key, dictionary):
        if key not in dictionary:
            raise AssertionError("'{0}' does not have key '{1}'".format(dictionary, key))

    if PY_VERSION == (2, 6):

        def assertIsInstance(self, obj, cls):
            """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
            default message."""
            if not isinstance(obj, cls):
                raise AssertionError('{0} is not an instance of {1}'.format(obj, cls))

        def assertGreater(self, a, b):
            """Just like self.assertTrue(a > b), but with a nicer default message."""
            if not a > b:
                raise AssertionError('{0} not greater than {1}'.format(a, b))

        def assertTupleEqual(self, tuple1, tuple2):
            """A tuple-specific equality assertion.

            Args:
                tuple1: The first tuple to compare.
                tuple2: The second tuple to compare.
                msg: Optional message to use on failure instead of a list of
                        differences.
            """
            if tuple1 != tuple2:
                raise AssertionError('{0} not equal to {1}'.format(tuple1, tuple2))

