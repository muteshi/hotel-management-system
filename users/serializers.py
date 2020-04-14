from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

from users import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name', 'password',)
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
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer fro the user authentication object"""
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
