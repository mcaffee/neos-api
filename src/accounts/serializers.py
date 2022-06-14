from rest_framework import serializers

from core.enums import LiteralEnum


class SaveUserCharacterSignRequestSerializer(serializers.Serializer):
    character = serializers.ChoiceField(
        choices=[v.value for v in LiteralEnum] + [v.value.lower() for v in LiteralEnum]
    )
    file = serializers.FileField(required=True)
