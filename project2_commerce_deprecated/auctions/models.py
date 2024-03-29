from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# main table to list on active listings
class Listing(models.Model):
    item_name = models.CharField(max_length=64)
    item_description = models.CharField(max_length=6400)
    item_start_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_image_url = models.URLField(max_length=200)
    item_category = models.CharField(max_length=200)
    
    # get from username
    item_username = models.CharField(max_length=64)

    # get datetime of post
    item_datetime = models.DateTimeField(max_length=64)

    # watchlist boolean
    users_watching = models.ManyToManyField(User, blank=True, related_name="watching")


# to log comments
class Comment(models.Model):
    comment_body = models.CharField(max_length=6400)
    comment_datetime = models.DateTimeField(max_length=64)
    comment_username = models.CharField(max_length=64)
    
    # link to Listing
    comment_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)