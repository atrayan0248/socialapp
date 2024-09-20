from rest_framework import serializers


class AddUserDetailsRequestSerializer(serializers.Serializer):
    details = serializers.JSONField()


class UpdateUserDetailsRequestSerializer(serializers.Serializer):
    details = serializers.JSONField()
