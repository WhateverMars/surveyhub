# Generated by Django 3.2.6 on 2021-08-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_alter_analysis_ans1count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='ans2count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='ans3count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='ans4count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='ans5count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='ans6count',
            field=models.IntegerField(null=True),
        ),
    ]