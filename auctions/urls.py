from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<str:catname>", views.category, name="category"),
    path("listing/<str:listname>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add-new-listing", views.add_new, name="add_new"),
]
