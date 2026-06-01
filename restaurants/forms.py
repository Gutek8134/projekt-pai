from django import forms

from .models import Restaurant


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "menu_type", "address",
                  "photo", "latitude", "longditude"]
