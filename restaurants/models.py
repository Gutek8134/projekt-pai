from django.db.models.manager import Manager
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class RestaurantMenuType(models.Model):
    objects: Manager
    menu_type = models.CharField(
        max_length=50, verbose_name="Menu Type", unique=True)

    def __str__(self):
        return repr(self.menu_type)


class Restaurant(models.Model):
    objects: Manager
    name = models.CharField(max_length=100, verbose_name="Restaurant Name")
    menu_type = models.ForeignKey(
        RestaurantMenuType, on_delete=models.RESTRICT)
    address = models.CharField(
        max_length=255, verbose_name="Restaurant Address")
    photo = models.ImageField()
    latitude = models.DecimalField(
        max_digits=8, decimal_places=5, verbose_name="Restaurant Latitude"
    )
    longditude = models.DecimalField(
        max_digits=8, decimal_places=5, verbose_name="Restaurant Longditude"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Created by")

    def __str__(self):
        return repr(self.name)

    class Meta:
        unique_together = [[
            "name", "address", "latitude", "longditude"
        ]]


class Review(models.Model):
    objects: Manager
    for_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="Rating")
    comment_text = models.TextField(verbose_name="Review Details")
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Created by")

    class Meta:
        indexes = [
            models.Index(fields=["comment_text"], name="comments_text_index")
        ]
        unique_together = [["for_restaurant", "created_by"]]
