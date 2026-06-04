from django import template

register = template.Library()

@register.filter()
def access_dict(dictionary: dict, key):
    return dictionary[key]