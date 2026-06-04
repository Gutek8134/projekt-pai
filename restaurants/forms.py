from django import forms

from .models import Restaurant, RestaurantMenuType, Review


class RestaurantFilterForm(forms.Form):
    name = forms.CharField(
        max_length=100, label="Restaurant Name", required=False)
    max_distance = forms.IntegerField(
        min_value=1, max_value=100, widget=forms.NumberInput, label="Max distance in kilometers", required=False)
    menu_types = forms.MultipleChoiceField(choices=list(
        RestaurantMenuType.objects.values_list("pk", "menu_type")), widget=forms.CheckboxSelectMultiple, required=False)


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "menu_type", "address",
                  "photo", "latitude", "longditude"]


class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(label="Rating", min_value=0, max_value=10)
    comment_text = forms.CharField(
        label="Review Details", widget=forms.Textarea, required=False)

    class Meta:
        model = Review
        fields = ["rating", "comment_text"]


class CommentFilterForm(forms.Form):
    comment_text = forms.CharField(
        label="Review Details", required=True)
