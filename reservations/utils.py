import string
import random

from .models import Reservation

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        reservation = Reservation.objects.get(reservation_id=the_id)
        id_generator()
    except Reservation.DoesNotExist:
        return the_id
