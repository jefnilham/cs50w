from django import forms
from .models import Listing

class CreateNewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["listing_name", "listing_description", "listing_price", "listing_category", "listing_image_url"]
