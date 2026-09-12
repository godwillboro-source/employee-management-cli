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