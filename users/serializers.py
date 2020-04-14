from rest_framework import serializers

from users import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user via API"""
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
