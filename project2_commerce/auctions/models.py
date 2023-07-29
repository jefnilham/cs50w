from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    listing_name = models.CharField(max_length=200)
    def __str__(self):
        return self.listing_name

class Biddings(models.Model):
    listings = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid_amount = models.IntegerField(max_length=200)
    item_has_bid = models.BooleanField()
    def __str__(self): 
        return self.bid_amount
    
class Comments(models.Model):
    listings = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    item_has_comment = models.BooleanField()
    def __str__(self):
        return self.comment_text