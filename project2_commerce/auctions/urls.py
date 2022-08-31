from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<str:item_name>", views.listing_page, name="listing_page"),
    path("category_page", views.category_page, name="category_page"),
    path("category_page_clicked/<str:item_category>", views.category_page_clicked, name="category_page_clicked"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
]
