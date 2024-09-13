from rest_framework import serializers


class AddUserRequestSerializer(serializers.Serializer):
    _id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()
    country_code = serializers.CharField()
