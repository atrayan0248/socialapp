# Import Bcrypt library for password hashing
import bcrypt

from socialapp.accounts.models import User

# Import User model for password checking


# Define method for hashing password
def hash_password(password: str) -> str:
    """
    Hashes the password using Bcrypt
    """
    # Convert the password string to bytes using 'utf-8' encoding
    password_bytes = password.encode('utf-8')
    # Hash the password
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    # Return the decoded hashed password string
    return hashed_bytes.decode('utf-8')


# Define method for checking password
def check_password(_id: str, password: str) -> bool:
    """
    Checks the hashed password against the database and returns True or False
    """
    # Get the hashed password from the user using _id
    user = User.find_one({'_id': _id})

    if not user:
        return False

    hashed_password = user.password

    # Convert the password from argument to bytes
    password_bytes = password.encode('utf-8')

    # Check if the password matches
    if not bcrypt.checkpw(password_bytes, hashed_password):
        # If not, return False
        return False
    else:
        # Else return True
        return True
