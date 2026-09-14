import sys
import os
import shutil
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import AuthManager


class TestAuthManager(unittest.TestCase):
  def setUp(self):
    # a throwaway folder so tests can't affect each other or real data;
    # the json file inside it doesn't exist until the first save
    self.temp_dir = tempfile.mkdtemp()
    self.auth = AuthManager(os.path.join(self.temp_dir, "users.json"))

  def tearDown(self):
    shutil.rmtree(self.temp_dir)

  def test_register_then_login(self):
    registered = self.auth.register("Ada", "ada@company.com", "mgrpass", "manager")
    self.assertIsNotNone(registered)

    user = self.auth.login("ada@company.com", "mgrpass")
    self.assertIsNotNone(user)
    self.assertEqual(user.name, "Ada")
    self.assertEqual(user.role, "manager")

  def test_login_with_wrong_password_fails(self):
    self.auth.register("Ada", "ada@company.com", "mgrpass", "manager")

    user = self.auth.login("ada@company.com", "wrongpass")
    self.assertIsNone(user)

  def test_login_with_unknown_email_fails(self):
    user = self.auth.login("nobody@company.com", "whatever")
    self.assertIsNone(user)

  def test_cannot_register_same_email_twice(self):
    self.auth.register("Ada", "ada@company.com", "mgrpass", "manager")
    second = self.auth.register("Someone Else", "ada@company.com", "otherpass", "employee")

    self.assertIsNone(second)

  def test_register_rejects_invalid_email(self):
    result = self.auth.register("Ada", "not-an-email", "mgrpass", "manager")
    self.assertIsNone(result)

  def test_delete_user(self):
    self.auth.register("Ada", "ada@company.com", "mgrpass", "manager")
    self.auth.delete_user("ada@company.com")

    self.assertIsNone(self.auth.login("ada@company.com", "mgrpass"))


if __name__ == "__main__":
  unittest.main()