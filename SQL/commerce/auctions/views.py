from dataclasses import fields
from pyexpat import model
from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','bid_start','category','image_url']
def index(request):
    # if request.user.is_authenticatied():
    return render(request, "auctions/index.html",{
        "listing" : Listing.objects.all()
    })    
    # return render(request, "auctions/index.html")


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

def categories(request):
    return render(request,"auctions/categories.html")

def watchlist(request):
    return render(request,"auctions/watchlist.html")

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
        return render(request,"auctions/index.html",{
            "listing":listing
        })
    else:
        return render(request,"auctions/create_listing.html")
def list_page(request,list_id):
    
    item = Listing.objects.get(id = list_id)
    return render(request,"auctions/list_page.html",{
        "product":item
    })