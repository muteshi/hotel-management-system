from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse
from users.models import UserProfile, Profile, UserTypes
from users import models


class UserDetailsSerializer(serializers.ModelSerializer):
    email_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = ('email_name', 'id', )

    def get_email_name(self, obj):
        return f'{obj.email}-{obj.name}'


class UserTypesSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserTypes
        fields = ("id", "name",)


class ActivateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = (
            'is_active',
        )


class UserProfileSerializer(serializers.ModelSerializer):

    """Serializes user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ['name', 'email', 'password', 'parent',
                  'from_api', 'is_active', ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user with encrypted password via API"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            from_api=validated_data['from_api'],
            password=validated_data['password'],
            parent=validated_data['parent'],
            is_active=validated_data['is_active'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = models.Profile
        fields = ['user',
                  'address',
                  'city',
                  'country',
                  'user_type',
                  'telephone_Number',
                  'organisation_name',
                  ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserProfile.objects.create(**user_data)
        user.set_password(user.password)
        user.save()
        profile = Profile.objects.create(user=user, **validated_data)
        return profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = [
            'address',
            'city',
            'country',
            'user_type',
            'telephone_Number',
            'commission',
            'organisation_name',
        ]


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and autheniticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided details')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class ProfileDetailsSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all())
    organisation_name = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    user_type_name = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    telephone_Number = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = ('name',
                  'email',
                  'parent',
                  'from_api',
                  'is_active',
                  'is_superuser',
                  'parent',
                  'id',
                  'profile',
                  'organisation_name',
                  'telephone_Number',
                  'city',
                  'country',
                  'address',
                  'user_type_name',
                  'user_type',

                  )
        # depth = 1

    def get_user_type_name(self, obj):
        try:
            return obj.profile.user_type.name
        except:
            pass

    def get_organisation_name(self, obj):
        try:
            return obj.profile.organisation_name
        except:
            pass

    def get_city(self, obj):
        try:
            return obj.profile.city
        except:
            pass

    def get_telephone_Number(self, obj):
        try:
            return obj.profile.telephone_Number
        except:
            pass

    def get_address(self, obj):
        try:
            return obj.profile.address
        except:
            pass

    def get_country(self, obj):
        try:
            return obj.profile.country
        except:
            pass

    def get_user_type(self, obj):
        try:
            return obj.profile.user_type.id
        except:
            pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff

        return token
