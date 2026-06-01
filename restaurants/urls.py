import re
from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns=[
    path("", views.restaurant_list, name=views.restaurant_list.__name__),
    path("add/", views.add_restaurant, name=views.add_restaurant.__name__),
    path("edit/<int:pk>", views.edit_restaurant, name=views.edit_restaurant.__name__),
    path("delete/<int:pk>", views.delete_restaurant, name=views.delete_restaurant.__name__),
]
