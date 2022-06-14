import shutil

from django.conf import settings
from django.core.files import File

from core import celery_app
from core.containers import OperationStatus
from core.enums import StatusEnum

from accounts.models import User
from user_model.ds_tools import CV2Generator, Splitter
from classifier.models import ClassifierModel, TrainingStatusChoices
from user_model.model_tools import ModelConverter
from user_model.user_model import UserModel


@celery_app.task
def run_post_training(user_id: int):
    user = User.objects.get(id=user_id)
    classifier_model, _ = ClassifierModel.objects.get_or_create(user=user)

    # set running status
    classifier_model.training_status = TrainingStatusChoices.RUNNING
    classifier_model.save()

    user_dir = settings.MODEL_TMP_DIR / user.username
    train_dir = user_dir / 'train'
    validate_dir = user_dir / 'validate'
    model_save_path = user_dir / 'model-user'
    tflite_model_save_path = user_dir / 'model-user.tflite'

    # cleanup
    try:
        shutil.rmtree(str(user_dir))
    except FileNotFoundError:
        pass

    # create dirs
    train_dir.mkdir(parents=True, exist_ok=True)
    validate_dir.mkdir(parents=True, exist_ok=True)

    # prepare dataset
    for sign in user.signs.all():
        cv2_gen = CV2Generator([sign.file.path], train_dir / sign.character)
        cv2_gen.generate()

        splitter = Splitter(train_dir / sign.character, validate_dir / sign.character, split=0.15)
        splitter.split()

    # run training
    user_model = UserModel(
        base_model_path=settings.USER_CLASSIFIER_MODEL['BASE_MODEL_PATH'],
        train_path=train_dir,
        validate_path=validate_dir,
        save_path=model_save_path,
    )
    user_model.train()
    user_model.fine_tune()
    user_model.save()

    # convert model
    converter = ModelConverter(model_save_path, tflite_model_save_path)
    converter.convert()

    # save result
    with open(tflite_model_save_path, 'rb') as infile:
        model_file = File(infile)
        name = f'{user.username}-user-model.tflite'
        classifier_model.data.save(name, model_file)

    # set running status
    classifier_model.training_status = TrainingStatusChoices.COMPLETE
    classifier_model.save()

    # cleanup
    try:
        shutil.rmtree(str(user_dir))
    except FileNotFoundError:
        pass

    operation_status = OperationStatus(
        status=StatusEnum.OK
    )
    return operation_status.dict()
