from django import forms
from hotels.models import Hotels, Packages
import django_filters

class HotelFilter(django_filters.FilterSet):
	name = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Hotels
		fields = ['name']


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