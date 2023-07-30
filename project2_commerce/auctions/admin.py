from django.contrib import admin
from .models import User, Listing, Bidding, Comment, Watchlist, Category
# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bidding)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Category)
