from django import template
from auction.models import *

register = template.Library()


@register.simple_tag(takes_context=True)
def get_images_by_car(context, car_pk):
    for i in context['car_images']:
        if i.car.pk == car_pk:
            return i.url

    return None
