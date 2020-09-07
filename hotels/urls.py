from django.urls import path
from . import views
from django.conf.urls import include, url
from .views import (
    HotelsListView,
    ApartmentListView,
    HotelsDetailView,
    ApartmentDetailView,
    PackagesDetailView,
    ConferenceHotelsDetailView


)

urlpatterns = [
    path('', views.home, name='bookings-home'),

    path('hotels/<slug:slug>', HotelsDetailView.as_view(), name='hotel-detail'),

    path('apartments/<slug:slug>',
         ApartmentDetailView.as_view(), name='apartment-detail'),

    path('hotels/conference/<slug:slug>',
         ConferenceHotelsDetailView.as_view(), name='conference-hotel-detail'),

    path('hotels/packages/<slug:slug>',
         PackagesDetailView.as_view(), name='package-detail'),

    path('company/', views.company, name='bookings-company'),

    path('hotels/', HotelsListView.as_view(), name='hotels-list'),

    path('apartments/', ApartmentListView.as_view(), name='apartments-list'),

    path('hotels/conference/', views.conference_hotels,
         name='conferencehotels-list'),

    path('packages/', views.package_main_list, name='packages-main-list'),

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

    path('hotels/search_results/', views.search, name='search-hotels'),

    path('hotels/conference/search_results/',
         views.search_conference_venues, name='search-conference-venues'),

    path('hotels/packages/search_results/',
         views.search_packages, name='search-packages'),

]
