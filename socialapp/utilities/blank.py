from rest_framework import serializers


def check_data(data: dict, serializer: serializers.Serializer) -> list:
    return_data = []
    attributes = serializer.__dict__

    for key, _value in attributes.items():
        try:
            if data[key] == '':
                return_data.append(key)
        except Exception:
            return_data.append(key)

    return return_data
