# Generated by Django 3.2.6 on 2021-08-16 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("survey", "0008_alter_question_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="asker",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="auth.user"
            ),
            preserve_default=False,
        ),
    ]
