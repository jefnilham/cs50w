from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import CreateNewListing, CreateNewComment, CreateNewBid, CloseBid
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
            new_form = form.save(commit=False)
            new_form.listing_created_by = request.user
            new_form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateNewListing()
    return render(request, "auctions/create.html", {"form":form})


def clicked_listing(request, id):
    clicked_listing = Listing.objects.get(id=id)
    comments = Comment.objects.filter(listings=clicked_listing)
    latest_bid = clicked_listing.bidding_set.order_by('-new_bid').first()
    current_user = request.user
    if request.method == "POST":

        # add comments
        comment_form = CreateNewComment(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user  # Assign the current user to the comment
            new_comment.listings = clicked_listing
            new_comment.created_at = timezone.now()
            new_comment.save()
            comment_form = CreateNewComment()
            return HttpResponseRedirect(reverse("clicked_listing", args=[id]))
        
        # add bid
        bid_form = CreateNewBid(request.POST)
        if bid_form.is_valid():
            new_bid = bid_form.cleaned_data['new_bid']
            if latest_bid is None or new_bid > latest_bid.new_bid:
                clicked_listing.listing_price = new_bid
                clicked_listing.listing_bid_by = request.user
                clicked_listing.save()
                new_bid_form = bid_form.save(commit=False)
                new_bid_form.bid_created_by = request.user
                new_bid_form.listings_name = clicked_listing
                new_bid_form.save()
                bid_form = CreateNewBid()
                return HttpResponseRedirect(reverse("clicked_listing", args=[id]))
            else:
                return render(request, 'auctions/error.html', {'message': 'Your bid must be higher than the current bid.'})

        # close bid
        close_bid_form = CloseBid(request.POST, instance=clicked_listing)
        if close_bid_form.is_valid():
            clicked_listing.listing_active = False
            clicked_listing.save()
            return HttpResponseRedirect('/closed_listings/')
        else:
            close_bid_form = CloseBid(instance=clicked_listing)

    else:
        bid_form = CreateNewBid()
        comment_form = CreateNewComment()
        comments = Comment.objects.all()
        close_bid_form = CloseBid()
    return render(request, "auctions/clicked_listing.html", {"comment_form":comment_form,
                                                             "comments":comments,
                                                             "clicked_listing":clicked_listing,
                                                             "bid_form":bid_form,
                                                             "latest_bid":latest_bid,
                                                             "close_bid_form": close_bid_form,
                                                             "current_user":current_user
                                                             })

def categories(request):
    all_listings = Listing.objects.all()
    all_active_listings = Listing.objects.filter(listing_active=True)
    all_active_categories = all_active_listings.values_list('listing_category', flat=True).distinct()
    print(all_active_categories)
    return render(request, "auctions/categories.html", {"all_active_categories":all_active_categories, 
                                                        "all_listings":all_listings,
                                                        "all_active_listings":all_active_listings})


def clicked_categories(request, listing_category):
    all_listings = Listing.objects.all()
    all_categories = Listing.objects.values_list('listing_category', flat=True)
    listings_in_category = Listing.objects.filter(listing_category=listing_category)
    return render(request, "auctions/clicked_categories.html", {"listings_in_category":listings_in_category, 
                                                                "all_listings":all_listings,
                                                                "all_categories":all_categories,
                                                                "listing_category":listing_category})


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


def closed_listings(request):
    all_listings = Listing.objects.all()
    user = request.user
    return render(request, "auctions/closed_listings.html", {"all_listings":all_listings, 
                                                             "user":user})