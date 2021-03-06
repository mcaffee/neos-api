# Generated by Django 3.2.10 on 2022-02-23 19:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220223_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charactersign',
            old_name='literal',
            new_name='character',
        ),
        migrations.AlterField(
            model_name='user',
            name='api_key',
            field=models.UUIDField(default=uuid.UUID('ae4361e9-ffb0-4195-b76f-a30bfe85dd5e')),
        ),
        migrations.AlterUniqueTogether(
            name='charactersign',
            unique_together={('user', 'character')},
        ),
    ]
