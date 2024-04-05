# Generated by Django 3.2.6 on 2021-08-11 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("survey", "0005_question_asker"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="asker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
