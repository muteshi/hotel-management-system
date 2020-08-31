from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.models import UserProfile, UserTypes, Profile
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.tokens import account_activation_token


from reservations.models import (
    Booking,
    BookingItems,
    BookingSettings,
    BookingStatus,
    PaymentOptions
)


class BookingStatusSerializer(ModelSerializer):
    class Meta:
        model = BookingStatus
        fields = (
            'name',
            'id',
        )


class PayemntOptionsSerializer(ModelSerializer):
    class Meta:
        model = PaymentOptions
        fields = (
            'name',
            'id',
        )


class BookingItemSerializer(ModelSerializer):
    room_Name = serializers.SerializerMethodField()
    room_Price = serializers.SerializerMethodField()
    package_Price = serializers.SerializerMethodField()
    is_conference_room = serializers.SerializerMethodField()
    sub_total = serializers.DecimalField(
        max_digits=10000, decimal_places=2, localize=True)

    class Meta:
        model = BookingItems
        fields = (
            'rooms',
            'id',
            'qty',
            'room_Name',
            'hotel_package',
            'name',
            'room_Price',
            'package_Price',
            'total_guests',
            'is_conference_room',
            'sub_total',
            'checkin',
            'checkout',
            'stay_duration',
        )

    def get_room_Name(self, obj):
        try:
            return obj.rooms.room_Name
        except:
            pass

    def get_is_conference_room(self, obj):
        try:
            return obj.rooms.is_conference_room
        except:
            pass

    def get_room_Price(self, obj):
        try:
            return obj.rooms.room_Price
        except:
            pass

    def get_package_Price(self, obj):
        try:
            return obj.hotel_package.package_Price
        except:
            pass

    def create(self, validated_data):
        return BookingItems.objects.create(**validated_data)


class BookingsCreateSerializer(ModelSerializer):
    items = BookingItemSerializer(many=True)

    class Meta:
        model = Booking
        fields = (
            'items',
            'id',
            'guest_name',
            'company_name',
            'final_total',
            'payment_option',
            'commission_total',
            'hotel',
            'package',
            'user',
            'mobile_Number',
            'email',
            'special_requests',
        )

    def to_internal_value(self, data):
        if 'account' in data:
            account = data.pop('account', None)
            parent = account[2]['parent']
            owner = UserProfile.objects.filter(id=parent)[0]

            user = UserProfile.objects.create_user(
                name=account[0]['name'],
                email=account[1]['email'],
                parent=owner,
                password=account[3]['password'],
                from_api=account[4]['from_api'],
            )

            user.set_password(account[3]['password'])
            try:
                usertype = UserTypes.objects.filter(name='Individual')[0]
                user.save()
                profile = Profile.objects.filter(user=user)[0]
                profile.user_type = usertype if usertype else None
                profile.save()
                current_site = settings.SITE_URL
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                context = {"current_site": current_site,
                        "name": user.name, 'uid': uid, 'token': token}
                subject = 'Activate Your Account at Marvellous Ventures'
                message = render_to_string(
                    'users/account_activation_email.html', context)
                plain_message = strip_tags(message)
                mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                    user.email], html_message=message)
            except:
                pass
            

        return super(BookingsCreateSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        booking = Booking.objects.create(**validated_data)
        for item_data in items_data:
            booking.items.create(**item_data)
        bookingData = Booking.objects.get(id=booking.id)
        bookingItems = booking.items.all()
        context = {"items": bookingItems, 'booking': bookingData}
        room_reservation_template = "reservations/room_reservation_success.html"
        package_reservation_template = "reservations/package_reservation_success.html"
        message = render_to_string(
            package_reservation_template if booking.package else room_reservation_template, context)
        plain_message = strip_tags(message)
        subject = f"Your booking details for {booking.package.title if booking.package else booking.hotel.name}"
        mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
            booking.email], html_message=message)
        return booking


class BookingUpdateSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            'id',
            'guest_name',
            'final_total',
            'deposit',
            'booking_status',
            'payment_option',
            'hotel',
            'package',
            'user',
            'special_requests',
        )


class BookingDetailsSerializer(ModelSerializer):
    items = BookingItemSerializer(many=True)
    booking_status_id = serializers.SerializerMethodField()
    booking_status_name = serializers.SerializerMethodField()
    payment_option_name = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    final_total = serializers.DecimalField(
        max_digits=10000, decimal_places=2, localize=True)
    hotel_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format="%b %d, %Y", required=False, read_only=True)

    class Meta:
        model = Booking
        fields = (
            'items',
            'id',
            'reservation_id',
            'booking_status_id',
            'booking_status',
            'booking_status_name',
            'created_at',
            'payment_option',
            'payment_option_name',
            'hotel',
            'package',
            'package_name',
            'commission_total',
            'address',
            'city',
            'country',
            'final_total',
            'tax_total',
            'deposit',
            'invoice_number',
            'user',
            'guest_name',
            'hotel_name',
            'special_requests',
        )

    def get_package_name(self, obj):
        try:
            return obj.package.title
        except:
            pass

    def get_booking_status_id(self, obj):
        try:
            return obj.booking_status.id
        except:
            pass

    def get_hotel_name(self, obj):
        try:
            return obj.hotel.name
        except:
            pass

    def get_address(self, obj):
        try:
            return obj.hotel.address
        except:
            pass

    def get_city(self, obj):
        try:
            return obj.hotel.city
        except:
            pass

    def get_country(self, obj):
        try:
            return obj.hotel.country
        except:
            pass

    def get_payment_option_name(self, obj):
        try:
            return obj.payment_option.name
        except:
            pass

    def get_booking_status_name(self, obj):
        try:
            return obj.booking_status.name
        except:
            pass


class BookingItemDetailsSerializer(ModelSerializer):
    items = BookingItemSerializer(many=True)

    class Meta:
        model = Booking
        fields = (
            'items',
        )


class BookingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSettings
        fields = [
            'commission',
        ]
