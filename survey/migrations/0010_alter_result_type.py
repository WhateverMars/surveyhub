# Generated by Django 3.2.6 on 2021-08-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_result_asker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
