from django.urls import path
from . import views
from django.conf.urls import include, url
from .views import (
    BookingCreateAPIView,
    BookingDetailAPIView,
    BookingUpdateAPIView,
    BookingDeleteAPIView,
    BookingListAPIView,
    PaymentOptionsListAPIView,
    BookingStatusListAPIView,
    BookingItemDetailAPIView,
    BookingSettingsAPIView
)
urlpatterns = urlpatterns = [

    path('booking/', BookingListAPIView.as_view(), name='api-bookings-list'),
    path('booking/new/', BookingCreateAPIView.as_view(), name='api-booking-create'),


    path('booking/<int:pk>/', BookingDetailAPIView.as_view(),
         name='api-booking-details'),

    path('booking-item/<int:pk>/', BookingItemDetailAPIView.as_view(),
         name='api-bookingItem-details'),

    path('booking-settings/', views.BookingSettingsAPIView.as_view()),

    path('booking/<int:pk>/update/',
         BookingUpdateAPIView.as_view(), name='api-booking-update'),

    path('booking/<int:pk>/delete/',
         BookingDeleteAPIView.as_view(), name='api-booking-delete'),

    path('booking-status/', BookingStatusListAPIView.as_view(),
         name='api-booking-status-list'),

    path('payment-options/', PaymentOptionsListAPIView.as_view(),
         name='api-payment-options-list'),
]
