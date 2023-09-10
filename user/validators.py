import re


def is_valid_phone_number(value):
    mobile_regex = "^09(1[0-9]|3[1-9])-?[0-9]{3}-?[0-9]{4}$"
    if not (re.search(mobile_regex, value)):
        return False
    return True
