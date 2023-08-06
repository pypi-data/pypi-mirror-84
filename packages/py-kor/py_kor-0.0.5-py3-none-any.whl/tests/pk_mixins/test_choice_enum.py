import unittest

from py_kor.pk_mixins import *


class ChoiceEnumTestCase(unittest.TestCase):
    def test_operations(self):
        class TestChoiceEnum(ChoiceEnum):
            TEST_1 = 1
            TEST_2 = 2
            TEST_3 = 3

        self.assertEqual(TestChoiceEnum.choices(), ((1, 'TEST_1'), (2, 'TEST_2'), (3, 'TEST_3')))