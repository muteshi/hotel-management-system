from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Hotels, Room


#signal to send email on successful property register
def property_created(sender, instance, created, *args, **kwargs):
	hotel = instance
	if created:
		#send an email
		hotel_is_created = Hotels.objects.get_or_create(hotel=hotel)
		if hotel_is_created:
			#create hash and send email
			
			hotel_is_created.property_register_email()

post_save.connect(hotel_is_created, sender=Hotels)