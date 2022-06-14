# Generated by Django 3.2.10 on 2022-02-23 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifiermodel',
            name='training_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'awaiting submission'), (1, 'running'), (2, 'complete')], default=0),
        ),
    ]
