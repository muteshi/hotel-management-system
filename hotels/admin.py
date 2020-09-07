from django.contrib import admin
from .models import (
    Hotels,
    HotelTypes,
    RoomTypes,
    Room,
    Photo,
    RoomPhoto,
    PackagePhoto,
    Packages,
    PackageTypes,
    Itinirery,
    HotelPackages,
    Slider,


)


class HotelsAdmin(admin.ModelAdmin):
    # list_display = ('title', 'body',)
    prepopulated_fields = {'slug': ('name',)}  # new


class PackagesAdmin(admin.ModelAdmin):
    # list_display = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}  # new


class RoomAdmin(admin.ModelAdmin):
    # list_display = ('title', 'body',)
    prepopulated_fields = {'slug': ('room_Name', 'room_type',)}  # new

    class Meta:
        model = Room


class SliderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "start_Date", "end_Date", "active", "featured"]

    class Meta:
        model = Slider


admin.site.register(Hotels, HotelsAdmin)

admin.site.register(HotelTypes)
admin.site.register(RoomTypes)

admin.site.register(Room, RoomAdmin)

admin.site.register(Photo)

admin.site.register(RoomPhoto)

admin.site.register(PackagePhoto)

admin.site.register(Packages, PackagesAdmin)

admin.site.register(PackageTypes)

admin.site.register(Itinirery)

admin.site.register(HotelPackages)


admin.site.register(Slider, SliderAdmin)
