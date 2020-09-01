from datetime import date
from django.db import models
from django.utils import timezone
import datetime
from users.models import UserProfile
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify


from PIL import Image


class HotelTypes(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Hotel Types'

    def __str__(self):
        return f'{self.name}'


class Hotels(models.Model):
    # General Hotel details

    name = models.CharField(max_length=255, null=True,
                            blank=True)  # The name of the hotel
    property_photo = models.ImageField(
        default='default.jpg', upload_to='hotel_photos')
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    # hotel settings
    hotel_type = models.ForeignKey(
        HotelTypes, on_delete=models.CASCADE, null=True, blank=True,)
    vat = models.PositiveIntegerField(default=1, null=True, blank=True)
    star_rating = models.PositiveIntegerField(default=1, null=True, blank=True)

    # hotel management
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    featured_from = models.DateField(null=True, blank=True)
    featured_to = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=12, null=True, blank=True)
    checkin = models.TimeField(null=True, blank=True)
    checkout = models.TimeField(null=True, blank=True)
    policies = models.TextField(null=True, blank=True)
    has_conference = models.BooleanField(default=False)
    is_apartment = models.BooleanField(default=False)
    contact_person = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE,  default=1)

    # Hotel location
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    # hotel facilities fields
    airport_transport = models.BooleanField(
        default=False)
    night_club = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    swimming_pool = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    air_conditioner = models.BooleanField(default=False)
    laundry_services = models.BooleanField(default=False)
    bar_lounge = models.BooleanField(default=False)
    disabled_services = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    shuttle_bus_service = models.BooleanField(default=False)
    cards_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'slug')
        verbose_name_plural = 'Hotels'
        ordering = ('-created_at',)

    def __str__(self):
        """Prints the name of the Hotel"""
        return self.name

    @property
    def get_hotel_type_id(self):
        return self.hotel_type.id

    def get_absolute_url(self):
        # Redirects the form to photo uploads
        return reverse('photo-upload', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """Override default save method"""
        super().save(*args, **kwargs)


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
    image = models.ImageField(upload_to='hotel_photos')
    hotel = models.ForeignKey(
        Hotels, on_delete=models.CASCADE, null=True, blank=True,)

    class Meta:
        verbose_name_plural = 'Photos'

    def __str__(self):
        """Prints the name of the Photo"""
        return f'{self.hotel} photos'


class RoomTypes(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Room Types'

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    """Creates room details"""

    hotel = models.ForeignKey(
        Hotels, on_delete=models.CASCADE, null=True, blank=True,)
    room_type = models.ForeignKey(
        RoomTypes, on_delete=models.CASCADE, null=True, blank=True,)
    room_photo = models.ImageField(
        default='default.jpg', upload_to='room_photos')
    room_Name = models.CharField(max_length=200)
    room_details = models.CharField(max_length=500)
    max_adults = models.PositiveIntegerField(default=1)
    max_child = models.PositiveIntegerField(default=1)
    extra_beds = models.PositiveIntegerField(default=0)
    extra_bed_price = models.PositiveIntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)
    room_Price = models.PositiveIntegerField(default=1)
    total_Rooms = models.PositiveIntegerField(default=1)  # room quantity
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    is_conference_room = models.BooleanField(default=False)
    is_apartment = models.BooleanField(default=False)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    # Room ammenities
    free_toiletries = models.BooleanField(default=False)
    water_body_view = models.BooleanField(default=False)
    safe_deposit_box = models.BooleanField(default=False)
    lcd_tv = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)
    pay_tv = models.BooleanField(default=False)
    mini_bar = models.BooleanField(default=False)
    refrigerator = models.BooleanField(default=False)
    blackout_drapes = models.BooleanField(default=False)
    telephone = models.BooleanField(default=False)
    ironing_facilities = models.BooleanField(default=False)
    desk = models.BooleanField(default=False)
    hair_dryer = models.BooleanField(default=False)
    extra_towels = models.BooleanField(default=False)
    bathrobes = models.BooleanField(default=False)
    wake_up_service = models.BooleanField(default=False)
    electric_kettle = models.BooleanField(default=False)
    warddrobe = models.BooleanField(default=False)
    toilet_paper = models.BooleanField(default=False)
    slippers = models.BooleanField(default=False)
    toilet = models.BooleanField(default=False)
    alarm_clock = models.BooleanField(default=False)
    tea_coffee_maker = models.BooleanField(default=False)
    bathtub_shower = models.BooleanField(default=False)
    makeup_shaving_mirror = models.BooleanField(default=False)
    city_view = models.BooleanField(default=False)
    air_conditioner = models.BooleanField(default=False)
    cribs_infant_beds = models.BooleanField(default=False)
    daily_housekeeping = models.BooleanField(default=False)
    garden_view = models.BooleanField(default=False)

    # conference room ammenities
    projector = models.BooleanField(default=False)
    screen = models.BooleanField(default=False)
    conference_phone = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)
    speakers = models.BooleanField(default=False)
    whiteboard = models.BooleanField(default=False)
    sockets = models.BooleanField(default=False)
    coffee = models.BooleanField(default=False)
    monitors = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room_Name', 'slug')
        verbose_name_plural = 'Rooms'
        ordering = ['room_Price', 'updated_at', ]

    def __str__(self):
        return f'{self.room_type}({self.room_Name})-{self.hotel.name}'

    def get_absolute_url(self):
        # Redirects the form to photo uploads
        return reverse("hotel-detail", args=[self.hotel.slug])

    def save(self, *args, **kwargs):
        """Override default save method"""
        super().save(*args, **kwargs)


class RoomPhoto(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='room_photos')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True,)

    class Meta:
        verbose_name_plural = 'Room Photos'

    def __str__(self):
        """Prints the name of the Photo"""
        return f'{self.room} photos'


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


class CartItems(models.Model):
    cart = models.ForeignKey(
        'Cart', on_delete=models.CASCADE, null=True, blank=True)
    rooms = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    CheckIn = models.DateField(null=True, blank=True)
    CheckOut = models.DateField(null=True, blank=True)
    stay_duration = models.PositiveIntegerField(default=1)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f'{self.rooms.room_Name}-{self.rooms.room_type} room-{self.rooms.hotel.name}'

    class Meta:
        verbose_name_plural = 'Cart Items'


class Cart(models.Model):
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Cart id: {self.id}'


class HotelService(models.Model):
    hotel = models.ForeignKey(
        Hotels, on_delete=models.CASCADE, null=True, blank=True,)
    title = models.CharField(max_length=120)
    service_photo = models.ImageField(
        default='default.jpg', upload_to='service_photos')
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        """Prints the name of the service"""
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Services'


class PackageTypes(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Package Types'

    def __str__(self):
        return f'{self.name}'


class Packages(models.Model):
    """Stores all the information about a particular package"""

    title = models.CharField(max_length=255)  # The name of the package
    package_type = models.ForeignKey(
        PackageTypes, on_delete=models.CASCADE, null=True, blank=True,)
    city = models.CharField(max_length=255, null=True, blank=True,)
    country = models.CharField(max_length=255, null=True, blank=True,)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    description = models.TextField()
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
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


class PackagePhoto(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='package_photos')
    package = models.ForeignKey(
        Packages, on_delete=models.CASCADE, null=True, blank=True,)


class HotelPackages(models.Model):
    """Creates package itinirery details"""
    hotel = models.ForeignKey(
        Hotels, on_delete=models.CASCADE, null=False, blank=False)
    package_Price = models.PositiveIntegerField(default=0)
    meal_Plans = models.TextField()
    package = models.ForeignKey(
        Packages, on_delete=models.CASCADE, null=True, blank=True,)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    duration = models.PositiveIntegerField(default=1)
    start_Date = models.DateField(null=False, blank=False)
    end_Date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hotel Package'
        verbose_name_plural = 'Hotel Packages'
        ordering = ['package_Price', 'created_at', ]

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
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    package = models.ForeignKey(
        Packages, on_delete=models.CASCADE, null=True, blank=True,)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Package Itinireries'

    def __str__(self):
        return f'{self.title}-{self.package}'


class CartPackageItems(models.Model):
    cart = models.ForeignKey(
        'Cart', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    hotel_package = models.ForeignKey(
        HotelPackages, on_delete=models.CASCADE, null=True, blank=True)
    line_total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    CheckIn = models.DateField(null=True, blank=True)
    CheckOut = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f'{self.hotel_package.hotel}'

    class Meta:
        verbose_name_plural = 'Pakage Cart Items'


class Slider(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='slider_photos')
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_Date = models.DateField(auto_now_add=False, null=True, blank=True)
    end_Date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f'Slider {self.id}'

    class Meta:
        ordering = ['-start_Date', '-end_Date']
        verbose_name_plural = 'Sliders'


class ConferenceRoom(models.Model):
    """Creates conference room details"""

    hotel = models.ForeignKey(
        Hotels, on_delete=models.CASCADE, null=True, blank=True,)
    room_Name = models.CharField(max_length=200)
    room_details = models.TextField(null=True, blank=True,)
    room_Capacity = models.PositiveIntegerField(default=10)
    room_Price = models.PositiveIntegerField(default=2000)
    room_discount = models.DecimalField(
        max_digits=1000, decimal_places=2, default=1.00)

    # ammenities
    projector = models.BooleanField(default=False)
    screen = models.BooleanField(default=False)
    conference_phone = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)
    speakers = models.BooleanField(default=False)
    whiteboard = models.BooleanField(default=False)
    sockets = models.BooleanField(default=False)
    coffee = models.BooleanField(default=False)
    monitors = models.BooleanField(default=False)

    slug = models.SlugField(unique=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)

    class Meta:
        unique_together = ('room_Name', 'slug')
        verbose_name_plural = 'Conference Rooms'
        ordering = ('room_Price', 'created_at',)

    def __str__(self):
        return f'{self.room_Name}'

    def get_absolute_url(self):
        # Redirects the form to photo uploads
        return reverse('conferenceroom-list')

    def features_as_list(self):
        return self.room_details.split('\n')

    def save(self):
        """Override default save method"""
        super().save(*args, **kwargs)


class ConferenceRoomPhoto(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='room_photos')
    conferenceroom = models.ForeignKey(
        ConferenceRoom, on_delete=models.CASCADE, null=True, blank=True,)

    class Meta:
        verbose_name_plural = 'Conference Room Photos'

    def __str__(self):
        """Prints the name of the Photo"""
        return f'{self.conferenceroom} photos'


def create_conferenceroom_slug(instance, new_slug=None):
    slug = slugify(instance.room_Name)
    if new_slug is not None:
        slug = new_slug
    qs = ConferenceRoom.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f'{slug}-{qs.first().id}'
        return create_conferenceroom_slug(instance, new_slug=new_slug)
    return slug


def pre_save_conferenceroom_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_conferenceroom_slug(instance)


pre_save.connect(pre_save_conferenceroom_receiver, sender=ConferenceRoom)


class CartConferenceItems(models.Model):
    cart = models.ForeignKey(
        'Cart', on_delete=models.CASCADE, null=True, blank=True)
    rooms = models.ForeignKey(
        ConferenceRoom, on_delete=models.CASCADE, null=True, blank=True)  # conference room
    hotel_room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True)
    guests = models.PositiveIntegerField(default=1)
    double_room = models.CharField(max_length=255, null=True, blank=True)
    single_room = models.CharField(max_length=255, null=True, blank=True)
    double_room_total = models.PositiveIntegerField(
        null=True, blank=True)  # Number of rooms selected
    single_room_total = models.PositiveIntegerField(null=True, blank=True)
    single_room_price = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    double_room_price = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    total = models.DecimalField(
        max_digits=1000, decimal_places=2, default=0.00)
    CheckIn = models.DateField(null=True, blank=True)
    CheckOut = models.DateField(null=True, blank=True)
    RoomCheckIn = models.DateField(null=True, blank=True)
    RoomCheckOut = models.DateField(null=True, blank=True)
    conference_duration = models.PositiveIntegerField(default=1)
    nights = models.PositiveIntegerField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f'{self.rooms.room_Name}-{self.rooms.hotel.name}'

    class Meta:
        verbose_name_plural = 'Conference Cart Items'
