from datetime import datetime
from datetime import timedelta

import jwt
from bson import ObjectId
from django.conf import settings

from socialapp.accounts.models import Token
from socialapp.accounts.models import User
from socialapp.utilities.hash import check_password


def authenticate_header(request) -> tuple:
    """
    Function to implement Token Authentication from request headers
    """

    # Get bearer token from request header
    auth_token = request.headers.get('Authorization')

    # Validate the auth token and get user_id from it
    user_id, error = validate_token(auth_token)

    if not error:
        user = User.find_one({'_id': ObjectId(user_id)})  # Find user by user id

        if not user:
            return None, None  # Return None if user does not exist

        return user, None  # Return user if authentication worked

    return None, None  # Return None if token validation failed


def authenticate_login(request) -> dict:
    """
    Function to implement Token Authentication for login view
    """

    # Initialize return dict
    return_data = {}

    # Get username and password from request data
    username = request.data.get('username')
    password = request.data.get('password')

    # Validate username and password
    user = User.find_one({'username': username})  # Find the user by username

    if not user:
        return_data['token'] = None

    if not check_password(password, user.password):  # Check password with hashed password
        return_data['token'] = None

    # Generate auth token using JWT
    auth_token = generate_auth_token(user)
    return_data['token'] = auth_token  # Append auth token to return data

    return return_data


def generate_auth_token(user: User) -> str:
    """
    Function to generate Auth Token for Token Auth Implementation
    """

    payload_data = {    # Initialize payload for JWT Encryption
        'sub': str(user.id),
        'name': f'{user.first_name} {user.last_name}',
        'exp': datetime.utcnow() + timedelta(days=2),
        'iat': datetime.utcnow(),
    }

    # Get secret key from django config
    secret_key = settings.SECRET_KEY

    # Encode token using HS256
    token = jwt.encode(payload=payload_data, key=secret_key)

    return str(token)


def validate_token(auth_token: str) -> tuple:
    """
    Function to validate auth token for Token Auth Implementation
    """

    secret_key = settings.SECRET_KEY  # Get secret key from django settings

    # Try to decode auth token
    try:
        payload_data: dict = jwt.decode(
            auth_token,
            secret_key,
            algorithms=['HS256'],
        )  # Decode auth token into payload data dict
    except Exception as DecodeError:
        return None, str(DecodeError)

    # Extract user id from payload data
    user_id = payload_data['sub']

    # Return user id and None as error
    return user_id, None


def blacklist_token(auth_token: str) -> tuple:
    """
    Function to blacklist auth token upon user logout
    """
    try:
        blacklisted_token = Token(token=auth_token)
        blacklisted_token.save()
    except Exception as E:

        return False, str(E)

    else:

        return True, None
