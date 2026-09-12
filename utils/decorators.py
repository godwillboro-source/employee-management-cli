def login_required(function):
  def wrapper(self, *args, **kwargs):
    if self.current_user is None:
      print("Please login first.")
      return
    return function(self, *args, **kwargs)
  return wrapper


def employer_required(function):
  def wrapper(self, *args, **kwargs):
    if self.current_user is None:
      print("Please login first.")
      return
    if self.current_user.role != "employer":
      print("Only the employer can do that.")
      return
    return function(self, *args, **kwargs)
  return wrapper


def manager_required(function):
  def wrapper(self, *args, **kwargs):
    if self.current_user is None:
      print("Please login first.")
      return
    if self.current_user.role != "manager":
      print("Only a manager can do that.")
      return
    return function(self, *args, **kwargs)
  return wrapper