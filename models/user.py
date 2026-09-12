import hashlib


class User:

  def __init__(self, name, email, password_hash, role, employee_id=None):
    self.name = name
    self.email = email
    self.password_hash = password_hash
    self.role = role
    self.employee_id = employee_id

  @staticmethod
  def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

  def check_password(self, password):
    return self.password_hash == self.hash_password(password)

  def to_dict(self):
    return {
      "name": self.name,
      "email": self.email,
      "password_hash": self.password_hash,
      "role": self.role,
      "employee_id": self.employee_id,
    }

  @classmethod
  def from_dict(cls, data):
    return cls(
      data["name"],
      data["email"],
      data["password_hash"],
      data["role"],
      data.get("employee_id"),
    )