from django.contrib import admin
from .models import(
    Reservation,
    PackageReservation,
    Booking,
    BookingSettings,
    BookingItems,
    BookingStatus,
    PaymentOptions,

)


class BookingAdmin(admin.ModelAdmin):
    list_display = ["guest_name", "created_at",
                    "final_total", "commission_total"]

    class Meta:
        model = Booking


admin.site.register(Reservation)

admin.site.register(PackageReservation)

admin.site.register(Booking,  BookingAdmin)

admin.site.register(BookingSettings)

admin.site.register(BookingItems)

admin.site.register(BookingStatus)

admin.site.register(PaymentOptions)
