from django.db.models.signals import post_save
from .models import UserProfile, Profile
from django.dispatch import receiver


@receiver(post_save, sender=UserProfile)
def create_profile(sender, instance, created, **kwargs):
    profile = Profile.objects.filter(user=instance)

    if ((created and instance.from_api == False) and (not profile)):
        Profile.objects.create(
            user=instance)


@receiver(post_save, sender=UserProfile)
def save_profile(sender, instance, created, **kwargs):
    if instance.from_api == False:
        instance.profile.save()
