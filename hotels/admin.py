from django.contrib import admin
from .models import Hotels, Room, Photo, Cart, CartItems, HotelService


class HotelsAdmin(admin.ModelAdmin):
    # list_display = ('title', 'body',)
    prepopulated_fields = {'slug': ('name',)} # new

class RoomAdmin(admin.ModelAdmin):
    # list_display = ('title', 'body',)
    prepopulated_fields = {'slug': ('room_Name','room_Type',)} # new

class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart

admin.site.register(Hotels, HotelsAdmin)

admin.site.register(Room, RoomAdmin)

admin.site.register(Photo)

admin.site.register(Cart, CartAdmin)

admin.site.register(CartItems)

admin.site.register(HotelService)
