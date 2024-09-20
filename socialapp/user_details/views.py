from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from socialapp.accounts.models import Token
from socialapp.user_details.serializers import AddUserDetailsRequestSerializer
from socialapp.user_details.serializers import UpdateUserDetailsRequestSerializer
from socialapp.utilities.auth import authenticate_header
from socialapp.utilities.response import api_response


class UserDetailsView(APIView):
    """
    Class related to user details crud operations
    """

    # Bypass Django Authentication
    permission_classes = [AllowAny]

    @swagger_auto_schema(  # Create schema for swagger documentation
        operation_description='View user details',
    )
    # GET method to fetch user details from the database
    def get(self, request):
        """
        Function to fetch user details
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

                if not auth_token:
                    return Response(
                        api_response(status=False, error='No auth token provided'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                # Check if token is already blacklisted
                is_blacklisted = Token.find_one({'token': auth_token})

                if is_blacklisted:
                    # Send error to client if token is already blacklisted
                    return Response(
                        api_response(status=False, error='Token Already Blacklisted'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                if not user:
                    return Response(
                        api_response(status=False, error='User not found'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

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
                'details': user.details,
            }

            # Return the dict
            return Response(api_response(status=True, data=return_data), status=status.HTTP_200_OK)

        except Exception as E:
            # In case of an error, return the error to client
            return Response(api_response(status=False, error=str(E)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(  # Create schema for swagger documentation
        operation_description='Add user details',
        request_body=AddUserDetailsRequestSerializer,
    )
    # POST Method to add user details to the database
    def post(self, request):
        """
        Function to add user details
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

                if not auth_token:
                    return Response(
                        api_response(status=False, error='No auth token provided'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                # Check if token is already blacklisted
                is_blacklisted = Token.find_one({'token': auth_token})

                if is_blacklisted:
                    # Send error to client if token is already blacklisted
                    return Response(
                        api_response(status=False, error='Token Already Blacklisted'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                if not user:
                    return Response(
                        api_response(status=False, error='User not found'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                try:
                    # Get data from request body
                    data = request.data

                    user.details = {  # Create User Details Document
                        'age': data['details']['age'],
                        'sex': data['details']['sex'],
                        'city': data['details']['city'],
                        'interests': data['details']['interests'],
                    }
                except Exception as E:
                    return Response(api_response(status=False, error=str(E)), status=status.HTTP_400_BAD_REQUEST)

                try:
                    # Save User Details Document
                    user.update()
                except Exception as E:
                    # Database error. Sent to client
                    return Response(
                        api_response(status=False, error=str(E)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                else:
                    return_data = {
                        '_id': str(user.id),
                        'username': user.username,
                        'details': user.details,
                    }
                    return Response(api_response(status=True, data=return_data), status=status.HTTP_201_CREATED)

        except Exception as E:
            # In case of an Exception, return it to the client
            return Response(api_response(status=False, error=str(E)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(operation_description='Update user details', request_body=UpdateUserDetailsRequestSerializer)
    def put(self, request):  # PUT Method to update user details
        """
        Function to update user details in the database
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

                if not auth_token:
                    return Response(
                        api_response(status=False, error='No auth token provided'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                # Check if token is already blacklisted
                is_blacklisted = Token.find_one({'token': auth_token})

                if is_blacklisted:
                    # Send error to client if token is already blacklisted
                    return Response(
                        api_response(status=False, error='Token Already Blacklisted'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                if not user:
                    return Response(
                        api_response(status=False, error='User not found'),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                try:
                    data = request.data
                    user.details = {
                        'age': data['age'],
                        'sex': data['sex'],
                        'interests': data['interests'],
                        'city': data['city'],
                    }
                    user.save()
                except Exception as E:

                    # Return database error to user
                    return Response(api_response(status=False, error=str(E)), status=status.HTTP_502_BAD_GATEWAY)

                else:
                    # In case of no error, parse the return dict
                    return_data = {
                        'age': user.details['age'],
                        'sex': user.details['sex'],
                        'interests': user.details['interests'],
                        'city': user.details['city'],
                    }
                    # Return the dic to the user
                    return Response(api_response(status=True, data=return_data), status=status.HTTP_200_OK)

        except Exception as E:

            # Return Server Error to user
            return Response(api_response(status=False, error=str(E)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
