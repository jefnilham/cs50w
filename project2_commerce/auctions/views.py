from secrets import choice
from turtle import textinput
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User
from django import forms
import datetime

# category choices for CreateListingForm
listing_item_category_list = [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ('nil', 'NIL')
    ]

# form to take inputs at create_listing page 
class CreateListingForm(forms.Form):
    listing_item_name = forms.CharField(label="Listing item name", widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_item_description = forms.CharField(label="Listing item description", widget=forms.Textarea(attrs={'class':'form-control', 'rows':'3'}))
    listing_item_start_price = forms.DecimalField(label="Listing item start price", max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_item_image_url = forms.URLField(label="Listing item image URL", max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_item_category = forms.CharField(label="Listing item category", widget=forms.Select(choices=listing_item_category_list, attrs={'class':'form-control'}))
    

def index(request):
    return render(request, "auctions/index.html")


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
        
        if form.is_valid():

            # data normalisation from form
            listing_item_name = form.cleaned_data['listing_item_name']
            listing_item_description = form.cleaned_data['listing_item_description']
            listing_item_start_price = form.cleaned_data['listing_item_start_price']
            listing_item_image_url = form.cleaned_data['listing_item_image_url']
            listing_item_category = form.cleaned_data['listing_item_category']

            # additional data for active listings (user posted and date of post)
            username = request.user.username
            listing_item_datetime = datetime.datetime.strptime(request.POST['time'], '%H:%M:%S').time()


