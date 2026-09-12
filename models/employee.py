from pathlib import Path

from utils.storage import load_json, save_json


class Employee:

    def __init__(self, employee_id, name, department, salary):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.role_title = "Staff"
        self._salary = salary
        self.work_log = []       
        self.conduct_notes = []  

    def get_salary(self):
        return self._salary

    def set_salary(self, new_salary):
        if new_salary < 0:
            print("Salary cannot be negative.")
            return
        self._salary = new_salary

    def log_work(self, date, hours):
        self.work_log.append((date, hours))

    def total_hours(self):
        total = 0
        for date, hours in self.work_log:
            total += hours
        return total

    def add_conduct_note(self, author, note):
        self.conduct_notes.append((author, note))

    def summary(self):
        return (f"[{self.employee_id}] {self.name} | {self.department} | "
                f"{self.role_title} | Salary: {self._salary} | "
                f"Hours logged: {self.total_hours()}")

    def to_dict(self):
        return {
            "type": "employee",
            "employee_id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "role_title": self.role_title,
            "salary": self._salary,
            "work_log": self.work_log,
            "conduct_notes": self.conduct_notes,
        }

    @classmethod
    def from_dict(cls, data):
        employee = cls(data["employee_id"], data["name"], data["department"], data["salary"])
        employee.role_title = data.get("role_title", "Staff")
        employee.work_log = [tuple(item) for item in data.get("work_log", [])]
        employee.conduct_notes = [tuple(item) for item in data.get("conduct_notes", [])]
        return employee


class Manager(Employee):
   

    def __init__(self, employee_id, name, department, salary):
        super().__init__(employee_id, name, department, salary)
        self.role_title = "Manager"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "manager"
        return data



class EmployeeDirectory:

    def __init__(self, employees_file="data/employees.json"):
        self.employees_file = Path(employees_file)

    def _load(self):
        records = load_json(self.employees_file)
        employees = []
        for record in records:
            if record["type"] == "manager":
                employees.append(Manager.from_dict(record))
            else:
                employees.append(Employee.from_dict(record))
        return employees

    def _save(self, employees):
        save_json(self.employees_file, [employee.to_dict() for employee in employees])

    def add_employee(self, employee):
        employees = self._load()
        employees.append(employee)
        self._save(employees)

    def get_all(self):
        return self._load()

    def get_by_department(self, department):
        result = []
        for employee in self._load():
            if employee.department.lower() == department.lower():
                result.append(employee)
        return result

    def find_by_id(self, employee_id):
        for employee in self._load():
            if employee.employee_id == employee_id:
                return employee
        return None

    def update_employee(self, updated_employee):
        employees = self._load()
        for index, employee in enumerate(employees):
            if employee.employee_id == updated_employee.employee_id:
                employees[index] = updated_employee
        self._save(employees)

    def remove_employee(self, employee_id):
        employees = self._load()
        employees = [e for e in employees if e.employee_id != employee_id]
        self._save(employees)
