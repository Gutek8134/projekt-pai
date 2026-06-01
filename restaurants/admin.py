from django.contrib import admin

from .models import Restaurant, RestaurantMenuType, Review
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(RestaurantMenuType)
admin.site.register(Review)
