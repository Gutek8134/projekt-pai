from django.db.models.manager import Manager
from django.db import models


# Create your models here.
class RestaurantMenuType(models.Model):
    objects: Manager
    menu_type = models.CharField(max_length=50, verbose_name="Menu Type")

    def __str__(self):
        return repr(self.menu_type)


class Restaurant(models.Model):
    objects: Manager
    name = models.CharField(max_length=100, verbose_name="Restaurant Name")
    menu_type = models.ForeignKey(
        RestaurantMenuType, on_delete=models.RESTRICT)
    address = models.CharField(
        max_length=255, verbose_name="Restaurant Address")
    photo = models.ImageField(width_field="512", height_field="512")
    latitude = models.DecimalField(
        max_digits=8, decimal_places=5, verbose_name="Restaurant Latitude"
    )
    longditude = models.DecimalField(
        max_digits=8, decimal_places=5, verbose_name="Restaurant Longditude"
    )

    def __str__(self):
        return repr(self.name)


class Review(models.Model):
    objects: Manager
    for_restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="Rating")
    comment_text = models.TextField(verbose_name="Review Details")

    class Meta:
        indexes = [
            models.Index(fields=["comment_text"], name="comments_text_index")
        ]
