from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from flashcards.models import *
from django.contrib.admin.templatetags.admin_list import items_for_result
from django.utils.timezone import now



def index(request):
    #print("####################################")
    #print ("         request index ")
    #print("####################################")
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    cards = card.objects.filter(closed=False)
    watched = 0
    watchcardids = Watchcard.objects.filter(user=request.user.username).order_by("-createdate").values_list('cardid',flat=True)
    if watchcardids:
        watched = len(watchcardids)
    
    return render(request, "flashcards/index.html", {"cards": cards, "is_seller": is_seller, "watched":watched})


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
            return render(request, "flashcards/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "flashcards/login.html")


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
            return render(request, "flashcards/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "flashcards/register.html", {
                "message": "Username already taken."
            })
            login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flashcards/register.html")
    
    


def viewcards(request):
    #print("####################################")
    #print ("         request viewcards")
    #print("####################################")
    cards = card.objects.all()
    cards = card.objects.filter(closed=False)
    watched = 0
    watchcardids = Watchcard.objects.filter(user=request.user.username).order_by("-createdate").values_list('cardid',flat=True)
    if watchcardids:
        watched = len(watchcardids)
    
    
    return render(request, "flashcards/index.html", {"cards": cards, "nocard": nocard })


def viewcard(request, cardid):
    #print("####################################")
    #print ("         request viewcard")
    #print("####################################")
    
    card = card.objects.get(id=cardid)
    
    newbid = card.currentbid
    bidmessage=""
    if request.method == "POST":
        
        postnewbid= request.POST.get("currentbid")
        postnewcomment = request.POST.get("comment")
        
        if postnewbid is not None and postnewbid.isnumeric():
            newbid = int(postnewbid)
            if card.currentbid < newbid:
                card.currentbid = newbid
                card.maxbider = request.user.username
                card.save()
            
            bid = Bid.objects.filter(cardid=cardid,biduser=request.user.username)
            if bid:
                bid.delete()
            bid = Bid()
            bid.biduser = request.user.username
            bid.cardid = cardid
            bid.bid = newbid
            bid.save()
        if postnewcomment is not None:
            comment = Comment()
            comment.comment = postnewcomment
            comment.commentuser = request.user.username
            comment.cardid = cardid
            comment.save()
            
            
    bids = Bid.objects.filter(cardid= cardid)
    if bids is not None and len(bids) > 1:
        bidcount = len(bids)
        bidmessage = "<strong>{bidcount} </strong> bid(s) so far.".format(bidcount=bidcount)
    if card.maxbider == request.user.username:
        if card.closed:
            bidmessage = "{bidmessage} You're the winner of bids.".format(bidmessage=bidmessage)
        else:
            bidmessage = "{bidmessage} Your bid is the current bid.".format(bidmessage=bidmessage)
        
    else:
        if card.closed:
            bidmessage = "{bidmessage} The list is closed.".format(bidmessage=bidmessage)
    
    
    comments = Comment.objects.filter(cardid=cardid).order_by("-createdate")
    
    watchcard = Watchcard.objects.filter(user=request.user.username, cardid= cardid)
    watching = False
    if watchcard:
        watching = True
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    watched = 0
    watchcardids = Watchcard.objects.filter(user=request.user.username).order_by("-createdate").values_list('cardid',flat=True)
    if watchcardids:
        watched = len(watchcardids)
    
    currentbid = newbid + 1
    return render(request, "flashcards/viewcard.html", {"card": card
            ,"watching": watching, "currentbid":currentbid
            ,"bidmessage":bidmessage, "comments": comments, "is_seller": is_seller, "watched":watched})



@login_required(login_url='/login')
def newcard(request):
    #print("####################################")
    #print ("         request newcard")
    #print("####################################")
    
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    
    if request.method == "POST":
        form = NewcardForm(request.POST)
        print("####################################")
        print (form)
        print("####################################")
        if form.is_valid():
            form.owner =request.user.username
            form.save()
        return HttpResponseRedirect(reverse("index"))
    else: 
        categories=Category.objects.all()
        return render(request,"flashcards/newcard.html", {"categories": categories, "is_seller": is_seller}) 
    

def category(request , categoryid):
    #print("####################################")
    #print ("         request category")
    #print("####################################")
    categories=Category.objects.all()
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    cards = card.objects.filter(closed=False)
    watched = 0
    watchcardids = Watchcard.objects.filter(user=request.user.username).order_by("-createdate").values_list('cardid',flat=True)
    if watchcardids:
        watched = len(watchcardids)
    
    if categoryid == 0:
        totalcategory = True
        return render(request, "flashcards/category.html", {"totalcategory": totalcategory, "categories": categories, "watched":watched})    
    else:
        totalcategory = False
        cardcategories = Category.objects.filter(id=categoryid).values_list('category',flat=True)
        
        cards = card.objects.filter(category__in=cardcategories, closed= False)
        return render(request, "flashcards/category.html", {"totalcategory": totalcategory, 
                "categories": categories, "category": cardcategories[0], "cards": cards, "is_seller": is_seller, "watched":watched})
       
@login_required(login_url='/login')
def watchlist(request):
    #print("####################################")
    #print ("         request watchlist")
    #print("####################################")
    
    watchcardids = Watchcard.objects.filter(user=request.user.username).order_by("-createdate").values_list('cardid',flat=True)
    
    watched = 0
    if watchcardids:
        watched = len(watchcardids)
    cards = card.objects.filter(id__in=watchcardids)
    
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    
    return render(request, "flashcards/watchlist.html", {"cards": cards , "is_seller": is_seller, "watched":watched})        


@login_required(login_url='/login')
def addwatchlist(request, cardid):

    watchcards = Watchcard.objects.filter(
        cardid=cardid, user=request.user.username)
    if watchcards:
            watchcards.delete()
    else:
        watch = Watchcard()
        watch.user = request.user.username
        watch.cardid = cardid
        watch.save()
    return HttpResponseRedirect(reverse("viewcard", kwargs={'cardid': cardid}))


@login_required(login_url='/login')
def deletecomment(request, commentid):
    comment = Comment.objects.get(id=commentid, commentuser=request.user.username)
    cardid = comment.cardid
    
    if comment:
        comment.delete()
        
    return HttpResponseRedirect(reverse("viewcard", kwargs={'cardid': cardid}))

@login_required(login_url='/login')    
def closedlists(request):
    #print("####################################")
    #print ("         request closedlists")
    #print("####################################")
    
    
    cards = card.objects.filter(closed=True)
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    
    return render(request, "flashcards/closedlist.html", {"cards": cards, "is_seller": is_seller})        
        
        

@login_required(login_url='/login')    
def closedlist(request , cardid):
    #print("####################################")
    #print ("         request closedlist ")
    #print("####################################")
    
    card = card.objects.get(id=cardid)
    if card is not None and card.closed == False:
        card.closed= True
        card.save()

     
    return HttpResponseRedirect(reverse("viewcard", kwargs={'cardid': cardid}))

    
    

