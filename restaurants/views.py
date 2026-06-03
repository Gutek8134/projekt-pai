from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, FloatField, Avg
from django.db.models.functions import Power, Sqrt, Radians, Sin, Cos, ATan2

from .forms import RestaurantForm, RestaurantFilterForm, CommentForm, CommentFilterForm
from .models import Restaurant, Review

from math import radians, cos

RADIUS = 6371
USER_LATITUDE = 52.40692
USER_LONGDITUDE = 16.92993

# Create your views here.


def restaurant_list(request: HttpRequest):
    restaurants = Restaurant.objects.all()
    average_ratings = {}
    for restaurant in restaurants:
        average_ratings[restaurant.pk] = Review.objects.filter(
            for_restaurant=restaurant).aggregate(Avg("rating"))['rating__avg']

    if request.method == "GET":
        filter_form = RestaurantFilterForm(request.GET)
        if "name" in request.GET:
            restaurants = restaurants.filter(name__icontains=filter_form.data['name'])\
                .annotate(distance_latitude_r=Radians(F("latitude")-USER_LATITUDE, output_field=FloatField()), distance_longditude_r=Radians(F("longditude")-USER_LONGDITUDE, output_field=FloatField()))\
                .annotate(a=Power(Sin(F("distance_latitude_r")/2), 2, output_field=FloatField()) +
                          cos(radians(USER_LATITUDE))*Cos(Radians(F("latitude")), output_field=FloatField()) *
                          Power(Sin(F("distance_longditude_r")/2), 2, output_field=FloatField()))\
                .annotate(c=2*ATan2(Sqrt(F("a")), Sqrt(1-F("a")), output_field=FloatField()))\
                .annotate(distance=RADIUS*F("c"))

        if "max_distance" in request.GET and request.GET["max_distance"].replace(".", "", 1).isdigit():
            try:
                restaurants = restaurants\
                    .filter(distance__lte=filter_form.data['max_distance'])
            except ValueError as e:
                print(e)

        if "menu_types" in request.GET:
            restaurants = restaurants.filter(
                menu_type__in=filter_form.data['menu_types'])

    else:
        filter_form = RestaurantFilterForm()

    restaurants.order_by("name")
    return render(
        request, "restaurants/restaurant_list.html", {
            "restaurants": restaurants,
            "average_ratings": average_ratings,
            "form": filter_form,
            "user_position": (USER_LATITUDE, USER_LONGDITUDE), }
    )


def restaurant_details(request: HttpRequest, pk: int):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    reviews = Review.objects.filter(for_restaurant=restaurant)
    average_rating = reviews.aggregate(Avg("rating"))['rating__avg']

    if request.method == "POST":
        form = CommentForm(request.POST)
        form.instance.for_restaurant = restaurant
        form.instance.created_by = request.user

        if form.is_valid():
            form.save()

    else:
        form = CommentForm()

    logged_in = request.user.is_authenticated
    left_a_comment = False
    if logged_in:
        left_a_comment = reviews.filter(created_by=request.user).exists()
    can_leave_a_comment = logged_in and not left_a_comment

    return render(request,
                  "restaurants/restaurant_details.html",
                  {
                      "restaurant": restaurant,
                      "reviews": reviews,
                      "average_rating": average_rating,
                      "can_leave_a_comment": can_leave_a_comment,
                      "form": form
                  })


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
    goto = request.GET.get("goto", "restaurants:restaurant_list")

    if request.method == "POST":
        Review.objects.filter(for_restaurant=restaurant).delete()
        restaurant.delete()
        return redirect("restaurants:restaurant_list")

    return render(
        request,
        "restaurants/confirm_delete_restaurant.html",
        {"restaurant": restaurant, "goto": goto},
    )


def delete_review(request: HttpRequest, pk: int):
    review = get_object_or_404(Review, pk=pk)
    goto = request.GET.get("goto", "restaurants:restaurant_list")

    if request.method == "POST":
        review.delete()
        return redirect(goto)

    return render(
        request,
        "restaurants/confirm_delete_review.html",
        {"review": review, "goto": goto},
    )


def search_reviews(request: HttpRequest):
    reviews = Review.objects.none()
    form = CommentFilterForm(request.GET)
    if form.is_valid():
        reviews = Review.objects.filter(
            comment_text__icontains=form.data['comment_text'])

    return render(
        request,
        "restaurants/search_review.html",
        {"form": form, "reviews": reviews}
    )
