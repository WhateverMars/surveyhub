# Generated by Django 3.2.6 on 2021-08-09 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Analysis",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("userstot", models.IntegerField()),
                ("number", models.IntegerField()),
                ("question", models.CharField(max_length=255)),
                ("ans1count", models.IntegerField()),
                ("ans2count", models.IntegerField()),
                ("ans3count", models.IntegerField()),
                ("ans4count", models.IntegerField()),
                ("ans5count", models.IntegerField()),
                ("ans6count", models.IntegerField()),
                ("ans1", models.CharField(max_length=255)),
                ("ans2", models.CharField(max_length=255)),
                ("ans3", models.CharField(max_length=255)),
                ("ans4", models.CharField(max_length=255)),
                ("ans5", models.CharField(max_length=255)),
                ("ans6", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("number", models.IntegerField()),
                ("question", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=64)),
                ("ans1", models.CharField(max_length=255)),
                ("ans2", models.CharField(max_length=255)),
                ("ans3", models.CharField(max_length=255)),
                ("ans4", models.CharField(max_length=255)),
                ("ans5", models.CharField(max_length=255)),
                ("ans6", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("user", models.IntegerField()),
                ("number", models.IntegerField()),
                ("question", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=64)),
                ("answer", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=64)),
                ("hash", models.CharField(max_length=64)),
                ("questions", models.IntegerField()),
            ],
        ),
    ]
