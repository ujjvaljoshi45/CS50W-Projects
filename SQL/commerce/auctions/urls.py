from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("categories",views.categories, name="categories"),
    path("category/<str:category>",views.category,name="category"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("create_listing",views.create_listing, name="create_listing"),
    path("logout", views.logout_view, name="logout"),
    path("new_bid/<int:list_id>",views.new_bid, name="new_bid"),
    path("list/<int:list_id>",views.list_page,name="list"),
    path("register", views.register, name="register")
]
