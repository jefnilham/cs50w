from re import U
from django.contrib.auth.models import AbstractUser
from django.db import models
from numpy import datetime_data
from pytz import timezone

# superuser 'jefnilham, masterchief'

class User(AbstractUser):
    pass

class Auction(models.Model):
    item_name = models.CharField(max_length=64)
    item_description = models.CharField(max_length=640)
    item_starting_bid = models.IntegerField()
    item_image_url = models.URLField(max_length=200)
    #item_listed_timestamp = models.DateTimeField(auto_now_add=True)
    item_listed_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Bid(models.Model):
    bid_price = models.IntegerField()
    #bid_created_timestamp = models.DateTimeField(auto_now_add=True)
    bid_created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    comments = models.CharField(max_length=640)
    #comment_created_timestamp = models.DateTimeField(auto_now_add=True)
    comment_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
