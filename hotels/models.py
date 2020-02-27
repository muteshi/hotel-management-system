from datetime import date
from django.db import models
from django.utils import timezone
from users.models import UserProfile
from django.urls import reverse
from django.db.models import Min
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse

from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core import mail
from django.template.loader import render_to_string

from PIL import Image


class Hotels(models.Model):
    """Stores all the information about the hotel and also used to query hotels"""

    name = models.CharField(max_length=255) #The name of the hotel
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=12)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    property_photo = models.ImageField(default='default.jpg', upload_to='hotel_photos')
    star_rating = models.PositiveIntegerField()
    contact_person = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null=True, blank=True,) #Owner of the hotel or person who created the hotel

    class Meta:
        unique_together = ('name', 'slug')
        verbose_name_plural = 'Hotels'


    def __str__(self):
        """Prints the name of the Hotel"""
        return self.name

    def get_absolute_url(self):
        #Redirects the form to photo uploads
        return reverse('photo-upload', kwargs={'pk': self.pk})

    def save(self):
        """Override default save method to resize the photo"""
        super().save()
        #Send email on Successfull property creation
        property_url ="%s/%s" %(settings.SITE_URL,reverse("hotel-detail", args=[self.slug]))
        context = {"property_url": property_url,"user":  self.contact_person.name,}
        message = render_to_string("hotels/property_register_success.html", context)
        plain_message = strip_tags(message)
        subject = f"Registration details for {self.name}"
        mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.contact_person.email], html_message=message)
        
        img = Image.open(self.property_photo.path)

        if img.height > 500 or img.width > 500:
            output_size = (450, 600)
            img.thumbnail(output_size)
            rgb_img =img.convert('RGB')
            rgb_img.save(self.property_photo.path)
 
def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Hotels.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f'{slug}-{qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_hotel_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_hotel_receiver, sender=Hotels)



class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='hotel_photos')
    hotel = models.ForeignKey(Hotels,on_delete = models.CASCADE, null=True, blank=True,)

    class Meta:
        verbose_name_plural = 'Photos'


    def __str__(self):
        """Prints the name of the Photo"""
        return f'{self.hotel} photos'



class Room(models.Model):
    """Creates room details"""

    ROOM_CHOICES = (
    ('Single', "Single"),
    ('Double', "Double"),
    ('Family', "Family"),
    ('Suit', "Suit"),
      )

    hotel = models.ForeignKey(Hotels,on_delete = models.CASCADE, null=True, blank=True,)
    room_Type = models.CharField(
        max_length = 20,
        choices = ROOM_CHOICES,
        default = 'Please Select',
        )
    room_photo = models.ImageField(default='default.jpg', upload_to='room_photos')
    room_Name = models.CharField(max_length = 200)
    room_details = models.CharField(max_length = 500)
    room_Capacity = models.PositiveIntegerField(default = 0)
    slug = models.SlugField(unique=True)
    # guest_numbers = models.IntegerField(default=0)
    room_Price= models.PositiveIntegerField(default = 0)
    total_Rooms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    class Meta:
        unique_together = ('room_Name', 'slug')
        verbose_name_plural = 'Rooms'

    def __str__(self):
         return f'{self.room_Name}-{self.room_Type} room-{self.hotel.name}'


    def get_absolute_url(self):
        #Redirects the form to photo uploads
        return reverse('room-list')


    def save(self):
        """Override default save method"""
        super().save()

        img = Image.open(self.room_photo.path)

        if img.height > 600 or img.width > 450:
            output_size = (600, 450)
            img.thumbnail(output_size)
            rgb_img =img.convert('RGB')
            rgb_img.save(self.room_photo.path)

def create_room_slug(instance, new_slug=None):
    slug = slugify(instance.room_Name)
    if new_slug is not None:
        slug = new_slug
    qs = Room.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f'{slug}-{qs.first().id}'
        return create_room_slug(instance, new_slug=new_slug)
    return slug

def pre_save_room_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_room_slug(instance)

pre_save.connect(pre_save_room_receiver, sender=Room)


# class Review(models.Model):
#     """Stores the Hotel reviews and is used to query the reviews"""
#     user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
#     hotel = models.ForeignKey(Hotels,on_delete=models.CASCADE)
#     comment = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     rating = models.IntegerField(default = 0)
#
#     class Meta:
#         verbose_name_plural = 'Reviews'
#
#     def __str__(self):
#          return self.comment


class CartItems(models.Model):
    cart = models.ForeignKey('Cart', on_delete = models.CASCADE, null=True, blank=True)
    rooms = models.ForeignKey(Room, on_delete = models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default = 1)
    line_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    CheckIn = models.DateField(null=True, blank=True)
    CheckOut = models.DateField(null=True, blank=True)
    stay_duration = models.PositiveIntegerField(default=1)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp =models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
         return f'{self.rooms.room_Name}-{self.rooms.room_Type} room-{self.rooms.hotel.name}'

    class Meta:
        verbose_name_plural = 'Cart Items'



class Cart(models.Model):
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp =models.DateTimeField(auto_now_add=True, auto_now=False)
    active = models.BooleanField(default=True)

    def __str__(self):
         return f'Cart id: {self.id}'

class HotelService(models.Model):
    hotel = models.ForeignKey(Hotels,on_delete=models.CASCADE, null=True, blank=True,)
    title = models.CharField(max_length=120)
    service_photo = models.ImageField(default='default.jpg', upload_to='service_photos')
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    updated =models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        """Prints the name of the service"""
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Services'



class Packages(models.Model):
    """Stores all the information about a particular package"""
    PACKAGE_TYPES = (
    ('honeymoon', "Honeymoon"),
    ('easter', "Easter"),
    ('christmas', "Christmas"),
    ('coast', "Coast"),
    ('selfdrive', "Weekend Gateway"),
      )

    title = models.CharField(max_length=255) #The name of the package
    package_type = models.CharField(max_length=120, choices=PACKAGE_TYPES, default='honeymoon')
    city = models.CharField(max_length=255, null=True, blank=True,)
    country = models.CharField(max_length=255, null=True, blank=True,)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    cover_photo = models.ImageField(default='default.jpg', upload_to='package_photos')
    description = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    slug = models.SlugField(unique=True)
    
    class Meta:
        unique_together = ('title', 'slug')
        verbose_name_plural = 'Packages'

    def __str__(self):
        """Prints the name of the Hotel"""
        return self.title

    def get_absolute_url(self):
        return reverse('package-hotel-create', kwargs={'pk': self.pk})
    
def create_package_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Packages.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f'{slug}-{qs.first().id}'
        return create_package_slug(instance, new_slug=new_slug)
    return slug

def pre_save_package_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_package_slug(instance)

pre_save.connect(pre_save_package_receiver, sender=Packages)



class HotelPackages(models.Model):
    """Creates package itinirery details"""
    hotel = models.OneToOneField(Hotels,on_delete = models.CASCADE, null=False, blank=False)
    package_Price= models.PositiveIntegerField(default = 0)
    meal_Plans= models.TextField()
    package = models.ForeignKey(Packages,on_delete=models.CASCADE, null=True, blank=True,)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    duration = models.PositiveIntegerField(default=1)
    start_Date = models.DateField(null=False, blank=False)
    end_Date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
    	verbose_name = 'Hotel Package'
    	verbose_name_plural = 'Hotel Packages'

    def __str__(self):
         return f'{self.package} in {self.hotel}'


    def get_absolute_url(self):
        
        return reverse('package-list')

    @property
    def is_past_due(self):
        return date.today() > self.end_Date

    def meals_as_list(self):
        return self.meal_Plans.split('\n')


class Itinirery(models.Model):
    """Creates package itinirery details"""
    title = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    package = models.ForeignKey(Packages,on_delete = models.CASCADE, null=True, blank=True,)
    package_photo = models.ImageField(default='default.jpg', upload_to='itinirery_photos')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Package Itinireries'

    def __str__(self):
         return f'{self.title}-{self.package}'



class CartPackageItems(models.Model):
    cart = models.ForeignKey('Cart', on_delete = models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default = 1)
    hotel_package = models.ForeignKey(HotelPackages, on_delete = models.CASCADE, null=True, blank=True)
    line_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    CheckIn = models.DateField(null=True, blank=True)
    CheckOut = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp =models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
         return f'{self.hotel_package.hotel}'

    class Meta:
        verbose_name_plural = 'Pakage Cart Items'


    




