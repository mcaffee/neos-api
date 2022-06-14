import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser

from core.enums import LiteralEnum


class User(AbstractUser):
    api_key = models.UUIDField(default=uuid.uuid4)


class CharacterSignManager(models.Manager):
    def alphabet_complete(self, user: User) -> bool:
        return user.signs.count() == len(LiteralEnum)


class CharacterSign(models.Model):
    objects = CharacterSignManager()

    class Meta:
        unique_together = [['user', 'character']]

    user = models.ForeignKey(User, models.CASCADE, related_name='signs')
    character = models.CharField(max_length=1)
    file = models.FileField()
