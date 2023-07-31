from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    listing_items_added_to_watchlist = models.ManyToManyField('Listing', related_name='watchlist_users')
    pass

class Listing(models.Model):
    listing_name = models.CharField(max_length=200)
    listing_description = models.CharField(max_length=1000)
    listing_price = models.IntegerField()
    listing_category = models.CharField(max_length=200)
    listing_image_url = models.URLField()
    listing_created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.listing_name

class Bidding(models.Model):
    listings_name = models.ForeignKey(Listing, on_delete=models.CASCADE)
    new_bid = models.IntegerField(null=True)
    bid_created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    #bid_replaced_price = models.BooleanField(default=False)
    def __unicode__(self): 
        return self.bid_amount
    
class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    listings = models.ForeignKey(Listing,null=True, on_delete=models.CASCADE)
    new_comment_text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=datetime.now)
    