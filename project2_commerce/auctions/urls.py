from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("clicked_listing/<int:id>/", views.clicked_listing, name="clicked_listing"),
    path("categories/", views.categories, name="categories"),
    path("clicked_categories/<str:listing_category>/", views.clicked_categories, name="clicked_categories"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path('add_to_watchlist/<int:id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path("my_listings/", views.my_listings, name="my_listings"),
    #path("my_bids/", views.my_bids, name="my_bids")    
]
