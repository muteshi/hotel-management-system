from django import forms
from hotels.models import Hotels, Packages
import django_filters


class HotelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    has_conference = django_filters.BooleanFilter(field_name='has_conference')

    class Meta:
        model = Hotels
        fields = ['name', 'has_conference']


PACKAGE_TYPES = (
    ('honeymoon', "Honeymoon"),
    ('easter', "Easter"),
    ('christmas', "Christmas"),
    ('coast', "Coast"),
    ('selfdrive', "Weekend Gateway"),
)


class PackagesFilter(django_filters.FilterSet):
    package_type = django_filters.ChoiceFilter(choices=PACKAGE_TYPES)

    class Meta:
        model = Packages
        fields = ['package_type']
