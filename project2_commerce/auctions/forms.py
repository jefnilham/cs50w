from django import forms

class CreateNewListing(forms.Form):
    listing_name = forms.CharField(label="Listing Name", max_length=200)
    listing_description = forms.CharField(label="Listing Description", max_length=1000)
    listing_price = forms.IntegerField(label="Price")
    listing_category = forms.CharField(label="Category", max_length=200)