from unicodedata import name
from . import views
from django.urls import path


urlpatterns = [
    path("" , views.index ,name="index"),
    path("ujjval",views.ujjval, name="ujjval"),
    path("<str:name>", views.greet, name="greet"),
]