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
    
    def __str__(self):
        return ' Category:{}  \n url:{}\n'.format(self.category, self.imageurl)

class Card(models.Model):
    category = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    meaning = models.TextField(default="")
    createdate = models.DateTimeField(auto_now_add=True)
    imageurl = models.CharField(max_length=1024
        ,default="")
    
class NewCardForm(forms.ModelForm):
    class Meta:
       model = Card
       fields = ["category","title", "meaning","imageurl"]
       
class NewCategoryForm(forms.ModelForm):
    class Meta:
       model = Category
       fields = ["category","imageurl"]
       
class Comment(models.Model):
    cardid = models.IntegerField()
    commentuser = models.CharField(max_length=128)
    comment = models.CharField(max_length=1024)
    createdate = models.DateTimeField(auto_now_add=True)
   
    
class Watchcard(models.Model):
    user = models.CharField(max_length=128)
    cardid = models.IntegerField()
    createdate = models.DateTimeField(auto_now_add=True)
    

