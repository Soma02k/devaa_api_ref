import re

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def validate_email_format(email: str) -> bool:
    """Validate email address format using regular expression."""
    if not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))

def validate_salary(salary) -> bool:
    """Validate salary is non-negative number."""
    if salary is None:
        return True
    try:
        val = float(salary)
        return val >= 0
    except (ValueError, TypeError):
        return False

def validate_employee_payload(data: dict, required_fields: list = None, is_update: bool = False):
    """
    Validate input data payload for employee POST and PUT requests.
    
    :param data: JSON payload dictionary
    :param required_fields: List of field names that must be present
    :param is_update: True if validating partial updates (PUT)
    :return: (is_valid: bool, error_message: str)
    """
    if not isinstance(data, dict):
        return False, "Request body must be a valid JSON object"

    if required_fields is None:
        required_fields = []

    if not is_update:
        # Validate mandatory required fields for creation
        for field in required_fields:
            if field not in data or data[field] is None:
                return False, f"Field '{field}' is required"
            if isinstance(data[field], str) and not data[field].strip():
                return False, f"Field '{field}' cannot be empty"
    else:
        if not data:
            return False, "No data provided for update"

    # Validate non-empty string constraint for critical fields if provided
    for field in ['name', 'email', 'phone']:
        if field in data and data[field] is not None:
            if isinstance(data[field], str) and not data[field].strip():
                return False, f"Field '{field}' cannot be empty string"

    # Email format validation
    if 'email' in data and data['email'] is not None:
        if not validate_email_format(data['email']):
            return False, "Invalid email format"

    # Salary validation
    if 'salary' in data and data['salary'] is not None:
        if not validate_salary(data['salary']):
            return False, "Salary must be a non-negative numeric value"

    return True, None
