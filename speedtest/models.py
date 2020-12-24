from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models
from django.utils.timezone import now



class User(AbstractUser):
    pass




class TestString(models.Model):
    string = models.TextField(default="")
    createdate = models.DateTimeField(auto_now_add=True)
 