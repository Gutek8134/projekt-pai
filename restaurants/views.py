from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RestaurantForm
from .models import Restaurant


# Create your views here.
def restaurant_list(request: HttpRequest):
    restaurants = Restaurant.objects.all().order_by("name")
    return render(
        request, "restaurants/restaurant_list.html", {
            "restaurants": restaurants}
    )


def add_restaurant(request: HttpRequest):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect("restaurants:restaurant_list")

    form = RestaurantForm()

    return render(
        request,
        "restaurants/restaurant_form.html",
        {
            "form": form,
            "title": "Add Restaurant",
            "submit_text": "Save restaurant",
        },
    )


def edit_restaurant(request: HttpRequest, pk: int):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect("restaurants:restaurant_list")

    form = RestaurantForm(instance=restaurant)

    return render(
        request,
        "restaurants/restaurant_form.html",
        {
            "form": form,
            "title": "Edit Restaurant",
            "submit_text": "Save changes",
        },
    )


def delete_restaurant(request: HttpRequest, pk: int):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if request.method == "POST":
        restaurant.delete()
        return redirect("restaurants:restaurant_list")

    return render(
        request,
        "restaurants/confirm_delete_restaurant.html",
        {"restaurant": restaurant},
    )
