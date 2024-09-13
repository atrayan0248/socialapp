from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utilities.regex import validate_email
from ..utilities.response import api_response
from .models import User
from .serializers import AddUserRequestSerializer

# from rest_framework import status


# Create new user view
class AddUserView(APIView):
    """
    Adds a new user to the database
    """

    @swagger_auto_schema(
        operation_description='Add a new user to the database',
        request_body=AddUserRequestSerializer,
    )
    # Post method to add user to the database
    def post(self, request):
        # Check if data is valid by serializer
        serializer = AddUserRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(api_response(status=False, error='Invalid Data Format'))

        data = request.data

        # Duplicate Username Check
        if User.find({'username': data['username']}):
            return Response(api_response(status=False, error='Duplicate Username'))

        # Duplicate Email Check
        if User.find({'email': data['email']}):
            return Response(api_response(status=False, error='Duplicate Email'))

        # Validate email address
        if not validate_email(data['email']):
            return Response(api_response(status=False, error='Invalid Email'))

        return Response(api_response(status=True, data={}))
