from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Bid, User, Listing, Comment, Watchlist, Winner


def index(request):
    return render(request, "auctions/index.html", {
        "listing": Listing.objects.all()
    })

def login_view(request):
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
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
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

@login_required(login_url='/login')
def categories(request):
    return render(request, "auctions/categories.html")

@login_required(login_url='/login')
def watchlist(request):
    list = []
    for e in Watchlist.objects.filter(user = request.user.username):
        list.append(Listing.objects.get(id=e.bid_id))

    if list:
        return render(request, "auctions/watchlist.html", {
            "list": list
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "message": "No Watchlist Found!"
        })

@login_required(login_url='/login')
def create_listing(request):
    if request.POST:
        item = Listing()

        item.seller_name = request.user.username
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.category = request.POST.get('category')
        item.bid_start = request.POST.get('bid_start')

        if request.POST.get('image_url'):
            item.image_url = request.POST.get('image_url')
        else:
            item.image_url = "https://www.aust-biosearch.com.au/wp-content/themes/titan/images/noimage.gif"
        item.save()
        listing = Listing.objects.all()
        empty = False
        if len(listing) == 0:
            empty = True
        return render(request, "auctions/index.html", {
            "listing": listing
        })
    else:
        return render(request, "auctions/create_listing.html")

@login_required(login_url='/login')
def list_page(request, list_id):
    item = Listing.objects.get(id=list_id)
    try:
        comments = Comment.objects.filter(bid_id = list_id)
    except:
        comments = None
    try:
        winner = Winner.objects.get(bid_id = list_id)
    except:
        winner = None
    if winner:
        return render(request,"auctions/list_page.html",{
            "product":item,
            "winner" : winner,
            "comments" : comments
        })
    new_bid = 0
    comments = "No comments added!"
    if request.POST:
        new_bid = int(request.POST.get('new_bid'))
    if new_bid > item.bid_start:
        item.bid_start = int(request.POST.get('new_bid'))
        item.save()
        try:
            bid = Bid.objects.get(bid_id = list_id)
        except:
            bid = None
        if bid:
            bid.bid = item.bid_start
            bid.save()
        else:
            bid = Bid()
            bid.user = request.POST.get('username')
            bid.bid_id = list_id
            bid.title = item.title
            bid.bid = item.bid_start
            bid.save()
        return render(request, "auctions/list_page.html", {
            "product": item,
            "comments": comments
        })
    else:
        return render(request, "auctions/list_page.html", {
            "product": item,
            "comments": comments,
            "message": "Enter a valid bid!"
        })

@login_required(login_url='/login')
def category(request, category):
    category_products = Listing.objects.filter(category=category)
    empty = False
    if len(category_products) == 0:
        empty = True

    return render(request, "auctions/category.html", {
        "category": category,
        "empty": empty,
        "products": category_products
    })

@login_required(login_url='/login')
def add_comment(request, list_id):
    item = Listing.objects.get(id=list_id)
    # if Comment.objects.get(bid_id = list_id):
    #     return list_page(request,list_id)
    comment = Comment()
    if request.POST:
        comment.user = request.POST.get('username')
        comment.commet = request.POST.get('comment')
        comment.bid_id = list_id
        comment.save()
        return render(request, "auctions/list_page.html", {
            "product": Listing.objects.get(id=list_id),
            "comments": Comment.objects.all()
        })
    return render(request, "auctions/list_page.html", {
        "product": Listing.objects.get(id=list_id)
    })

@login_required(login_url='/login')
def add_watchlist(request, list_id):
    entry = Watchlist.objects.filter(
        bid_id=list_id, user=request.user.username)
    if entry:
        Watchlist.objects.filter(bid_id=list_id).delete()

    else:
        entry = Watchlist()
        entry.user = request.user.username
        entry.bid_id = list_id
        entry.save()
    list = []
    for e in Watchlist.objects.all():
        list.append(Listing.objects.get(id=e.bid_id))

    if list:
        return render(request, "auctions/watchlist.html", {
            "list": list
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "message": "No Watchlist Found!"
        })

@login_required(login_url='/login')
def close_bid(request,list_id):
    winner = Winner()
    try:
        already_there = Winner.objects.filter(bid_id = list_id)
    except:
        return list_id(request,list_id)
    item = Listing.objects.get(id = list_id)
    winner.title = item.title
    winner.bid_id = list_id
    winner.owner = item.seller_name
    try:
        winne_name = Bid.objects.get(bid_id = list_id).user 
    except:
        winne_name = item.seller_name
    winner.winner = winne_name
    winner.final_prize = item.bid_start
    winner.save()
    return render(request,"auctions/list_page.html",{
        "product":item,
        "winner" :Winner.objects.get(bid_id = list_id)
    })