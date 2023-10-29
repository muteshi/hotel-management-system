from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from PIL import Image
from django.utils import timezone


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None, **extra_fields):
        """Creates a new user profile"""
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, name, password):
        """Creates a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self.db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)  # full name of the user
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, )
    from_api = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name_plural = 'Users'
        ordering = ('-created_at',)

    def get_full_name(self):
        """Retrieves user fullname"""
        return self.name

    def get_short_name(self):
        """Retrieves short name of the user"""
        return self.name

    def __str__(self):
        """Returns string representation of the user"""
        return self.email

    # def save(self, *args, **kwargs):
    #     """Override default save method"""
    #     super(UserProfile, self).save(*args, **kwargs)


class UserTypes(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'User types'

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    """Creates users profile information"""
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True,)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    address = models.CharField(max_length=255, null=True, blank=True,)
    city = models.CharField(max_length=255, null=True, blank=True,)
    country = models.CharField(max_length=255, null=True, blank=True,)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    commission = models.PositiveIntegerField(default=1)
    telephone_Number = models.CharField(max_length=20, null=True, blank=True,)
    email_confirmed = models.BooleanField(default=False)
    user_type = models.ForeignKey(
        UserTypes, null=True, blank=True, on_delete=models.CASCADE)
    organisation_name = models.CharField(default='N/A', max_length=255)

    class Meta:
        verbose_name_plural = 'User profiles'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user.name} Profile'

    def save(self, *args, **kwargs):
        """Override default save method"""
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            rgb_img = img.convert('RGB')
            rgb_img.save(self.image.path)
