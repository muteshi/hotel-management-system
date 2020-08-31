import random
from django.http import HttpResponse, Http404
from reservations.utils import id_generator
from hotels.api.permissions import IsOwnerOrReadOnly,  IsAdminOrOwner, IsAdmin
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
    ListCreateAPIView,
)
from reservations.models import (
    Booking,
    BookingSettings,
    BookingStatus,
    PaymentOptions,

)

from .serializers import (
    BookingStatusSerializer,
    PayemntOptionsSerializer,
    BookingsCreateSerializer,
    BookingDetailsSerializer,
    BookingItemDetailsSerializer,
    BookingUpdateSerializer,
    BookingSettingsSerializer,
)

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import UpdateModelMixin
from rest_framework import status, permissions, serializers, viewsets
from rest_framework.permissions import BasePermission
from django.db.models import Q
from rest_framework.response import Response


class BookingCreateAPIView(CreateAPIView):
    """Create a new hotel booking object"""
    queryset = Booking.objects.all()
    serializer_class = BookingsCreateSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        serializer.save(reservation_id=id_generator(
        ), invoice_number=random.randint(11, 99)*254)


class BookingDetailAPIView(RetrieveAPIView):
    """Display details of a single booking"""
    queryset = Booking.objects.all()
    serializer_class = BookingDetailsSerializer
    permission_classes = ()


class BookingItemDetailAPIView(RetrieveAPIView):
    """Display details of a single booking item"""
    queryset = Booking.objects.all()
    serializer_class = BookingItemDetailsSerializer
    permission_classes = ()


class BookingSettingsAPIView(ListAPIView):
    """Displays details of  settings"""
    queryset = BookingSettings.objects.all()
    serializer_class = BookingSettingsSerializer
    permission_classes = ()


class BookingUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of a booking object"""
    queryset = Booking.objects.all()
    serializer_class = BookingUpdateSerializer
    permission_classes = (IsAdminOrOwner,)

    def perform_update(self, serializers):
        serializers.save(user=self.request.user)


class BookingDeleteAPIView(DestroyAPIView):
    """Deletes a booking object"""
    queryset = Booking.objects.all()
    serializer_class = BookingsCreateSerializer
    permission_classes = (IsAdminOrOwner,)

    def destroy(self, request, *args, **kwargs):
        """Override default destroy method"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingListAPIView(ListAPIView):
    serializer_class = BookingDetailsSerializer
    permission_classes = ()

    def get_queryset(self, *args, **kwargs):
        if (self.request.user) and (self.request.user.is_superuser):
            bookings = Booking.objects.all()
        else:
            bookings = Booking.objects.filter(
                Q(user=self.request.user.id))

        return bookings


class PaymentOptionsListAPIView(ListAPIView):
    """Displays list of payment options"""
    queryset = PaymentOptions.objects.all()
    serializer_class = PayemntOptionsSerializer
    permission_classes = (permissions.AllowAny,)


class BookingStatusListAPIView(ListAPIView):
    """Displays list of booking status"""
    queryset = BookingStatus.objects.all()
    serializer_class = BookingStatusSerializer
    permission_classes = (permissions.AllowAny,)
