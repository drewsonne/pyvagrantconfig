import six
if six.PY2:
    from unittest2 import TestCase
else:
    from unittest import TestCase

__author__ = 'drews'


class TestVagrantCase(TestCase):
    def assertHasAttr(self, object, attribute):
        if not hasattr(object, attribute):
            raise AssertionError("'{0}' does not have attribute '{1}'".format(object, attribute))

    def assertKeyInDict(self, key, dictionary):
        if key not in dictionary:
            raise AssertionError("'{0}' does not have key '{1}'".format(dictionary, key))
    #
    # if PY_VERSION == (2, 6):
    #
    #     def assertIsInstance(self, obj, cls):
    #         """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
    #         default message."""
    #         if not isinstance(obj, cls):
    #             raise AssertionError('{0} is not an instance of {1}'.format(obj, cls))
    #
    #     def assertGreater(self, a, b):
    #         """Just like self.assertTrue(a > b), but with a nicer default message."""
    #         if not a > b:
    #             raise AssertionError('{0} not greater than {1}'.format(a, b))
    #
    #     def assertTupleEqual(self, tuple1, tuple2):
    #         """A tuple-specific equality assertion.
    #
    #         Args:
    #             tuple1: The first tuple to compare.
    #             tuple2: The second tuple to compare.
    #             msg: Optional message to use on failure instead of a list of
    #                     differences.
    #         """
    #         if self._compareList(tuple1, tuple2):
    #             raise AssertionError('{0} not equal to {1}'.format(tuple1, tuple2))
    #
    #
    #     def assertListEqual(self, list1, list2):
    #         if list1 != list2:
    #             raise AssertionError('{0} not equal to {1}'.format(list1, list2))
    #
    #     def assertDictEqual(self, dict1, dict2):
    #         if not self._compareDict(dict1, dict2):
    #             raise AssertionError('{0} not equal to {1}'.format(dict1, dict2))
    #
    #     def _compareDict(self, dict1, dict2):
    #         #1 - Compare keys
    #         keys1 = dict1.keys()
    #         keys2 = dict2.keys()
    #         if not self._cmpSets(keys1, keys2):
    #             return False
    #         #2 - Compare values
    #         for key in keys1:
    #             key_type = type(dict1[key])
    #             if key_type in [dict, list]:
    #                 if (key_type == list) and not self._compareList(dict1[key], dict2[key]):
    #                     return False
    #                 elif (key_type == dict) and not self._compareDict(dict1[key], dict2[key]):
    #                     return False
    #             else:
    #                 if dict1[key] != dict2[key]:
    #                     return False
    #         return True
    #
    #     def _compareList(self, list1, list2):
    #
    #         return set(list1) != set(list2)
    #
    #     def _cmpSets(self, set1, set2):
    #         return set(set1) == set(set2)
    #
    #     def _dictEqual(self, dict1, dict2):
    #         pass
    #
    #     def _listEqual(self, dict1, dict2):
    #         pass