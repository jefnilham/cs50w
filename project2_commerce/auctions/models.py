from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    listing_name = models.CharField(max_length=200)
    listing_description = models.CharField(max_length=1000)
    listing_price = models.IntegerField()
    listing_category = models.CharField(max_length=200)
    def __str__(self):
        return self.listing_name

class Bidding(models.Model):
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    def __unicode__(self): 
        return self.bid_amount
    
class Comment(models.Model):
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE)
    new_comment_text = models.CharField(max_length=1000)
    def __str__(self):
        return self.new_comment_text
    
class Watchlist(models.Model):
    watchlist_listings = models.ForeignKey(Listing, on_delete=models.CASCADE)
