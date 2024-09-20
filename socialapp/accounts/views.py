from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utilities.blank import check_data
from ..utilities.hash import check_password
from ..utilities.hash import hash_password
from ..utilities.regex import check_password_strength
from ..utilities.regex import validate_email
from ..utilities.response import api_response
from .models import Token
from .models import User
from .serializers import AddUserRequestSerializer
from .serializers import AddUserResponseSerializer
from .serializers import GetUserResponseSerializer
from .serializers import LoginUserRequestSerializer
from .serializers import LoginUserResponseSerializer
from .serializers import LogoutUserResponseSerializer
from .serializers import UpdateUserRequestSerializer
from .serializers import UpdateUserResponseSerializer
from socialapp.utilities.auth import authenticate_header
from socialapp.utilities.auth import authenticate_login
from socialapp.utilities.auth import blacklist_token
from socialapp.utilities.auth import generate_auth_token


# Create new user view
class UserView(APIView):
    """
    Class related to user CRUD operations
    """

    # Bypass Django Authentication
    permission_classes = [AllowAny]  # Bypass Django Authentication

    @swagger_auto_schema(  # Create schema for swagger documentation
        operation_description='Add a new user to the database',
        responses={
            200:
                openapi.Response(
                    description='A successful response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,  # Indicates a dictionary (object)
                        properties=AddUserResponseSerializer.success(),
                    ),
                ),
            400:
                openapi.Response(
                    description='A failed response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=AddUserResponseSerializer.failure(),
                    ),
                ),
        },
        request_body=AddUserRequestSerializer,
    )
    # Post method to add user to the database
    def post(self, request):
        """
        Function to save new user into the database
        """
        try:
            # Check if data is valid by serializer
            serializer = AddUserRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    api_response(status=False, error='Invalid Data Format'),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = request.data

            # Duplicate Username Check
            if User.find({'username': data['username']}):
                return Response(
                    api_response(status=False, error='Duplicate Username'),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Duplicate Email Check
            if User.find({'email': data['email']}):
                return Response(
                    api_response(status=False, error='Duplicate Email'),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate email address
            if not validate_email(data['email']):
                return Response(api_response(status=False, error='Invalid Email'), status=status.HTTP_400_BAD_REQUEST)

            # Check for a secure_password
            password_check = check_password_strength(data['password'])
            if not password_check['success']:
                return Response(api_response(status=False, error='Invalid Password'))
            try:
                # Hashing password
                data['password'] = hash_password(data['password'])
            except Exception as HashingError:
                # Return error on password hashing fail
                return Response(
                    api_response(status=False, error=str(HashingError)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Check if none of the fields are empty
            empty_keys = check_data(data, AddUserRequestSerializer)
            return_error = ''
            if not empty_keys == []:
                for key in empty_keys:
                    return_error += f'{key}, ' if not str(key).startswith('_') else ''

                if not return_error == '':
                    return Response(api_response(status=False, error=return_error), status=status.HTTP_400_BAD_REQUEST)

            # Add the user to the database
            new_user = User(
                _id=None,
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['username'],
                password=data['password'],
                phone=data['phone'],
                country_code=data['country_code'],
                email=data['email'],
            )

            # Try to save the user model to the database
            try:
                new_user.save()
            except Exception as DatabaseError:
                # In case of an error, return an error
                return Response(
                    api_response(status=False, error=f'{DatabaseError}: {str(DatabaseError)}'),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            else:
                # In case of no error, create an auth token
                auth_token = generate_auth_token(new_user)

                # Then return the new auth_token
                return_data = {'token': auth_token}
                return Response(
                    api_response(status=True, data=return_data, message='User created successfully'),
                    status=status.HTTP_201_CREATED,
                )

        except Exception as ServerError:
            # In case of an exception, return the error
            return Response(api_response(status=False, error=str(ServerError)))

    @swagger_auto_schema(  # Create schema for swagger documentation
        operation_description='Fetch an user from the database',
        responses={
            200:
                openapi.Response(
                    description='A successful response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,  # Indicates a dictionary (object)
                        properties=GetUserResponseSerializer.success(),
                    ),
                ),
            400:
                openapi.Response(
                    description='A failed response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=GetUserResponseSerializer.failure(),
                    ),
                ),
        },
    )
    # Get method to fetch user from the database
    def get(self, request):
        """
        Function to fetch user from the database
        """
        try:
            # Try to retrieve auth token from request header
            try:
                user, err = authenticate_header(request=request)
            except Exception as E:
                return Response(
                    api_response(status=False, error=f'Authorization Error: {str(E)}'),
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                auth_token = request.headers.get('Authorization')
                # Check if token is already blacklisted
                is_blacklisted = Token.find_one({'token': auth_token})

                if is_blacklisted:
                    # Send error to client if token is already blacklisted
                    return Response(api_response(status=False, error='Token Already Blacklisted'))

                if err:
                    return Response(api_response(status=False, error=str(err)))

            # Query the user and extract user _id
            user_id = user.id

            # Gather the required data into a dict
            return_data = {
                '_id': str(user_id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'country_code': user.country_code,
                'phone': user.phone,
            }

            # Return the dict
            return Response(api_response(status=True, data=return_data))

        except Exception as E:
            # In case of an error, return the error to client
            return Response(api_response(status=False, error=str(E)))

    @swagger_auto_schema(  # Create schema for swagger documentation
        operation_description='Update a user in the database',
        responses={
            200:
                openapi.Response(
                    description='A successful response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,  # Indicates a dictionary (object)
                        properties=UpdateUserResponseSerializer.success(),
                    ),
                ),
            400:
                openapi.Response(
                    description='A failed response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=UpdateUserResponseSerializer.failure(),
                    ),
                ),
        },
        request_body=UpdateUserRequestSerializer,
    )
    # Method to update user data
    def put(self, request):
        """
        Function to partially update user data in the database
        """
        try:
            try:
                # Validate user via auth header
                user, err = authenticate_header(request)

            except Exception as E:
                # Return error as api response
                return Response(api_response(status=False, error=str(E)))

            else:
                auth_token = request.headers.get('Authorization')
                # Check if token is already blacklisted
                is_blacklisted = Token.find_one({'token': auth_token})

                if is_blacklisted:
                    # Send error to client if token is already blacklisted
                    return Response(api_response(status=False, error='Token Already Blacklisted'))

                if err:
                    # Return error as api response
                    return Response(api_response(status=False, error=str(err)))

                # Fetch user id from user object
                user_id = user.id
                # Check if user password is correct
                data = request.data
                user_password = data['password']
                # If the password is correct
                if check_password(user_id, user_password):
                    # Then create object for updated user
                    updated_user = User(
                        _id=user_id,
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        username=data['username'],
                        email=data['email'],
                        phone=data['phone'],
                        password=user.password,  # Keep the same password
                        country_code=user.country_code,
                    )

                    # Save changes to updated user
                    updated_user.update()

                    # Convert ObjectID to str
                    updated_user._id = str(user_id)

                    # Remove the password variable from the dict
                    return_dict = updated_user.to_dict()
                    del return_dict['password']
                    return Response(api_response(status=True, data=return_dict))
                # Return invalid password message
                return Response(api_response(status=False, error='Invalid Password'))

        except Exception as E:
            # Return response with error in case
            return Response(api_response(status=False, error=str(E)))


class LoginView(APIView):
    """
    Login and Logout a user with auth token
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(  # Create schema for swagger documentation
        operation_description='Login an existing user',
        responses={
            200:
                openapi.Response(
                    description='A successful response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,  # Indicates a dictionary (object)
                        properties=LoginUserResponseSerializer.success(),
                    ),
                ),
            400:
                openapi.Response(
                    description='A failed response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=LoginUserResponseSerializer.failure(),
                    ),
                ),
        },
        request_body=LoginUserRequestSerializer,
    )
    # Method to login existing user
    def post(self, request):
        """
        Function to log in user using Auth Token
        """
        try:
            try:
                # Validate User and generate and Auth Token
                return_data = authenticate_login(request)

            except Exception as E:
                # Return error in case of exception
                return Response(api_response(status=False, error=str(E)))

            else:

                if type(return_data['token']) is None:
                    return Response(api_response(status=False, error='Authentication Error'))

                # Check if token is blacklisted
                token = Token.find_one({'token': request.headers.get('Authorization')})

                if token:
                    # If blacklisted, return appropriate message
                    return Response(api_response(status=False, error='Token Blacklisted'))
                # If no exception, then return success message
                return Response(api_response(status=True, data=return_data))

        except Exception as E:

            # Return error in case of exception
            return Response(api_response(status=False, error=str(E)))


class LogoutView(APIView):
    """
    Class to implement logout functionality
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(  # Create schema for swagger documentation
        operation_description='Log out an existing logged-in user',
        responses={
            200:
                openapi.Response(
                    description='A successful response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,  # Indicates a dictionary (object)
                        properties=LogoutUserResponseSerializer.success(),
                    ),
                ),
            400:
                openapi.Response(
                    description='A failed response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties=LogoutUserResponseSerializer.failure(),
                    ),
                ),
        },
    )
    # Method to logout logged-in user
    def get(self, request):
        """
        Function to log out and blacklist user token
        """
        try:
            # Retrieve auth token from header
            try:
                auth_token = request.headers.get('Authorization')
            except Exception as E:

                return Response(api_response(status=False, error=str(E)))

            else:
                # Check if token is already blacklisted
                is_blacklisted = Token.find_one({'token': auth_token})

                if is_blacklisted:
                    # Send error to client if token is already blacklisted
                    return Response(api_response(status=False, error='Token Already Blacklisted'))

                blacklist_status, err = blacklist_token(auth_token)  # Add token to blacklist database

                if not blacklist_status:
                    # Return error if token failed to be blacklisted
                    return Response(api_response(status=False, error='Database Error'))

                return Response(api_response(status=True, data={'blacklisted_token': auth_token}))

        except Exception as E:

            return Response(api_response(status=False, error=str(E)))
