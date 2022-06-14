from rest_framework import serializers


class ModelTrainingStatusSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)


class ModelTrainingDataSerializer(serializers.Serializer):
    data = serializers.CharField(required=True)
