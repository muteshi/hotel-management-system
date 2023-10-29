from django.urls import path
from . import views
from rest_framework import routers
from django.conf.urls import include
from .views import (
    HotelCreateAPIView,
    HotelsListAPIView,
    HotelDetailAPIView,
    HotelDeleteAPIView,
    HotelUpdateAPIView,
    HotelFacilitiesUpdateAPIView,
    HotelPolicyUpdateAPIView,
    HotelSettingsUpdateAPIView,
    HotelTypeListAPIView,
    RoomTypeListAPIView,
    RoomTypesSerializers,
    RoomAmmenitiesUpdateAPIView,
    RoomSettingsUpdateAPIView,
    RoomCreateAPIView,
    RoomDetailAPIView,
    RoomsListAPIView,
    RoomUpdateAPIView,
    RoomDeleteAPIView,
    PackageCreateAPIView,
    PackagesListAPIView,
    PackageDetailAPIView,
    PackageUpdateAPIView,
    PackageDeleteAPIView,
    ConferenceHotelsListAPIView,
    HotelPackageCreateAPIView,
    HotelPackageUpdateAPIView,
    HotelPackageListAPIView,
    HotelPackageDetailAPIView,
    HotelPackageDeleteAPIView,
    ItinireryCreateAPIView,
    ItinireryDetailAPIView,
    ItinireryUpdateAPIView,
    ItinireryListAPIView,
    ItinireryDeleteAPIView,
    PackageTypeListAPIView,
    PackagePhotoUploadView,
    PackagePhotoListAPIView,
    HotelPartialUpdateView,
    PackagePartialUpdateView,
    PhotoUploadView,
    PhotoListAPIView,
    RoomPhotoUploadView,
    RoomPhotoListAPIView,
    HotelsAPIView
)

# router = routers.DefaultRouter()
# router.register(r'hotel', views.HotelsViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('hotel-types/', HotelTypeListAPIView.as_view(),
         name='api-hoteltypes-list'),

    path('room-types/', RoomTypeListAPIView.as_view(),
         name='api-roomtypes-list'),

    path('hotel/new/', HotelCreateAPIView.as_view(), name='api-hotel-create'),

    path('hotel/', HotelsListAPIView.as_view(), name='api-hotels-list'),

    path('mobile-hotel/', HotelsAPIView.as_view(), name='api-hotel-mobile-list'),

    path('conference-hotel/', ConferenceHotelsListAPIView.as_view(),
         name='api-chotels-list'),

    path('hotel/<slug:slug>/', HotelDetailAPIView.as_view(),
         name='api-hotel-details'),

    path('hotel/<slug:slug>/update/',
         HotelUpdateAPIView.as_view(), name='api-hotel-update'),

    path('hotel-facilities/<slug:slug>/update/',
         HotelFacilitiesUpdateAPIView.as_view(), name='api-hotelfacility-update'),

    path('hotel-settings/<slug:slug>/update/',
         HotelSettingsUpdateAPIView.as_view(), name='api-hotelsettings-update'),

    path('hotel-policy/<slug:slug>/update/',
         HotelPolicyUpdateAPIView.as_view(), name='api-hotelsettings-update'),

    path('hotel/<slug:slug>/partial-update/',
         HotelPartialUpdateView.as_view(), name='api-hotel-partialupdate'),


    path('hotel/<int:pk>/delete/',
         HotelDeleteAPIView.as_view(), name='api-hotel-delete'),


    path('package-types/', PackageTypeListAPIView.as_view(),
         name='api-packagetypes-list'),

    path('package/<slug:slug>/partial-update/',
         PackagePartialUpdateView.as_view(), name='api-package-partialupdate'),


    path('package/new/', PackageCreateAPIView.as_view(),
         name='api-package-create'),

    path('package/', PackagesListAPIView.as_view(),
         name='api-packages-list'),

    path('package/<slug:slug>/', PackageDetailAPIView.as_view(),
         name='api-packages-details'),

    path('package/<slug:slug>/update/',
         PackageUpdateAPIView.as_view(), name='api-package-update'),

    path('package/<slug:slug>/delete/',
         PackageDeleteAPIView.as_view(), name='api-package-delete'),

    path('hotel-package/new/', HotelPackageCreateAPIView.as_view(),
         name='api-hotelpackage-create'),

    path('hotelpackages/<int:pk>/', HotelPackageListAPIView.as_view(),
         name='api-packages-list'),

    path('hotel-package/<int:pk>', HotelPackageDetailAPIView.as_view(),
         name='api-hotelpackage-details'),

    path('hotel-package/<int:pk>/update/',
         HotelPackageUpdateAPIView.as_view(), name='api-hotelpackage-update'),

    path('hotel-package/<int:pk>/delete/',
         HotelPackageDeleteAPIView.as_view(), name='api-hotelpackage-delete'),

    path('itinirery/new/', ItinireryCreateAPIView.as_view(),
         name='api-itinirery-create'),

    path('itinirery/<int:pk>/', ItinireryListAPIView.as_view(),
         name='api-packages-list'),

    path('itinirery/<int:pk>', ItinireryDetailAPIView.as_view(),
         name='api-itinirery-details'),

    path('itinirery/<int:pk>/update/',
         ItinireryUpdateAPIView.as_view(), name='api-itinirery-update'),

    path('itinirery/<int:pk>/delete/',
         ItinireryDeleteAPIView.as_view(), name='api-itinirery-delete'),


    path('hotel/room/new/', RoomCreateAPIView.as_view(),
         name='api-hotelroom-create'),

    path('hotel-room/<int:pk>/', RoomsListAPIView.as_view(),
         name='api-hotelroom-list'),

    path('hotel/room/<int:pk>', RoomDetailAPIView.as_view(),
         name='api-hotelroom-details'),

    path('hotel-room/<int:pk>/update/',
         RoomUpdateAPIView.as_view(), name='api-room-update'),

    path('hotel-room/<int:pk>/delete/',
         RoomDeleteAPIView.as_view(), name='api-room-delete'),

    path('room-ammenities/<int:pk>/update/',
         RoomAmmenitiesUpdateAPIView.as_view(), name='api-roomammenities-update'),

    path('room-settings/<int:pk>/update/',
         RoomSettingsUpdateAPIView.as_view(), name='api-roomsettings-update'),

    path('photos-upload/', PhotoUploadView.as_view(),
         name='api-hotel-photos-upload'),

    path('hotel/photos/<int:pk>/',
         PhotoListAPIView.as_view(), name='api-hotel-photos'),

    path('room-photos-upload/', RoomPhotoUploadView.as_view(),
         name='api-hotelroom-photos-upload'),

    path('hotel-room/photos/<int:pk>/',
         RoomPhotoListAPIView.as_view(), name='api-hotelroom-photos'),

    path('package-photos-upload/', PackagePhotoUploadView.as_view(),
         name='api-package-photos-upload'),

    path('package/photos/<int:pk>/',
         PackagePhotoListAPIView.as_view(), name='api-package-photos'),

]
