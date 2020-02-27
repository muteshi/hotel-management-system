from django.contrib import admin
from .models import Reservation, PackageReservation


admin.site.register(Reservation)

admin.site.register(PackageReservation)
