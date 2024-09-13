from drf_yasg import openapi
from rest_framework import serializers


class AddUserRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()
    country_code = serializers.CharField()


class AddUserResponseBody:

    @staticmethod
    def add_user_response() -> dict:
        return {
            '_id': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
        }
