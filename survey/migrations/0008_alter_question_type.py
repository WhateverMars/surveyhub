# Generated by Django 3.2.6 on 2021-08-12 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_alter_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
