import re

# Define regular expression
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
