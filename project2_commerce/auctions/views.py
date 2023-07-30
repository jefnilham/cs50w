from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateNewListing

from .models import User, Listing, Bidding, Comment, Watchlist


def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"all_listings":all_listings})


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

def create(request):
    if request.method == 'POST':
        form = CreateNewListing(request.POST)
        if form.is_valid():
            listing_name = form.cleaned_data["listing_name"]
            listing_description = form.cleaned_data["listing_description"]
            listing_price = form.cleaned_data["listing_price"]
            listing_category = form.cleaned_data["listing_category"]                    
            listing_created = Listing(listing_name=listing_name,
                                      listing_description=listing_description,
                                      listing_price=listing_price,
                                      listing_category=listing_category)
            listing_created.save()
            return HttpResponseRedirect("/%i" %listing_created.id)
    else:
        form = CreateNewListing()
    return render(request, "auctions/create.html", {"form":form})

def clicked_listing(request, id):
    clicked_listing = Listing.objects.get(id=id)
    return render(request, "auctions/clicked_listing.html", {"clicked_listing":clicked_listing})