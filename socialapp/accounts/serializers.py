from drf_yasg import openapi
from rest_framework import serializers


class AddUserRequestSerializer(serializers.Serializer):  # Request Serializer for Add User endpoint
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()
    country_code = serializers.CharField()


class AddUserResponseSerializer(serializers.Serializer):  # Response Serializer for Add User endpoint

    @staticmethod
    def success() -> dict:

        # Return the format of the response data
        return {
            'token': openapi.Schema(type=openapi.TYPE_STRING),
        }

    @staticmethod
    def failure() -> dict:

        # Return the format of the response data
        return {'error': openapi.Schema(type=openapi.TYPE_STRING)}


class UpdateUserRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField()
    country_code = serializers.CharField()


class UpdateUserResponseSerializer(serializers.Serializer):

    @staticmethod
    def success() -> dict:

        # Return the format of the Response data
        return {
            '_id': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'country_code': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
        }

    @staticmethod
    def failure() -> dict:

        # Return the format of the response data

        return {'error': openapi.Schema(type=openapi.TYPE_STRING)}


class GetUserResponseSerializer(serializers.Serializer):

    @staticmethod
    def success() -> dict:

        # Return the format of the response data
        return {
            '_id': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'country_code': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
        }

    @staticmethod
    def failure() -> dict:

        # Return the format of the response data
        return {'error': openapi.Schema(type=openapi.TYPE_STRING)}


class LoginUserRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginUserResponseSerializer(serializers.Serializer):

    @staticmethod
    def success() -> dict:
        return {'token': openapi.Schema(type=openapi.TYPE_STRING)}

    @staticmethod
    def failure() -> dict:
        return {'error': openapi.Schema(type=openapi.TYPE_STRING)}


class LogoutUserResponseSerializer(serializers.Serializer):

    @staticmethod
    def success() -> dict:
        return {'blacklisted_token': openapi.Schema(type=openapi.TYPE_STRING)}

    @staticmethod
    def failure() -> dict:
        return {'error': openapi.Schema(type=openapi.TYPE_STRING)}
