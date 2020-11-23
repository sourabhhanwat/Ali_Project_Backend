from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    """
    project_create_access=models.BooleanField(default=False)


class PlatformType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BracingType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class NumberOfLegsType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PlatformMannedStatus(models.Model):
    name = models.CharField(max_length=200)
    ranking = models.CharField(max_length=1, default="A")
    description = models.CharField(max_length=600, default="")

    def __str__(self):
        return self.name
