
import re


PATTERNS_ = {
    "word": "^[a-zA-Z]+$",
    "integer": "^[0-9]+$",
    "positive_decimal_or_empty_string": "^[0-9]+\.?[0-9]*$|^$",
    "alphanumeric_with_spaces_or_empty_string": "^[a-zA-Z0-9 ]+$|^$",
    "alphanumeric_or_empty_string": "^[a-zA-Z0-9]+$|^$",
    "alphanumeric_spaces_dots_commas_or_empty_string": "^[a-zA-Z0-9 \.,]+$|^$",
    "customer_id": "^[a-zA-Z0-9\-]+$|^$",
    # Adapted pattern from: https://stackoverflow.com/questions/22061723/regex-date-validation-for-yyyy-mm-dd
    "date": "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$|^$",
    "address": "^[a-zA-Z0-9\-,\.#()\/ ]+$",
    # Had to ignore due to last minute demo_data phone numbers
    # "phone_number": "^\+[0-9]+\(\d{3}\)\d{3}-\d{4}$", 
    "phone_number": "^[0-9\+\-\(\)]+$",
    "business_name": "^[a-zA-Z0-9\-,\.# ]+$",
    "composed_name": "^[a-zA-Z ]+$",
    "email": "^[a-zA-Z0-9\-_\.@ ]+$|^$",
    "part_number": "^[a-zA-Z0-9\-\.\_]+$|^$"
}

def is_valid(type_, value):
    try:
        if PATTERNS_.get(type_):
            if re.match(PATTERNS_[type_], str(value)):
                return True, "Matched"
            return False, "Didn't matched"
        else:
            return False, f"Type: '{type_}' not in validation types: {list(PATTERNS_.keys())}"
    except Exception as ex:
        return False, "There was an error when matching pattern"