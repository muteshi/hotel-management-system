from django.db import models
from django.db.models.signals import pre_save
from hotels.models import Hotels, Room, Cart, ConferenceRoom, Packages, HotelPackages
from users.models import UserProfile

from django.conf import settings

from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create a Reservation Model which stores booking details

STATUS_CHOICES = (
    ("Started", 'Started'),
    ("Abandoned", 'Abandoned'),
    ("Finished", 'Finished'),
)

PAYMENT_OPTIONS = (
    ("pay_on_checkin", 'Pay on CheckIn'),
    ("visa_mastercard", 'Visa or MasterCard'),
)


class Reservation(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    reservation_id = models.CharField(
        max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True,)
    sub_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    final_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=120, choices=STATUS_CHOICES, default='Started')
    payment_option = models.CharField(
        max_length=120, choices=PAYMENT_OPTIONS, default='pay_on_checkin')
    special_request = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'Reservation #{self.reservation_id}'


class PackageReservation(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    reservation_id = models.CharField(
        max_length=120, default='ABC', unique=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True,)
    sub_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    final_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=120, choices=STATUS_CHOICES, default='Started')
    payment_option = models.CharField(
        max_length=120, choices=PAYMENT_OPTIONS, default='pay_on_checkin')
    special_request = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = 'Package Reservations'

    def __str__(self):
        return f'Reservation #{self.reservation_id}'


class BookingStatus(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Booking Status'

    def __str__(self):
        return f'{self.name}'


class BookingSettings(models.Model):
    commission = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = 'Booking Settings'

    def __str__(self):
        return f'{self.commission}'


class PaymentOptions(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Payment Options'

    def __str__(self):
        return f'{self.name}'


class BookingItems(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True,)
    rooms = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)
    hotel_package = models.ForeignKey(
        HotelPackages, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField(default=1)  # room quantity
    total_guests = models.PositiveIntegerField(default=1)  # guests quantity
    sub_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    checkin = models.DateField(null=True, blank=True)
    checkout = models.DateField(null=True, blank=True)
    stay_duration = models.PositiveIntegerField(default=1)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Booking items'


class Booking(models.Model):
    """Database table for users booking details"""
    email = models.EmailField(max_length=255, unique=False)
    guest_name = models.CharField(max_length=255, null=True, blank=True,)
    first_name = models.CharField(max_length=255, null=True, blank=True,)
    last_name = models.CharField(max_length=255, null=True, blank=True,)
    company_name = models.CharField(max_length=255, null=True, blank=True,)
    commission_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    mobile_Number = models.CharField(max_length=12, null=True, blank=True,)
    invoice_number = models.CharField(max_length=20, null=True, blank=True,)
    tax_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    final_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    deposit = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    reservation_id = models.CharField(
        max_length=120, default='ABC', unique=True)
    payment_option = models.ForeignKey(
        PaymentOptions, on_delete=models.CASCADE, null=True, blank=True,)
    hotel = models.ForeignKey(
        Hotels, on_delete=models.CASCADE, null=True, blank=True,)
    items = models.ManyToManyField(BookingItems)
    booking_status = models.ForeignKey(
        BookingStatus, on_delete=models.CASCADE, null=True, blank=True,)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    package = models.ForeignKey(
        Packages, on_delete=models.CASCADE, null=True, blank=True,)
    special_requests = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f'Reservation #{self.reservation_id}'


def get_commission_total(sender, instance, *args, **kwargs):

    commission = BookingSettings.objects.all()[0].commission
    instance.commission_total = commission/100 * instance.final_total


pre_save.connect(get_commission_total, sender=Booking)


class ConferenceReservation(models.Model):
    """Database table for users booking details"""
    organisation_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_Number = models.CharField(max_length=12)
    reservation_id = models.CharField(
        max_length=120, default='ABC', unique=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    attachment = models.FileField(
        upload_to='pay_attachments', null=True, blank=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=True,)
    crooms = models.ForeignKey(
        ConferenceRoom, on_delete=models.CASCADE, null=True, blank=True)
    hrooms = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)
    final_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    name_of_guests = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = 'Conference Reservations'

    def __str__(self):
        return f'Reservation #{self.reservation_id}'

    def guests_as_list(self):
        return self.name_of_guests.split('\n')
