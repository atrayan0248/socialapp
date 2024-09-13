from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utilities.blank import check_data
from ..utilities.hash import hash_password
from ..utilities.regex import validate_email
from ..utilities.response import api_response
from .models import User
from .serializers import AddUserRequestSerializer
from .serializers import AddUserResponseBody


# Create new user view
class AddUserView(APIView):
    """
    Adds a new user to the database
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description='Add a new user to the database',
        reponses={
            200:
                openapi.Response(
                    description='A successful response',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,  # Indicates a dictionary (object)
                        properties=AddUserResponseBody.add_user_response(),
                    ),
                ),
            400:
                'Bad Request',
        },
        request_body=AddUserRequestSerializer,
    )
    # Post method to add user to the database
    def post(self, request):
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
                    api_response(status=False, error=str(DatabaseError)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            else:
                # In case of no error, return the new user id, username, and email
                return_data = {'_id': str(new_user.id), 'username': new_user.username, 'email': new_user.email}
                return Response(
                    api_response(status=True, data=return_data, message='User created successfully'),
                    status=status.HTTP_201_CREATED,
                )

        except Exception as ServerError:
            # In case of an exception, return the error
            return Response(api_response(status=False, error=str(ServerError)))
