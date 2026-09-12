import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(_file_))))

from utils.validators import not_empty, valid_email


class TestValidators(unittest.TestCase):
    def test_not_empty(self):
        self.assertTrue(not_empty("Ada"))
        self.assertFalse(not_empty(""))
        self.assertFalse(not_empty("   "))

    def test_valid_email(self):
        self.assertTrue(valid_email("ada@company.com"))
        self.assertFalse(valid_email("not-an-email"))
        self.assertFalse(valid_email("ada@companycom"))


if _name_ == "_main_":
    unittest.main()