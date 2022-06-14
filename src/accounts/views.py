import os.path

from django.core.files.uploadedfile import UploadedFile
from drf_spectacular.utils import extend_schema

import core.serializers
from core.views import PostHandlerAPIView
from core.containers import OperationStatus
from core.enums import StatusEnum
from accounts.models import User, CharacterSign
from accounts import serializers


@extend_schema(
    request=serializers.SaveUserCharacterSignRequestSerializer,
    responses=core.serializers.OperationStatusSerializer,
)
class SaveUserCharacterSignView(PostHandlerAPIView):
    request_serializer_class = serializers.SaveUserCharacterSignRequestSerializer
    result_to_dict = True

    def get_handler_kwargs(self) -> dict:
        kwargs = super().get_handler_kwargs()
        data = self.get_request_serializer_data()

        kwargs.update({
            'user': self.request.user,
            'character': data['character'].lower(),
            'file': data['file'],
        })

        return kwargs

    def handler(self, user: User, character: str, file: UploadedFile) -> OperationStatus:

        _, ext = os.path.splitext(file.name)
        file.name = f'{user.username}-{character}.{ext.replace(".", "")}'

        character_model, _ = CharacterSign.objects.get_or_create(user=user, character=character)
        character_model.file = file
        character_model.save()

        result = OperationStatus(
            status=StatusEnum.OK
        )

        return result
