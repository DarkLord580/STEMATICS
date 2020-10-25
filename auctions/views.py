from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from auctions.models import *
from django.contrib.admin.templatetags.admin_list import items_for_result
from django.utils.timezone import now



def index(request):
    #print("####################################")
    #print ("         request index ")
    #print("####################################")
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    items = Item.objects.filter(closed=False)
    watched = 0
    watchitemids = Watchitem.objects.filter(user=request.user.username).order_by("-createdate").values_list('itemid',flat=True)
    if watchitemids:
        watched = len(watchitemids)
    
    return render(request, "auctions/index.html", {"items": items, "is_seller": is_seller, "watched":watched})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
            login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    


def viewitems(request):
    #print("####################################")
    #print ("         request viewitems")
    #print("####################################")
    items = Item.objects.all()
    items = Item.objects.filter(closed=False)
    watched = 0
    watchitemids = Watchitem.objects.filter(user=request.user.username).order_by("-createdate").values_list('itemid',flat=True)
    if watchitemids:
        watched = len(watchitemids)
    
    
    return render(request, "auctions/index.html", {"items": items, "noitem": noitem })


def viewitem(request, itemid):
    #print("####################################")
    #print ("         request viewitem")
    #print("####################################")
    
    item = Item.objects.get(id=itemid)
    
    newbid = item.currentbid
    bidmessage=""
    if request.method == "POST":
        
        postnewbid= request.POST.get("currentbid")
        postnewcomment = request.POST.get("comment")
        
        if postnewbid is not None and postnewbid.isnumeric():
            newbid = int(postnewbid)
            if item.currentbid < newbid:
                item.currentbid = newbid
                item.maxbider = request.user.username
                item.save()
            
            bid = Bid.objects.filter(itemid=itemid,biduser=request.user.username)
            if bid:
                bid.delete()
            bid = Bid()
            bid.biduser = request.user.username
            bid.itemid = itemid
            bid.bid = newbid
            bid.save()
        if postnewcomment is not None:
            comment = Comment()
            comment.comment = postnewcomment
            comment.commentuser = request.user.username
            comment.itemid = itemid
            comment.save()
            
            
    bids = Bid.objects.filter(itemid= itemid)
    if bids is not None and len(bids) > 1:
        bidcount = len(bids)
        bidmessage = "<strong>{bidcount} </strong> bid(s) so far.".format(bidcount=bidcount)
    if item.maxbider == request.user.username:
        if item.closed:
            bidmessage = "{bidmessage} You're the winner of bids.".format(bidmessage=bidmessage)
        else:
            bidmessage = "{bidmessage} Your bid is the current bid.".format(bidmessage=bidmessage)
        
    else:
        if item.closed:
            bidmessage = "{bidmessage} The list is closed.".format(bidmessage=bidmessage)
    
    
    comments = Comment.objects.filter(itemid=itemid).order_by("-createdate")
    
    watchitem = Watchitem.objects.filter(user=request.user.username, itemid= itemid)
    watching = False
    if watchitem:
        watching = True
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    watched = 0
    watchitemids = Watchitem.objects.filter(user=request.user.username).order_by("-createdate").values_list('itemid',flat=True)
    if watchitemids:
        watched = len(watchitemids)
    
    currentbid = newbid + 1
    return render(request, "auctions/viewitem.html", {"item": item
            ,"watching": watching, "currentbid":currentbid
            ,"bidmessage":bidmessage, "comments": comments, "is_seller": is_seller, "watched":watched})



@login_required(login_url='/login')
def newitem(request):
    #print("####################################")
    #print ("         request newitem")
    #print("####################################")
    
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    
    if request.method == "POST":
        form = NewItemForm(request.POST)
        print("####################################")
        print (form)
        print("####################################")
        if form.is_valid():
            form.owner =request.user.username
            form.save()
        return HttpResponseRedirect(reverse("index"))
    else: 
        categories=Category.objects.all()
        return render(request,"auctions/newitem.html", {"categories": categories, "is_seller": is_seller}) 
    

def category(request , categoryid):
    #print("####################################")
    #print ("         request category")
    #print("####################################")
    categories=Category.objects.all()
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    items = Item.objects.filter(closed=False)
    watched = 0
    watchitemids = Watchitem.objects.filter(user=request.user.username).order_by("-createdate").values_list('itemid',flat=True)
    if watchitemids:
        watched = len(watchitemids)
    
    if categoryid == 0:
        totalcategory = True
        return render(request, "auctions/category.html", {"totalcategory": totalcategory, "categories": categories, "watched":watched})    
    else:
        totalcategory = False
        itemcategories = Category.objects.filter(id=categoryid).values_list('category',flat=True)
        
        items = Item.objects.filter(category__in=itemcategories, closed= False)
        return render(request, "auctions/category.html", {"totalcategory": totalcategory, 
                "categories": categories, "category": itemcategories[0], "items": items, "is_seller": is_seller, "watched":watched})
       
@login_required(login_url='/login')
def watchlist(request):
    #print("####################################")
    #print ("         request watchlist")
    #print("####################################")
    
    watchitemids = Watchitem.objects.filter(user=request.user.username).order_by("-createdate").values_list('itemid',flat=True)
    
    watched = 0
    if watchitemids:
        watched = len(watchitemids)
    items = Item.objects.filter(id__in=watchitemids)
    
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    
    return render(request, "auctions/watchlist.html", {"items": items , "is_seller": is_seller, "watched":watched})        


@login_required(login_url='/login')
def addwatchlist(request, itemid):

    watchitems = Watchitem.objects.filter(
        itemid=itemid, user=request.user.username)
    if watchitems:
            watchitems.delete()
    else:
        watch = Watchitem()
        watch.user = request.user.username
        watch.itemid = itemid
        watch.save()
    return HttpResponseRedirect(reverse("viewitem", kwargs={'itemid': itemid}))


@login_required(login_url='/login')
def deletecomment(request, commentid):
    comment = Comment.objects.get(id=commentid, commentuser=request.user.username)
    itemid = comment.itemid
    
    if comment:
        comment.delete()
        
    return HttpResponseRedirect(reverse("viewitem", kwargs={'itemid': itemid}))

@login_required(login_url='/login')    
def closedlists(request):
    #print("####################################")
    #print ("         request closedlists")
    #print("####################################")
    
    
    items = Item.objects.filter(closed=True)
    is_seller= 'Seller' in request.user.groups.values_list('name', flat=True)
    
    return render(request, "auctions/closedlist.html", {"items": items, "is_seller": is_seller})        
        
        

@login_required(login_url='/login')    
def closedlist(request , itemid):
    #print("####################################")
    #print ("         request closedlist ")
    #print("####################################")
    
    item = Item.objects.get(id=itemid)
    if item is not None and item.closed == False:
        item.closed= True
        item.save()

     
    return HttpResponseRedirect(reverse("viewitem", kwargs={'itemid': itemid}))

    
    

