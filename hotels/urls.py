from django.urls import path
from . import views
from django.conf.urls import include, url
from .views import (
    HotelsListView,
    ApartmentListView,
    HotelsDetailView,
    ApartmentDetailView,
    HotelsCreateView,
    PhotoUploadView,
    HotelsUpdateView,
    HotelsDeleteView,
    RoomListView,
    RoomUpdateView,
    RoomDeleteView,
    PackagesCreateView,
    HotelPackagesCreateView,
    ItinireryCreateView,
    PackagesDetailView,
    ConferenceHotelsDetailView,
    ConferenceRoomDeleteView,
    ConferenceRoomUpdateView,
    CityHotelsListView,
    FrontendAppView
)

urlpatterns = [
    path('', views.home, name='bookings-home'),

    path('dashboard/', FrontendAppView.as_view()),

    path('hotels/<slug:slug>', HotelsDetailView.as_view(), name='hotel-detail'),

    path('apartments/<slug:slug>',
         ApartmentDetailView.as_view(), name='apartment-detail'),

    path('hotels/conference/<slug:slug>',
         ConferenceHotelsDetailView.as_view(), name='conference-hotel-detail'),

    path('hotels/packages/<slug:slug>',
         PackagesDetailView.as_view(), name='package-detail'),

    path('hotels/new/', HotelsCreateView.as_view(), name='hotel-create'),

    path('hotels/package/new', PackagesCreateView.as_view(), name='package-create'),

    path('hotels/room/new', views.new_room, name='room-create'),

    path('hotels/conferenceroom/new', views.new_conferenceroom,
         name='conferenceroom-create'),

    path('hotels/package/itinirery/<int:pk>/',
         ItinireryCreateView.as_view(), name='itinirery-create'),

    # path('hotels/review/new', views.ReviewCreateView.as_view(), name='review-create'),
    path('hotels/<int:pk>/update/',
         HotelsUpdateView.as_view(), name='hotel-update'),

    path('hotels/rooms/<int:pk>/update/',
         RoomUpdateView.as_view(), name='room-update'),

    path('hotels/conferenceroom/<int:pk>/update/',
         ConferenceRoomUpdateView.as_view(), name='conferenceroom-update'),

    path('hotels/rooms/<int:pk>/delete/',
         RoomDeleteView.as_view(), name='room-delete'),

    path('hotels/conferenceroom/<int:pk>/delete/',
         ConferenceRoomDeleteView.as_view(), name='conferenceroom-delete'),

    path('hotels/<int:pk>/delete/',
         HotelsDeleteView.as_view(), name='hotel-delete'),

    path('company/', views.company, name='bookings-company'),

    path('hotels/', HotelsListView.as_view(), name='hotels-list'),

    path('apartments/', ApartmentListView.as_view(), name='apartments-list'),

    path('hotels/<slug:slug>', CityHotelsListView.as_view(),
         name='city-hotels-list'),

    path('hotels/conference/', views.conference_hotels,
         name='conferencehotels-list'),

    path('packages/', views.package_main_list, name='packages-main-list'),

    path('hotels/rooms/', RoomListView.as_view(), name='room-list'),

    path('hotels/package/', views.package_list, name='package-list'),

    path('hotels/packages/honeymoon/', views.package_honeymoon_list,
         name='package_honeymoon_list'),

    path('hotels/packages/easter/', views.package_easter_list,
         name='package_easter_list'),

    path('hotels/packages/christmas/', views.package_christmas_list,
         name='package_christmas_list'),

    path('hotels/packages/coast/', views.package_coast_list,
         name='package_coast_list'),

    path('hotels/packages/selfdrive/', views.package_selfdrive_list,
         name='package_selfdrive_list'),

    path('photo-upload/hotels/<int:pk>/',
         views.PhotoUploadView.as_view(), name='photo-upload'),
    path('hotels/package/<int:pk>/',
         views.HotelPackagesCreateView.as_view(), name='package-hotel-create'),

    path('clear/', views.clear_database, name='clear-database'),
    path('cart/', views.view, name='cart'),

    path('hotels/package/cart/', views.package_view, name='package-cart'),

    path('hotels/conference/cart/', views.conference_view, name='conference-cart'),

    # path('hotels/booking/<int:pk>/', views.update_booking, name='update-booking'),
    # path('hotels/<slug:slug>/', views.single, name='single_hotel'),
    # path('cart/<slug:slug>/', views.update_booking, name='update-booking'),

    url(r'^cart/(?P<id>\d+)/$', views.remove_from_cart, name='remove-booking'),

    url(r'^hotels/package/cart/remove/(?P<id>\d+)/$',
        views.remove_from_packagecart, name='remove-package-booking'),

    url(r'^hotels/conference/cart/remove/(?P<id>\d+)/$',
        views.remove_from_conferencecart, name='remove-conference-booking'),

    path('reservations/', views.reservations, name='user_reservations'),
    # path('hotels/search/', views.search_hotels, name='search'),

    path('hotels/search_results/', views.search, name='search-hotels'),

    path('hotels/conference/search_results/',
         views.search_conference_venues, name='search-conference-venues'),

    path('hotels/packages/search_results/',
         views.search_packages, name='search-packages'),

]
