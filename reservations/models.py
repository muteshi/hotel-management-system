from django.db import models
from hotels.models import Hotels, Room, Cart
from users.models import UserProfile

from django.conf import settings

from django.core.mail import send_mail

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


#Create a Reservation Model which stores booking details

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
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = True, blank = True)
    reservation_id = models.CharField(max_length=120, default='ABC',unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True,)
    sub_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    final_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    payment_option = models.CharField(max_length=120, choices=PAYMENT_OPTIONS, default='pay_on_checkin')
    special_request = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = 'Reservations'

    def __str__(self):
         return f'Reservation #{self.reservation_id}'


    # def save(self):
    #     """Override default save method to resize the photo"""
    #     super().save()
    #     #Send email on Successfull reservation creation
    #     cart2 = Reservation.objects.get(cart2=self.cart.id)
    #     context = {"user":  self.user.name, "room": cart2.cart.cartitems_set.all()[0].rooms}
    #     message = render_to_string("hotels/user_reservation_details.html", context)
    #     plain_message = strip_tags(message)
    #     subject = f"Registration details for {room}"
    #     mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.user.email], html_message=message)

    #     self.status = "Finished"

class PackageReservation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    reservation_id = models.CharField(max_length=120, default='ABC',unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True,)
    sub_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    tax_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    final_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    payment_option = models.CharField(max_length=120, choices=PAYMENT_OPTIONS, default='pay_on_checkin')
    special_request = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp =models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = 'Package Reservations'

    def __str__(self):
         return f'Reservation #{self.reservation_id}'


TITLE_OPTIONS = (
    ("mr", 'Mr.'),
    ("mrs", 'Mrs.'),
    ("ms", 'Ms.'),
)

PAYMENT_OPTIONS = (
    ("pay_on_checkin", 'Pay on CheckIn'),
    ("visa_mastercard", 'Visa or MasterCard'),
)

class Booking(models.Model):
    """Database table for users booking details"""
    title = models.CharField(max_length=120, choices=TITLE_OPTIONS, default='mr')
    email = models.EmailField(max_length=255, unique=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_Number = models.CharField(max_length=12)
    reservation_id = models.CharField(max_length=120, default='ABC',unique=True)
    payment_option = models.CharField(max_length=120, choices=PAYMENT_OPTIONS, default='pay_on_checkin')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True,)
    final_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    special_requests = models.TextField(null=True, blank=True,)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    register_as_user = models.BooleanField(default=False)
   

    class Meta:
        verbose_name_plural = 'Bookings'

    def __str__(self):
         return f'Reservation #{self.reservation_id}'

