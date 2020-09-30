from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from hotels.models import (
    Hotels,
    HotelTypes,
    PackageTypes,
    Packages,
    HotelPackages,
    Itinirery,
    Room,
    RoomTypes,
    Photo,
    PackagePhoto,
    RoomPhoto,
)


class HotelAdminCreateSerializer(ModelSerializer):
    """
    Creates serializer object that has extra form fields that only super user have access to
    For instance featured or active

    """
    created_at = serializers.DateTimeField(read_only=True)
    last_modified = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(required=False, read_only=True)
    photo_count = serializers.SerializerMethodField()
    room_count = serializers.SerializerMethodField()
    hotel_hits = serializers.SerializerMethodField()

    class Meta:
        model = Hotels
        fields = (
            "name",
            "id",
            'photo_count',
            'room_count',
            "address",
            "city",
            'slug',
            "country",
            "featured_from",
            "featured_to",
            "mobile_number",
            "description",
            "has_conference",
            "is_apartment",
            "property_photo",
            "star_rating",
            "contact_person",
            "created_at",
            "last_modified",
            "active",
            "featured",
            "airport_transport",
            "night_club",
            "wifi",
            "parking",
            "swimming_pool",
            "restaurant",
            "gym",
            "air_conditioner",
            "laundry_services",
            "bar_lounge",
            "disabled_services",
            "elevator",
            "shuttle_bus_service",
            "cards_accepted",
            "checkin",
            "checkout",
            "policies",
            'hotel_type_id',
            'hotel_hits',
        )

    def get_room_count(self, obj):
        return obj.room_set.all().count()

    def get_photo_count(self, obj):
        return obj.photo_set.all().count()

    def create(self, validated_data):
        return Hotels.objects.create(**validated_data)

    def get_hotel_hits(self, obj):
        try:
            return obj.hit_count.hits
        except:
            pass


class HotelOwnerCreateSerializer(ModelSerializer):
    """
    Creates a serializer that contains form fields that can be accessed by the hotel owner
    """
    created_at = serializers.DateTimeField(read_only=True)
    last_modified = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(required=False, read_only=True)
    photo_count = serializers.SerializerMethodField()
    room_count = serializers.SerializerMethodField()
    hotel_hits = serializers.SerializerMethodField()

    class Meta:
        model = Hotels
        fields = (
            "name",
            "id",
            'photo_count',
            'room_count',
            "address",
            "city",
            'slug',
            "country",
            "featured_from",
            "featured_to",
            "mobile_number",
            "description",
            "has_conference",
            "is_apartment",
            "property_photo",
            "star_rating",
            "contact_person",
            "created_at",
            "last_modified",
            "airport_transport",
            "night_club",
            "wifi",
            "parking",
            "swimming_pool",
            "restaurant",
            "gym",
            "air_conditioner",
            "laundry_services",
            "bar_lounge",
            "disabled_services",
            "elevator",
            "shuttle_bus_service",
            "cards_accepted",
            "checkin",
            "checkout",
            "policies",
            'hotel_type_id',
            'hotel_hits',

        )

    def get_hotel_hits(self, obj):
        try:
            return obj.hit_count.hits
        except:
            pass

    def get_photo_count(self, obj):
        return obj.photo_set.all().count()

    def get_room_count(self, obj):
        return obj.room_set.all().count()

    def create(self, validated_data):
        return Hotels.objects.create(**validated_data)


class HotelSerializers(ModelSerializer):
    slug = serializers.SlugField(required=False, read_only=True)
    hotel_hits = serializers.SerializerMethodField()

    class Meta:
        model = Hotels
        fields = (
            "name",
            "id",
            "address",
            "city",
            "country",
            "mobile_number",
            "description",
            "has_conference",
            "is_apartment",
            "star_rating",
            "contact_person",
            "slug",
            "active",
            "featured",
            "hotel_type",
            "vat",
            "policies",
            "featured_from",
            "featured_to",
            "checkin",
            "checkout",
            "airport_transport",
            "night_club",
            "wifi",
            "parking",
            "swimming_pool",
            "restaurant",
            "gym",
            "air_conditioner",
            "laundry_services",
            "bar_lounge",
            "disabled_services",
            "elevator",
            "shuttle_bus_service",
            "cards_accepted",
            "checkin",
            "checkout",
            "policies",
            "policies",
            "hotel_hits",
        )

        def get_hotel_hits(self, obj):
            try:
                return obj.hit_count.hits
            except:
                pass


class HotelTypesSerializers(serializers.ModelSerializer):

    class Meta:
        model = HotelTypes
        fields = ("id", "name",)


class HotelSettingsSerializers(serializers.ModelSerializer):
    hotel_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Hotels
        fields = (
            "has_conference",
            "is_apartment",
            "star_rating",
            "hotel_type",
            "hotel_type_name",
            "vat",
            "id",
            "slug",
            "featured_from",
            "featured_to",
        )

    def get_hotel_type_name(self, obj):
        try:
            return obj.hotel_type.name
        except:
            pass


class HotelPolicySerializers(serializers.ModelSerializer):

    class Meta:
        model = Hotels
        fields = (
            "checkin",
            "checkout",
            "policies",
            "id",
            "slug",

        )


class HotelFacilitiesSerializers(ModelSerializer):

    class Meta:
        model = Hotels
        fields = (
            "airport_transport",
            "night_club",
            "id",
            "slug",
            "wifi",
            "parking",
            "swimming_pool",
            "restaurant",
            "gym",
            "air_conditioner",
            "laundry_services",
            "bar_lounge",
            "disabled_services",
            "elevator",
            "shuttle_bus_service",
            "cards_accepted",
        )


class HotelDetailSerializer(serializers.ModelSerializer):

    hotel_type_name = serializers.SerializerMethodField()
    hotel_hits = serializers.SerializerMethodField()

    class Meta:
        model = Hotels

        fields = (
            "name",
            "address",
            "id",
            "city",
            "vat",
            'hotel_type',
            'hotel_type_name',
            "country",
            "mobile_number",
            "description",
            "slug",
            "active",
            "featured_from",
            "featured_to",
            "has_conference",
            "is_apartment",
            "featured",
            "property_photo",
            "star_rating",
            "contact_person",
            "airport_transport",
            "night_club",
            "wifi",
            "parking",
            "swimming_pool",
            "restaurant",
            "gym",
            "air_conditioner",
            "laundry_services",
            "bar_lounge",
            "disabled_services",
            "elevator",
            "shuttle_bus_service",
            "cards_accepted",
            "checkin",
            "checkout",
            "policies",
            "hotel_hits",
        )

    def get_hotel_type_name(self, obj):
        try:
            return obj.hotel_type.name
        except:
            pass

    def get_hotel_hits(self, obj):
        try:
            return obj.hit_count.hits
        except:
            pass


class RoomTypesSerializers(serializers.ModelSerializer):

    class Meta:
        model = RoomTypes
        fields = ("id", "name",)


class RoomAmmenitiesSerializers(ModelSerializer):

    class Meta:
        model = Room
        fields = (
            'id',
            "free_toiletries",
            "bathrobes",
            "safe_deposit_box",
            "lcd_tv",
            "free_wifi",
            "pay_tv",
            "mini_bar",
            "refrigerator",
            "telephone",
            "ironing_facilities",
            "desk",
            "hair_dryer",
            "extra_towels",
            "bathrobes",
            "wake_up_service",
            "electric_kettle",
            "warddrobe",
            "toilet_paper",
            "slippers",
            "toilet",
            "blackout_drapes",
            "alarm_clock",
            "tea_coffee_maker",
            "bathtub_shower",
            "makeup_shaving_mirror",
            "city_view",
            "air_conditioner",
            "cribs_infant_beds",
            "daily_housekeeping",
            "garden_view",
            'projector',
            'screen',
            "water_body_view",
            'conference_phone',
            'water',
            'free_wifi',
            'speakers',
            'whiteboard',
            'sockets',
            'coffee',
            'monitors',

        )


class RoomSettingsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
            'id',
            "hotel",
            "room_type",
            "max_adults",
            "max_child",
            "extra_beds",
            "extra_bed_price",
            "room_Price",
            "total_Rooms",
            "active",
            "is_conference_room",
        )


class RoomSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(required=False, read_only=True)
    hotel_name = serializers.SerializerMethodField()
    room_type_name = serializers.SerializerMethodField()
    hotel_slug = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            'hotel',
            'hotel_name',
            'hotel_slug',
            "room_type",
            "room_type_name",
            "room_photo",
            "room_Name",
            "created_at",
            "updated_at",
            "total_Rooms",
            "room_details",
            "max_adults",
            "slug",
            "room_Price",
            "active",
            "is_conference_room",
            "is_apartment",
            'user',
            'id',

        )

    def get_hotel_name(self, obj):
        return obj.hotel.name

    def get_room_type_name(self, obj):
        try:
            return obj.room_type.name
        except:
            pass

    def get_hotel_slug(self, obj):
        return obj.hotel.slug

    def create(self, validated_data):
        return Room.objects.create(**validated_data)


class RoomDetailSerializer(ModelSerializer):
    room_type_name = serializers.SerializerMethodField()
    hotel_name = serializers.SerializerMethodField()
    hotelSlug = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "hotel",
            "hotel_name",
            'id',
            "room_photo",
            "room_Name",
            "room_details",
            "slug",
            "hotelSlug",
            "room_Price",
            "total_Rooms",
            "room_type",
            "room_type_name",
            "max_adults",
            "max_child",
            "extra_beds",
            "extra_bed_price",
            "total_Rooms",
            "is_conference_room",
            "is_apartment",
            "active",
            "free_toiletries",
            "water_body_view",
            "safe_deposit_box",
            "lcd_tv",
            "free_wifi",
            "pay_tv",
            "mini_bar",
            "refrigerator",
            "blackout_drapes",
            "telephone",
            "ironing_facilities",
            "desk",
            "hair_dryer",
            "extra_towels",
            "bathrobes",
            "wake_up_service",
            "electric_kettle",
            "warddrobe",
            "toilet_paper",
            "slippers",
            "toilet",
            "alarm_clock",
            "tea_coffee_maker",
            "bathtub_shower",
            "makeup_shaving_mirror",
            "city_view",
            "air_conditioner",
            "cribs_infant_beds",
            "daily_housekeeping",
            "garden_view",
            'projector',
            'screen',
            'conference_phone',
            'water',
            'free_wifi',
            'speakers',
            'whiteboard',
            'sockets',
            'coffee',
            'monitors',

        )

    def get_room_type_name(self, obj):
        try:
            return obj.room_type.name
        except:
            pass

    def get_hotel_name(self, obj):
        try:
            return obj.hotel.name
        except:
            pass

    def get_hotelSlug(self, obj):
        try:
            return obj.hotel.slug
        except:
            pass


class PackageTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PackageTypes
        fields = ("id", "name",)


class PackageSerializer(ModelSerializer):
    slug = serializers.SlugField(required=False, read_only=True)
    hotel_count = serializers.SerializerMethodField()
    itinirery_count = serializers.SerializerMethodField()
    package_type_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = Packages
        fields = (
            "title",
            'name',
            "package_type",
            'package_type_id',
            'hotel_count',
            'photo_count',
            'itinirery_count',
            "city",
            "country",
            "active",
            "featured",
            "description",
            "slug",
            'id',

        )

    def get_package_type_id(self, obj):
        return obj.package_type.id

    def get_name(self, obj):
        return obj.title

    def get_photo_count(self, obj):
        return obj.packagephoto_set.all().count()

    def get_hotel_count(self, obj):
        return obj.hotelpackages_set.all().count()

    def get_itinirery_count(self, obj):
        return obj.itinirery_set.all().count()


class ItinirerySerializer(ModelSerializer):
    package_slug = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()

    class Meta:
        model = Itinirery
        fields = (
            'title',
            'package',
            'package_slug',
            'package_name',
            'description',
            'id',

        )

    def get_package_name(self, obj):
        return obj.package.title

    def get_package_slug(self, obj):
        return obj.package.slug


class HotelPackageSerializer(ModelSerializer):
    hotel_name = serializers.SerializerMethodField()
    hotel_user = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    package_slug = serializers.SerializerMethodField()

    class Meta:
        model = HotelPackages
        fields = (
            "hotel",
            'hotel_name',
            'hotel_user',
            'package_slug',
            'package_name',
            "package_Price",
            "meal_Plans",
            "package",
            'is_past_due',
            "duration",
            "start_Date",
            "end_Date",
            'id',
        )

    def get_hotel_name(self, obj):
        return obj.hotel.name

    def get_hotel_user(self, obj):
        return obj.hotel.contact_person.id

    def get_package_name(self, obj):
        return obj.package.title

    def get_package_slug(self, obj):
        return obj.package.slug


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "image",
            "hotel",
        )


class RoomPhotoSerializer(ModelSerializer):
    class Meta:
        model = RoomPhoto
        fields = (
            "image",
            "room",
        )


class PackagePhotoSerializer(ModelSerializer):
    class Meta:
        model = PackagePhoto
        fields = (
            "image",
            "package",
        )
