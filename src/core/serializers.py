from rest_framework import serializers


class OperationStatusSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)