import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User


class TestUser(unittest.TestCase):
  def test_password_is_hashed_not_stored_plain(self):
    password_hash = User.hash_password("mypassword")
    user = User("Ada", "ada@company.com", password_hash, "employee")

    self.assertNotEqual(user.password_hash, "mypassword")

  def test_check_password_correct_and_incorrect(self):
    password_hash = User.hash_password("mypassword")
    user = User("Ada", "ada@company.com", password_hash, "employee")

    self.assertTrue(user.check_password("mypassword"))
    self.assertFalse(user.check_password("wrongpassword"))

  def test_to_dict_and_from_dict(self):
    password_hash = User.hash_password("mypassword")
    user = User("Ada", "ada@company.com", password_hash, "manager", "ada@company.com")

    rebuilt = User.from_dict(user.to_dict())

    self.assertEqual(rebuilt.name, "Ada")
    self.assertEqual(rebuilt.role, "manager")
    self.assertEqual(rebuilt.employee_id, "ada@company.com")
    self.assertTrue(rebuilt.check_password("mypassword"))


if __name__ == "__main__":
  unittest.main()