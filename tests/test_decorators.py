import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.decorators import login_required, employer_required, manager_required


class FakeUser:
  def __init__(self, role):
    self.role = role


class FakeApp:
  """A stand-in for EmployeeManagementCLI, just enough to test the decorators."""

  def __init__(self, current_user=None):
    self.current_user = current_user

  @login_required
  def do_login_only_thing(self):
    return "done"

  @employer_required
  def do_employer_thing(self):
    return "done"

  @manager_required
  def do_manager_thing(self):
    return "done"


class TestDecorators(unittest.TestCase):
  def test_login_required_blocks_when_logged_out(self):
    app = FakeApp(current_user=None)
    self.assertIsNone(app.do_login_only_thing())

  def test_login_required_allows_when_logged_in(self):
    app = FakeApp(current_user=FakeUser("employee"))
    self.assertEqual(app.do_login_only_thing(), "done")

  def test_employer_required_blocks_non_employer(self):
    app = FakeApp(current_user=FakeUser("manager"))
    self.assertIsNone(app.do_employer_thing())

  def test_employer_required_allows_employer(self):
    app = FakeApp(current_user=FakeUser("employer"))
    self.assertEqual(app.do_employer_thing(), "done")

  def test_manager_required_blocks_employer(self):
    app = FakeApp(current_user=FakeUser("employer"))
    self.assertIsNone(app.do_manager_thing())

  def test_manager_required_allows_manager(self):
    app = FakeApp(current_user=FakeUser("manager"))
    self.assertEqual(app.do_manager_thing(), "done")


if __name__ == "__main__":
  unittest.main()