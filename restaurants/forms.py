from django import forms

from .models import Restaurant, RestaurantMenuType


class RestaurantFilterForm(forms.Form):
    name = forms.CharField(
        max_length=100, label="Restaurant Name", required=False)
    max_distance = forms.IntegerField(
        min_value=0, max_value=100, widget=forms.NumberInput({"step": "5"}), label="Max distance in kilometers", required=False)
    menu_types = forms.MultipleChoiceField(choices=list(
        RestaurantMenuType.objects.values_list("pk", "menu_type")), widget=forms.CheckboxSelectMultiple, required=False)


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "menu_type", "address",
                  "photo", "latitude", "longditude"]
