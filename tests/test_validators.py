import sys
import os
import shutil
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.employee import Employee, Manager, EmployeeDirectory


class TestEmployee(unittest.TestCase):
    def test_new_employee_has_default_role_title(self):
        employee = Employee("bob@company.com", "Bob", "Engineering", 50000)
        self.assertEqual(employee.role_title, "Staff")

    def test_salary_get_and_set(self):
        employee = Employee("bob@company.com", "Bob", "Engineering", 50000)
        self.assertEqual(employee.get_salary(), 50000)

        employee.set_salary(60000)
        self.assertEqual(employee.get_salary(), 60000)

    def test_salary_cannot_go_negative(self):
        employee = Employee("bob@company.com", "Bob", "Engineering", 50000)
        employee.set_salary(-10)
        self.assertEqual(employee.get_salary(), 50000)  # unchanged

    def test_log_work_and_total_hours(self):
        employee = Employee("bob@company.com", "Bob", "Engineering", 50000)
        employee.log_work("2026-09-10", 8)
        employee.log_work("2026-09-11", 6)

        self.assertEqual(employee.total_hours(), 14)
        self.assertEqual(employee.work_log, [("2026-09-10", 8), ("2026-09-11", 6)])

    def test_add_conduct_note(self):
        employee = Employee("bob@company.com", "Bob", "Engineering", 50000)
        employee.add_conduct_note("Ada", "Great teamwork")

        self.assertEqual(employee.conduct_notes, [("Ada", "Great teamwork")])


class TestManager(unittest.TestCase):
    def test_manager_is_an_employee(self):
        manager = Manager("ada@company.com", "Ada", "Engineering", 70000)
        self.assertIsInstance(manager, Employee)

    def test_manager_default_role_title(self):
        manager = Manager("ada@company.com", "Ada", "Engineering", 70000)
        self.assertEqual(manager.role_title, "Manager")

    def test_manager_inherits_employee_behaviour(self):
        manager = Manager("ada@company.com", "Ada", "Engineering", 70000)
        manager.log_work("2026-09-11", 8)
        self.assertEqual(manager.total_hours(), 8)


class TestEmployeeDirectory(unittest.TestCase):
    def setUp(self):
        # each test gets its own throwaway folder, and the json file inside
        # it doesn't exist yet - that's what a fresh install looks like
        self.temp_dir = tempfile.mkdtemp()
        self.directory = EmployeeDirectory(os.path.join(self.temp_dir, "employees.json"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_add_and_get_all(self):
        self.directory.add_employee(Employee("bob@company.com", "Bob", "Engineering", 50000))
        self.directory.add_employee(Manager("ada@company.com", "Ada", "Engineering", 70000))

        employees = self.directory.get_all()
        self.assertEqual(len(employees), 2)

    def test_find_by_id(self):
        self.directory.add_employee(Employee("bob@company.com", "Bob", "Engineering", 50000))

        found = self.directory.find_by_id("bob@company.com")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Bob")

        not_found = self.directory.find_by_id("nobody@company.com")
        self.assertIsNone(not_found)

    def test_get_by_department(self):
        self.directory.add_employee(Employee("bob@company.com", "Bob", "Engineering", 50000))
        self.directory.add_employee(Employee("cara@company.com", "Cara", "Sales", 45000))

        engineering = self.directory.get_by_department("Engineering")
        self.assertEqual(len(engineering), 1)
        self.assertEqual(engineering[0].name, "Bob")

    def test_update_employee(self):
        self.directory.add_employee(Employee("bob@company.com", "Bob", "Engineering", 50000))

        employee = self.directory.find_by_id("bob@company.com")
        employee.set_salary(55000)
        self.directory.update_employee(employee)

        updated = self.directory.find_by_id("bob@company.com")
        self.assertEqual(updated.get_salary(), 55000)

    def test_remove_employee(self):
        self.directory.add_employee(Employee("bob@company.com", "Bob", "Engineering", 50000))
        self.directory.remove_employee("bob@company.com")

        self.assertIsNone(self.directory.find_by_id("bob@company.com"))

    def test_manager_type_survives_save_and_load(self):
        self.directory.add_employee(Manager("ada@company.com", "Ada", "Engineering", 70000))

        found = self.directory.find_by_id("ada@company.com")
        self.assertIsInstance(found, Manager)


if __name__ == "__main__":
    unittest.main()