from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# main table to list on active listings
class Listings(models.Model):
    item_name = models.CharField(max_length=64)
    item_description = models.CharField(max_length=6400)
    item_start_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_image_url = models.URLField(max_length=200)
    item_category = models.CharField(max_length=200)

