from pathlib import Path

from models.user import User
from utils.storage import load_json, save_json
from utils.validators import not_empty, valid_email


class AuthManager:
  def __init__(self, users_file="data/users.json"):
    self.users_file = Path(users_file)

  def register(self, name, email, password, role, employee_id=None):
    email = email.strip().lower()

    if not not_empty(name):
      print("Name cannot be empty.")
      return None
    if not valid_email(email):
      print("Please enter a valid email.")
      return None

    users = load_json(self.users_file)
    for user in users:
      if user["email"] == email:
        print("An account with that email already exists.")
        return None

    password_hash = User.hash_password(password)
    user = User(name, email, password_hash, role, employee_id)
    users.append(user.to_dict())
    save_json(self.users_file, users)
    return user

  def login(self, email, password):
    email = email.strip().lower()
    users = load_json(self.users_file)

    for record in users:
      if record["email"] == email:
        user = User.from_dict(record)
        if user.check_password(password):
          return user
        return None

    return None

  def delete_user(self, email):
    email = email.strip().lower()
    users = load_json(self.users_file)
    users = [u for u in users if u["email"] != email]
    save_json(self.users_file, users)