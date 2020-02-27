import string
import random

from .models import Reservation, PackageReservation

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        reservation = Reservation.objects.get(reservation_id=the_id)
        id_generator()
    except Reservation.DoesNotExist:
        return the_id


def pack_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        reservation = PackageReservation.objects.get(reservation_id=the_id)
        id_generator()
    except PackageReservation.DoesNotExist:
        return the_id
