from django.contrib import admin
from .models import Listings, Biddings, Comments
# Register your models here.

admin.site.register(Listings)
admin.site.register(Biddings)
admin.site.register(Comments)
