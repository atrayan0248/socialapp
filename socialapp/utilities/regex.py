import re

# Define regular expression for email validation
email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


# Email Verification method with regular expression
def validate_email(email: str) -> bool:
    # Check if email pattern matches regex
    if email_pattern.match(email):
        # If pattern matches return True
        return True
    else:
        # Else return False
        return False


def check_password_strength(password: str) -> dict:

    return_data = {'success': True, 'error': None}

    # Check the length of the password
    if not len(password) >= 8:
        return_data['success'] = False,
        return_data['error'] = 'Password must be at least 8 characters'
        return return_data

    # Check for digits
    if not re.search(r'\d', password):
        return_data['success'] = False,
        return_data['error'] = 'Password must contain at least 1 digit'
        return return_data

    # Check for uppercase letters
    if not re.search(r'[A-Z]', password):
        return_data['success'] = False,
        return_data['error'] = 'Password must contain at least 1 digit'
        return return_data

    # Check for lowercase letters
    if not re.search(r'[a-z]', password):
        return_data['success'] = False,
        return_data['error'] = 'Password must contain at least 1 digit'
        return return_data

    # Check for special characters
    if not re.search(r'[@$!%*#?&]', password):
        return_data['success'] = False,
        return_data['error'] = 'Password must contain at least 1 digit'
        return return_data

    return return_data
