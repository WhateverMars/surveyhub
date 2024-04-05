from django.db import models
from django.db.models.fields import IntegerField
from django.contrib.auth.models import User

# Create your models here.


class Surveyer(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    questions = models.IntegerField(default=0)
    link = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user.username}"


class Question(models.Model):
    asker = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    question = models.CharField(max_length=255)
    type = models.IntegerField(default=0)
    ans1 = models.CharField(max_length=255)
    ans2 = models.CharField(max_length=255)
    ans3 = models.CharField(max_length=255)
    ans4 = models.CharField(max_length=255)
    ans5 = models.CharField(max_length=255)
    ans6 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question}"


class Result(models.Model):
    asker = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.IntegerField()
    number = models.IntegerField()
    question = models.CharField(max_length=255)
    type = models.IntegerField(default=0)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.answer}"


class Analysis(models.Model):
    asker = models.ForeignKey(User, on_delete=models.CASCADE)
    userstot = models.IntegerField()
    number = models.IntegerField()
    question = models.CharField(max_length=255)
    ans1count = models.IntegerField()
    ans2count = models.IntegerField()
    ans3count = models.IntegerField()
    ans4count = models.IntegerField()
    ans5count = models.IntegerField()
    ans6count = models.IntegerField()
    ans1 = models.CharField(max_length=255)
    ans2 = models.CharField(max_length=255)
    ans3 = models.CharField(max_length=255)
    ans4 = models.CharField(max_length=255)
    ans5 = models.CharField(max_length=255)
    ans6 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.number: self.question}"
