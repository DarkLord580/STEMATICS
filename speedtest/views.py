from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from speedtest.models import *
from django.contrib.admin.templatetags.admin_list import items_for_result
from django.utils.timezone import now
from django.core import serializers
import json
from .models import *
import random
from speedtest.models import TestString
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




def index(request):
    print("####################################")
    print ("         request index ")
    print("####################################")
    return render(request, "index.html")

def getstring(request):
    stringA = TestString.objects.all()
    string = stringA[int(random.uniform(0, len(stringA)))]
    string = string.string  
    stringArray = string.split()
    return JsonResponse({"message": "Done","status":201, "strArr": stringArray})


def typing(request):
    stringA = TestString.objects.all()
    string = stringA[int(random.uniform(0, len(stringA)))]
    string = string.string  
    stringArray = string.split()
    print(stringArray)
    list = []
    for i in range(0,len(stringArray)):
        list.append(i)
    zipped_list = zip(list, stringArray)
    
    return render(request, "typing.html" , {"list": zipped_list, "string" : string})


#def savescore(request):
 #   data = json.loads(request.body)
  #  wpm = data.score
  #  scoresaver = Score(wpm = int(wpm))
   # scoresaver.save()
    #return JsonResponse({"message": "Done","status":201})


def login_view(request):
    #print("####################################")
    #print ("         request log_in ")
    #print("####################################")
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    #print("####################################")
    #print ("         request log_out ")
    #print("####################################")
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    #print("####################################")
    #print ("         request register")
    #print("####################################")
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
            login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    

@login_required(login_url='/login')
def score(request):
    #print("####################################")
    #print ("         request newcard")
    #print("####################################")
    
    return render(request,"score.html", ) 



@csrf_exempt
@login_required(login_url='/login')
def save(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print("request user ==========",request.user)
    print("request user ==========",type(request.user))
    wordpm = data.get("score")
    scoreboard = Score(
        user = request.user,
        wpm = int(wordpm)
    )   
    scoreboard.save()
    return JsonResponse({"message": "Post created successfully.", "status": 201})

