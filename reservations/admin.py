from django.contrib import admin
from .models import Reservation, PackageReservation, Booking


admin.site.register(Reservation)

admin.site.register(PackageReservation)

admin.site.register(Booking)
