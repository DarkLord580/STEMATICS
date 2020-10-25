from django.contrib.auth.models import AbstractUser
from django import forms
from django.db import models
from django.utils.timezone import now



class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=128, default="")
    
    

class Item(models.Model):
    owner = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    imageurl = models.CharField(max_length=1024
        ,default="https://lh3.googleusercontent.com/ogw/ADGmqu83910wkHMPdQYwo6o7h8MIAD-wnEBgWa0b2syc=s192-c-mo")
    description = models.TextField(default="")
    currentbid = models.IntegerField(default=0)
    
    maxbider = models.CharField(max_length=128, default=None,blank=True,null=True)
    createdate = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    
class NewItemForm(forms.ModelForm):
    class Meta:
       model = Item
       fields = ["owner","category", "title", "imageurl", "description", "currentbid"]
       
       

    
class Bid(models.Model):
    itemid = models.IntegerField()
    biduser= models.CharField(max_length=128)
    bid = models.IntegerField()
    biddate = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    itemid = models.IntegerField()
    commentuser = models.CharField(max_length=128)
    comment = models.CharField(max_length=1024)
    createdate = models.DateTimeField(auto_now_add=True)
   
    
class Watchitem(models.Model):
    user = models.CharField(max_length=128)
    itemid = models.IntegerField()
    createdate = models.DateTimeField(auto_now_add=True)
    

