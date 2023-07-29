from cgitb import text
from secrets import choice
from tkinter import FLAT
from turtle import textinput
from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Comment
from django import forms
import datetime
from django.core.files.storage import default_storage




# category choices for CreateListingForm
listing_item_category_list = [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('no category', 'No Category')
    ]

# form to take inputs at create_listing page 
class CreateListingForm(forms.Form):
    listing_item_name = forms.CharField(label="Listing item name", widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_item_description = forms.CharField(label="Listing item description", widget=forms.Textarea(attrs={'class':'form-control', 'rows':'3'}))
    listing_item_start_price = forms.DecimalField(label="Listing item start price", max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_item_image_url = forms.URLField(label="Listing item image URL", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_item_category = forms.CharField(label="Listing item category", widget=forms.Select(choices=listing_item_category_list, attrs={'class':'form-control'}))

# form to create comment. still add on to main Listing model
class CreateComment(forms.Form):
    comment_body = forms.CharField(label="Add a comment", widget=forms.Textarea(attrs={'class':'form-control', 'rows':'3'}))




def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

# Users can create a new listing on this page 
def create_listing(request):

    # "GET /create_listing HTTP/1.1" 200 
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm(),
        })

    # take user input to backend once form submit i.e. POST /create_listing HTTP/1.1
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        # get datetime of listing created
        listing_item_datetime = datetime.datetime.now()
        
        if form.is_valid():

            # data normalisation from form
            listing_item_name = form.cleaned_data['listing_item_name']
            listing_item_description = form.cleaned_data['listing_item_description']
            listing_item_start_price = form.cleaned_data['listing_item_start_price']
            listing_item_image_url = form.cleaned_data['listing_item_image_url']
            listing_item_category = form.cleaned_data['listing_item_category']

        # additional data for active listings (user posted and date of post)
        listing_item_username = request.user.username
        #listing_item_datetime = datetime.datetime.strptime(request.POST['time'], '%H:%M:%S').time()

        # saving data into Listing model
        listing_created = Listing(
            item_name = listing_item_name,
            item_description = listing_item_description,
            item_start_price = listing_item_start_price,
            item_image_url = listing_item_image_url,
            item_category = listing_item_category,
            item_username = listing_item_username,
            item_datetime = listing_item_datetime,
            )

        listing_created.save()
        print("-------------------------------------------------->",listing_created.id)
    # return to index page after submit form
    return HttpResponseRedirect(reverse("index"))


# listing_page
def listing_page(request, item_name):

    # get id of item_name from db matching clicked from index page
    clicked_listing_id = Listing.objects.get(item_name=item_name).id
    clicked_listing_data = Listing.objects.filter(id=clicked_listing_id).values()

    # get comments model data to display
    comments = Comment.objects.all()

    # redirect to same page when add comment
    if request.method == "POST":
        form = CreateComment(request.POST)
        comment_datetime = datetime.datetime.now()
        comment_username = request.user.username
        if form.is_valid():
            comment_body = form.cleaned_data['comment_body']

        # add comment data to model
        comment_created = Comment(
            comment_body = comment_body,
            comment_datetime = comment_datetime,
            comment_username = comment_username,
            comment_listing =  Listing.objects.get(item_name=item_name),
        )

        # save comments
        comment_created.save()


    return render(request, "auctions/listing_page.html", {
        "listings": clicked_listing_data,
        "form": CreateComment(),
        "comments": comments
    })



# page to only show all listings categories
def category_page(request):

    # get unique item category to display on category page
    listings = Listing.objects.all().values('item_category').distinct()

    # display list of categories if nothing
    return render(request, "auctions/category_page.html", {
        "listings": listings,
    })
# page after a category is clicked from category_page
def category_page_clicked(request, item_category):

    print("OIIIIIIIIIIIIIIIIIIIII", item_category)

    # filter to item_category clicked
    clicked_listing_data = Listing.objects.filter(item_category=item_category).values()

    return render(request, "auctions/category_page_clicked.html", {
        "listings": clicked_listing_data,
    })



# user clicks add to watchlist button
def add_to_watchlist(request):

    # get user who clicked 
    username = User.objects.get(username=request.user.username)
    source_address = (request.META.get('HTTP_REFERER'))
    item_name = (str(source_address)).split('/')[-1]
    print(item_name)
    listings = Listing.objects.get(item_name=item_name)

    print('Added user {} to watchlist for item: {}'.format(username, listings))
    print('Current watchlist: ', listings.users_watching.all())

    return HttpResponseRedirect(source_address)




'''
# watchlist page. users come from clicking watchlist button on listing_page
def watchlist_page(request, item_name):

    # get id of clicked item from item_name e.g "home"
    clicked_listing_id = Listing.objects.get(item_name=item_name).id    

    # create list for watched items, each elem is an item_name from Listing
    watchlist_list = []
    watchlist_list.append(item_name)

    # remove duplicates
    watchlist_list = list(dict.fromkeys(watchlist_list))
    print(watchlist_list)

    # get unique item category to display on category page
    clicked_listing_id = Listing.objects.get(item_name=item_name).id    
    clicked_listing_data = Listing.objects.filter(id=clicked_listing_id).values()


    # display list of categories if nothing
    return render(request, "auctions/watchlist_page.html", {
        "listings": clicked_listing_data,
    })


'''