from django import forms
from .models import Listing, Comment, Bidding

class CreateNewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["listing_name", "listing_description", "listing_price", "listing_category", "listing_image_url"]

class CreateNewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["new_comment_text", "created_at"] 

class CreateNewBid(forms.ModelForm):
    class Meta:
        model = Bidding
        fields = ["new_bid"]

class CloseBid(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["listing_active"]

