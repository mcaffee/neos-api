from django.db import models

from accounts.models import User
from django.utils.translation import gettext_lazy as _


class TrainingStatusChoices(models.IntegerChoices):
    AWAITING_SUBMISSION = 0, _('awaiting submission')
    RUNNING = 1, _('running')
    COMPLETE = 2, _('complete')


class ClassifierModel(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='classifier_model')
    data = models.FileField(null=True, blank=True)
    training_status = models.PositiveSmallIntegerField(
        choices=TrainingStatusChoices.choices,
        default=TrainingStatusChoices.AWAITING_SUBMISSION
    )
