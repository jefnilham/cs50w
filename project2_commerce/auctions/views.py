from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import CreateNewListing, CreateNewComment
from .models import User, Listing, Bidding, Comment
from django.utils import timezone


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
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateNewListing()
    return render(request, "auctions/create.html", {"form":form})


def clicked_listing(request, id):
    clicked_listing = Listing.objects.get(id=id)
    #listing = get_object_or_404(Listing, id=id)
    if request.method == "POST":
        comment_form = CreateNewComment(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user  # Assign the current user to the comment
            new_comment.clicked_listing = clicked_listing
            new_comment.created_at = timezone.now()
            new_comment.save()
            comment_form = CreateNewComment()
            return HttpResponseRedirect(reverse("clicked_listing", id=id))
    else:
        comment_form = CreateNewComment()
        comments = Comment.objects.all()
    return render(request, "auctions/clicked_listing.html", {"comment_form":comment_form,
                                                             "comments":comments,
                                                             "clicked_listing":clicked_listing,
                                                             "clicked_listing":clicked_listing
                                                             })

def categories(request):
    all_categories = Listing.objects.values('listing_category').distinct()
    return render(request, "auctions/categories.html", {"all_categories":all_categories})


def clicked_categories(request, listing_category):
    listing_category = Listing.objects.filter(listing_category=listing_category)
    return render(request, "auctions/clicked_categories.html", {"listing_category":listing_category})


def watchlist(request):
    user = User.objects.get(username=request.user.username)
    watchlisted_items = user.listing_items_added_to_watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlisted_items":watchlisted_items})


def add_to_watchlist(request, id):
    if request.method == 'POST':
        item = Listing.objects.get(pk=id)
        user = User.objects.get(username=request.user.username)
        user.listing_items_added_to_watchlist.add(item)
        watchlisted_items = user.listing_items_added_to_watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlisted_items":watchlisted_items})


def remove_from_watchlist(request, id):
    if request.method == 'POST':
        item = Listing.objects.get(pk=id)
        user = User.objects.get(username=request.user.username)
        user.listing_items_added_to_watchlist.remove(item)
        watchlisted_items = user.listing_items_added_to_watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlisted_items":watchlisted_items})

'''
def add_comment(request):
    listing = get_object_or_404(Listing, id=id)
    if request.method == "POST":
        comment_form = CreateNewComment(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save()
            new_comment.listings = listing
            new_comment.save()
            return HttpResponseRedirect(reverse("clicked_listing", id=id))
    else:
        comment_form = CreateNewComment()
        comments = Comment.objects.filter(listings=listing)
    return render(request, "auctions/clicked_listing.html", {"comment_form":comment_form,
                                                             "listing":listing,
                                                             "comments":comments})
'''
