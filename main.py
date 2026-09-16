import argparse

from colorama import Fore, Style, init as colorama_init

from models.employee import Employee, EmployeeDirectory, Manager
from utils.auth import AuthManager
from utils.decorators import login_required, employer_required, manager_required
from utils.validators import not_empty


def parse_args():
    parser = argparse.ArgumentParser(
        prog="employee-cli",
        description="Employee Database Management System",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored terminal output",
    )

    subparsers = parser.add_subparsers(dest="command")

    p_add = subparsers.add_parser("add", help="Add a new employee")
    p_add.add_argument("--name", required=True, help="Employee full name")
    p_add.add_argument("--email", required=True, help="Login email, used as employee ID")
    p_add.add_argument("--department", required=True, help="Employee's department")
    p_add.add_argument("--salary", type=float, required=True, help="Starting salary")
    p_add.add_argument("--manager", action="store_true", help="Create as a manager")

    p_list = subparsers.add_parser("list", help="List employees")
    p_list.add_argument("--department", help="Only show employees in this department")

    p_fire = subparsers.add_parser("fire", help="Remove an employee")
    p_fire.add_argument("employee_id", help="Email of the employee to remove")

    p_log = subparsers.add_parser("log-hours", help="Log hours worked")
    p_log.add_argument("employee_id", help="Email of the employee logging hours")
    p_log.add_argument("date", help="Date worked, e.g. 2026-09-16")
    p_log.add_argument("hours", type=float, help="Number of hours worked")

    return parser.parse_args()


class EmployeeManagementCLI:
    def __init__(self):
        self.auth = AuthManager()
        self.directory = EmployeeDirectory()
        self.current_user = None

    def run(self):
        print(Fore.CYAN + "EMPLOYEE DATABASE MANAGEMENT SYSTEM" + Style.RESET_ALL)

        while True:
            if self.current_user is None:
                self.guest_menu()
            elif self.current_user.role == "employer":
                self.employer_menu()
            elif self.current_user.role == "manager":
                self.manager_menu()
            else:
                self.employee_menu()

    # ---------- guest ----------

    def guest_menu(self):
        print("\n1. Register as employer")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            user = self.auth.register(name, email, password, role="employer")
            if user:
                self.current_user = user
                print("Employer account created. You are logged in.")

        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            user = self.auth.login(email, password)
            if user:
                self.current_user = user
                print(f"Welcome, {user.name} ({user.role}).")
            else:
                print("Invalid email or password.")

        elif choice == "3":
            print("Goodbye!")
            raise SystemExit

        else:
            print("Invalid option.")

    def logout(self):
        self.current_user = None
        print("Logged out.")

    # ---------- employer ----------

    def employer_menu(self):
        print(f"\nEMPLOYER MENU - {self.current_user.name}")
        print("1. Add employee")
        print("2. Fire employee")
        print("3. View all employees")
        print("4. Change salary")
        print("5. Change manager's department")
        print("6. Assign role to employee")
        print("7. Comment on employee conduct")
        print("8. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.add_employee()
        elif choice == "2":
            self.fire_employee()
        elif choice == "3":
            self.directory_display(self.directory.get_all())
        elif choice == "4":
            self.change_salary()
        elif choice == "5":
            self.change_manager_department()
        elif choice == "6":
            self.assign_role()
        elif choice == "7":
            self.comment_on_conduct()
        elif choice == "8":
            self.logout()
        else:
            print("Invalid option.")

    @employer_required
    def add_employee(self):
        name = input("Name: ")
        email = input("Email (used as login and employee ID): ").strip().lower()
        department = input("Department: ")
        salary = float(input("Starting salary: "))
        password = input("Temporary password: ")
        is_manager = input("Is this a manager? (y/n): ").strip().lower() == "y"

        if not not_empty(name) or not not_empty(department):
            print("Name and department are required.")
            return

        if is_manager:
            employee = Manager(email, name, department, salary)
            role = "manager"
        else:
            employee = Employee(email, name, department, salary)
            role = "employee"

        self.directory.add_employee(employee)
        self.auth.register(name, email, password, role, employee_id=email)
        print("Employee added.")

    def add_employee_args(self, args):
        if not not_empty(args.name) or not not_empty(args.department):
            print("Name and department are required.")
            return

        email = args.email.strip().lower()

        if args.manager:
            employee = Manager(email, args.name, args.department, args.salary)
        else:
            employee = Employee(email, args.name, args.department, args.salary)

        self.directory.add_employee(employee)
        print("Employee added.")

    @employer_required
    def fire_employee(self):
        employee_id = input("Employee ID (email) to remove: ").strip().lower()
        if self.directory.find_by_id(employee_id) is None:
            print("Employee not found.")
            return
        self.directory.remove_employee(employee_id)
        self.auth.delete_user(employee_id)
        print("Employee removed.")

    def fire_employee_args(self, employee_id):
        employee_id = employee_id.strip().lower()
        if self.directory.find_by_id(employee_id) is None:
            print("Employee not found.")
            return
        self.directory.remove_employee(employee_id)
        self.auth.delete_user(employee_id)
        print("Employee removed.")

    @employer_required
    def change_salary(self):
        employee_id = input("Employee ID: ").strip().lower()
        employee = self.directory.find_by_id(employee_id)
        if employee is None:
            print("Employee not found.")
            return
        new_salary = float(input("New salary: "))
        employee.set_salary(new_salary)
        self.directory.update_employee(employee)
        print("Salary updated.")

    @employer_required
    def change_manager_department(self):
        employee_id = input("Manager's employee ID: ").strip().lower()
        employee = self.directory.find_by_id(employee_id)
        if not isinstance(employee, Manager):
            print("That ID does not belong to a manager.")
            return
        employee.department = input("New department: ")
        self.directory.update_employee(employee)
        print("Department updated.")

    # ---------- manager ----------

    def manager_menu(self):
        manager = self.directory.find_by_id(self.current_user.employee_id)
        print(f"\nMANAGER MENU - {self.current_user.name} ({manager.department})")
        print("1. View employees in my department")
        print("2. Assign role to an employee")
        print("3. Comment on an employee's conduct")
        print("4. Log my work hours")
        print("5. View my profile")
        print("6. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.directory_display(self.directory.get_by_department(manager.department))
        elif choice == "2":
            self.assign_role()
        elif choice == "3":
            self.comment_on_conduct()
        elif choice == "4":
            self.log_work()
        elif choice == "5":
            self.view_my_profile()
        elif choice == "6":
            self.logout()
        else:
            print("Invalid option.")

    # shared by employer and manager (with a plain role check inside)
    def assign_role(self):
        if self.current_user.role not in ("employer", "manager"):
            print("You do not have permission to do that.")
            return

        employee_id = input("Employee ID: ").strip().lower()
        employee = self.find_in_scope(employee_id)
        if employee is None:
            return
        employee.role_title = input("New role/title: ")
        self.directory.update_employee(employee)
        print("Role assigned.")

    def comment_on_conduct(self):
        if self.current_user.role not in ("employer", "manager"):
            print("You do not have permission to do that.")
            return

        employee_id = input("Employee ID: ").strip().lower()
        employee = self.find_in_scope(employee_id)
        if employee is None:
            return
        note = input("Conduct note: ")
        employee.add_conduct_note(self.current_user.name, note)
        self.directory.update_employee(employee)
        print("Note added.")

    def find_in_scope(self, employee_id):
        """Employer can reach anyone; a manager only their own department."""
        employee = self.directory.find_by_id(employee_id)
        if employee is None:
            print("Employee not found.")
            return None

        if self.current_user.role == "manager":
            manager = self.directory.find_by_id(self.current_user.employee_id)
            if employee.department.lower() != manager.department.lower():
                print("That employee is outside your department.")
                return None

        return employee

    # ---------- employee ----------

    def employee_menu(self):
        print(f"\nEMPLOYEE MENU - {self.current_user.name}")
        print("1. View my profile")
        print("2. Log my work hours")
        print("3. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.view_my_profile()
        elif choice == "2":
            self.log_work()
        elif choice == "3":
            self.logout()
        else:
            print("Invalid option.")

    @login_required
    def view_my_profile(self):
        employee = self.directory.find_by_id(self.current_user.employee_id)
        print(employee.summary())
        for author, note in employee.conduct_notes:
            print(f"  - {note} (by {author})")

    @login_required
    def log_work(self):
        date = input("Date: ")
        hours = float(input("Hours worked: "))
        employee = self.directory.find_by_id(self.current_user.employee_id)
        employee.log_work(date, hours)
        self.directory.update_employee(employee)
        print("Hours logged.")

    def log_work_args(self, employee_id, date, hours):
        employee_id = employee_id.strip().lower()
        employee = self.directory.find_by_id(employee_id)
        if employee is None:
            print("Employee not found.")
            return
        employee.log_work(date, hours)
        self.directory.update_employee(employee)
        print("Hours logged.")

    def list_employees(self, department=None):
        if department:
            self.directory_display(self.directory.get_by_department(department))
        else:
            self.directory_display(self.directory.get_all())

    @staticmethod
    def directory_display(employees):
        if not employees:
            print("No employees found.")
            return
        for employee in employees:
            print(employee.summary())


if __name__ == "__main__":
    args = parse_args()
    colorama_init(strip=args.no_color)

    app = EmployeeManagementCLI()

    try:
        if args.command is None:
            app.run()
        elif args.command == "add":
            app.add_employee_args(args)
        elif args.command == "list":
            app.list_employees(args.department)
        elif args.command == "fire":
            app.fire_employee_args(args.employee_id)
        elif args.command == "log-hours":
            app.log_work_args(args.employee_id, args.date, args.hours)
    except KeyboardInterrupt:
        print("\nClosed.")