import datetime
from django.template import Library

register = Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter
def plus_days(value, days):
    return value + datetime.timedelta(days=days)