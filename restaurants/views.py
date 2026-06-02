from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, FloatField
from django.db.models.functions import Power, Sqrt, Radians, Sin, Cos, ATan2

from .forms import RestaurantForm, RestaurantFilterForm
from .models import Restaurant, RestaurantMenuType

from math import radians, cos

RADIUS = 6371
USER_LATITUDE = 52.40692
USER_LONGDITUDE = 16.92993

# Create your views here.


def restaurant_list(request: HttpRequest):
    restaurants = Restaurant.objects.all()
    menu_types: list[str] = list(
        RestaurantMenuType.objects.values_list("menu_type", flat=True))

    restaurant_name = ""
    max_distance = ""

    if request.method == "GET":
        filter_form = RestaurantFilterForm(request.GET)
        if "name" in request.GET:
            restaurant_name = request.GET["name"]
            restaurants = restaurants.filter(name__icontains=restaurant_name)\
                .annotate(distance_latitude_r=Radians(F("latitude")-USER_LATITUDE, output_field=FloatField()), distance_longditude_r=Radians(F("longditude")-USER_LONGDITUDE, output_field=FloatField()))\
                .annotate(a=Power(Sin(F("distance_latitude_r")/2), 2, output_field=FloatField()) +
                          cos(radians(USER_LATITUDE))*Cos(Radians(F("latitude")), output_field=FloatField()) *
                          Power(Sin(F("distance_longditude_r")/2), 2, output_field=FloatField()))\
                .annotate(c=2*ATan2(Sqrt(F("a")), Sqrt(1-F("a")), output_field=FloatField()))\
                .annotate(distance=RADIUS*F("c"))

        if "max_distance" in request.GET and request.GET["max_distance"].replace(".", "", 1).isdigit():
            try:
                max_distance = float(request.GET["max_distance"])
                restaurants = restaurants\
                    .filter(distance__lte=max_distance)
            except ValueError as e:
                print(e)

        if "menu_types" in request.GET:
            restaurants = restaurants.filter(
                menu_type__in=request.GET["menu_types"])

    else:
        filter_form = RestaurantFilterForm()

    restaurants.order_by("name")
    return render(
        request, "restaurants/restaurant_list.html", {
            "restaurants": restaurants,
            "form": filter_form,
            "user_position": (USER_LATITUDE, USER_LONGDITUDE), }
    )


def add_restaurant(request: HttpRequest):
    if request.method == "POST":
        form = RestaurantForm(request.POST, request.FILES)
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            return redirect("restaurants:restaurant_list")
    else:
        form = RestaurantForm()

    return render(
        request,
        "restaurants/restaurant_add_form.html",
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

    else:
        form = RestaurantForm(instance=restaurant)

    return render(
        request,
        "restaurants/restaurant_edit_form.html",
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
