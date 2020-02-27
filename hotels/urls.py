from django.urls import path
from . import views
from django.conf.urls import include, url
from .views import (HotelsListView, HotelsDetailView,
                    HotelsCreateView, PhotoUploadView,
                    HotelsUpdateView, HotelsDeleteView,
                    RoomListView, RoomUpdateView, RoomDeleteView,
                    PackagesCreateView,HotelPackagesCreateView,
                    ItinireryCreateView,PackagesDetailView
                    )

urlpatterns = [
    path('', views.home, name='bookings-home'),
    path('hotels/<slug:slug>', HotelsDetailView.as_view(), name='hotel-detail'),
    path('hotels/packages/<slug:slug>', PackagesDetailView.as_view(), name='package-detail'),
    path('hotels/new/', HotelsCreateView.as_view(), name='hotel-create'),
    path('hotels/package/new', PackagesCreateView.as_view(), name='package-create'),
    path('hotels/room/new', views.new_room, name='room-create'),
     path('hotels/package/itinirery/<int:pk>/', ItinireryCreateView.as_view(), name='itinirery-create'),
    # path('hotels/review/new', views.ReviewCreateView.as_view(), name='review-create'),
    path('hotels/<int:pk>/update/', HotelsUpdateView.as_view(), name='hotel-update'),
    path('hotels/rooms/<int:pk>/update/', RoomUpdateView.as_view(), name='room-update'),
    path('hotels/rooms/<int:pk>/delete/', RoomDeleteView.as_view(), name='room-delete'),
    path('hotels/<int:pk>/delete/', HotelsDeleteView.as_view(), name='hotel-delete'),
    path('company/', views.company, name='bookings-company'),
    path('hotels/', views.hotels, name='hotels-list'),
    path('packages/', views.package_main_list, name='packages-main-list'),
    path('hotels/rooms/', RoomListView.as_view(), name='room-list'),
    path('hotels/package/', views.package_list, name='package-list'),
    path('photo-upload/hotels/<int:pk>/', views.PhotoUploadView.as_view(), name='photo-upload'),
    path('hotels/package/<int:pk>/', views.HotelPackagesCreateView.as_view(), name='package-hotel-create'),
    path('clear/', views.clear_database, name='clear-database'),
    path('cart/', views.view, name='cart'),
    path('hotels/package/cart/', views.package_view, name='package-cart'),
    # path('hotels/booking/<int:pk>/', views.update_booking, name='update-booking'),
    # path('hotels/<slug:slug>/', views.single, name='single_hotel'),
    # path('cart/<slug:slug>/', views.update_booking, name='update-booking'),
    url(r'^cart/(?P<id>\d+)/$', views.remove_from_cart, name='remove-booking'),
    url(r'^hotels/package/cart/remove/(?P<id>\d+)/$', views.remove_from_packagecart, name='remove-package-booking'),
    path('reservations/', views.reservations, name='user_reservations'),
    path('hotels/search/', views.search_hotels, name='search'),
]
