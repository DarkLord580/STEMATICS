from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models
from django.utils.timezone import now



class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=128, default="")
    imageurl = models.CharField(max_length=1024
        ,default="https://lh3.googleusercontent.com/ogw/ADGmqu83910wkHMPdQYwo6o7h8MIAD-wnEBgWa0b2syc=s192-c-mo")
    
    

class Card(models.Model):
    category = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    meaning = models.TextField(default="")
    createdate = models.DateTimeField(auto_now_add=True)
    
class NewCardForm(forms.ModelForm):
    class Meta:
       model = Card
       fields = ["category","title", "meaning"]
       
class Comment(models.Model):
    itemid = models.IntegerField()
    commentuser = models.CharField(max_length=128)
    comment = models.CharField(max_length=1024)
    createdate = models.DateTimeField(auto_now_add=True)
   
    
class Watchitem(models.Model):
    user = models.CharField(max_length=128)
    itemid = models.IntegerField()
    createdate = models.DateTimeField(auto_now_add=True)
    

