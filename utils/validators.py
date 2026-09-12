def not_empty(value):
    return value.strip() != ""


def valid_email(email):
    return "@" in email and "." in email