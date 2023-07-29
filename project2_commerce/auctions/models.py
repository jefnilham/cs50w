from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    any_listings_saved_to_watchlist = models.BooleanField()
    pass

class Listing(models.Model):
    listing_name = models.CharField(max_length=200)
    listing_description = models.CharField(max_length=1000)
    listing_watchlisters = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.listing_name

class Bidding(models.Model):
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.IntegerField(max_length=200)
    def __str__(self): 
        return self.bid_amount, self.listings
    
class Comment(models.Model):
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    #item_has_comment = models.BooleanField()
    def __str__(self):
        return self.comment_text, self.listings