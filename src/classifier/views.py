import base64

from drf_spectacular.utils import extend_schema

from classifier.containers import ModelTrainingStatus, ModelTrainingData
from classifier.models import ClassifierModel, TrainingStatusChoices
from core.exceptions import DoesNotExist
from core.views import GetHandlerAPIView, PostHandlerAPIView
from accounts.models import User, CharacterSign
from classifier import serializers
from classifier.tasks import run_post_training


@extend_schema(
    responses=serializers.ModelTrainingStatusSerializer,
)
class StartUserModelTrainingView(PostHandlerAPIView):
    result_to_dict = True

    def get_handler_kwargs(self) -> dict:
        kwargs = super().get_handler_kwargs()

        kwargs.update({
            'user': self.request.user,
        })

        return kwargs

    def handler(self, user: User) -> ModelTrainingStatus:
        classifier_model, _ = ClassifierModel.objects.get_or_create(user=user)

        # # we don't interrupt a process that is already running
        # if classifier_model.training_status != TrainingStatusChoices.RUNNING:
        if CharacterSign.objects.alphabet_complete(user):
            run_post_training.s(user_id=user.id).apply_async()

            result = ModelTrainingStatus(
                status=TrainingStatusChoices.RUNNING.name
            )
        else:
            result = ModelTrainingStatus(
                status=TrainingStatusChoices.AWAITING_SUBMISSION.name
            )

        return result


@extend_schema(
    responses=serializers.ModelTrainingStatusSerializer,
)
class GetUserModelTrainingStatusView(GetHandlerAPIView):
    result_to_dict = True

    def get_handler_kwargs(self) -> dict:
        kwargs = super().get_handler_kwargs()
        # data = self.get_request_serializer_data()

        kwargs.update({
            'user': self.request.user,
        })

        return kwargs

    def handler(self, user: User) -> ModelTrainingStatus:
        classifier_model, _ = ClassifierModel.objects.get_or_create(user=user)

        result = ModelTrainingStatus(
            status=classifier_model.get_training_status_display()
        )

        return result


@extend_schema(
    responses=serializers.ModelTrainingDataSerializer,
)
class GetUserModelTrainingDataView(GetHandlerAPIView):
    result_to_dict = True

    def get_handler_kwargs(self) -> dict:
        kwargs = super().get_handler_kwargs()

        kwargs.update({
            'user': self.request.user,
        })

        return kwargs

    def handler(self, user: User) -> ModelTrainingData:
        classifier_model, _ = ClassifierModel.objects.get_or_create(user=user)

        if classifier_model.training_status != TrainingStatusChoices.COMPLETE:
            raise DoesNotExist('Training data is not ready yet.')

        result = ModelTrainingData(
            data=base64.b64encode(classifier_model.data.read()).decode()
        )

        return result
