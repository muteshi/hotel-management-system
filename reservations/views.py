from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from hotels.models import Cart
from .models import Reservation
import time, datetime
from .utils import id_generator
from hotels.models import Room, CartItems



@login_required
def check_out(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
       
    except:
        the_id = None
        return HttpResponseRedirect(reverse('cart'))

    try:
        new_reservation = Reservation.objects.get(cart=cart)

    except Reservation.DoesNotExist:
        new_reservation = Reservation()
        new_reservation.cart = cart
        new_reservation.user = request.user
        new_reservation.reservation_id = id_generator()
        new_reservation.final_total =cart.total
        # new_reservation.status = "Finished"
        new_reservation.payment_option = "pay_on_checkin"
        new_reservation.save()


        #send email

        # context = {"cart": cart, "booking": new_reservation}
        # message = render_to_string("hotels/user_reservation_details.html", context)
        # plain_message = strip_tags(message)
        # subject = f"Your reservation details for #{new_reservation.reservation_id}"
        # mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_reservation.user.email], html_message=message)

    except:
        return HttpResponseRedirect(reverse('cart'))


    if new_reservation.status == "Finished":


        # booking = Reservation.objects.get(reservation_id=new_reservation.reservation_id)
        # # calculate the remaining number of rooms
        # new_rooms_total = booking.cart.cartitems_set.all()[0].rooms.total_Rooms - booking.cart.cartitems_set.all()[0].quantity
        # print(new_rooms_total)
        # print(booking.cart.cartitems_set.all()[0].quantity)

        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse('cart'))

    context = {"cart": cart, "reservation": new_reservation}
    template = "hotels/checkout.html"

    return render(request, template, context)


def add_to_cart(request, slug):
    request.session.set_expiry(900)
#Create  reservation order
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    request.session['cart_id']
    cart = Cart.objects.get(id=the_id)
    try:
        room = Room.objects.get(slug=slug)
    except Room.DoesNotExist:
        pass
    except:
        pass

    #Capture users booking details from the booking form
    if request.method == "POST":
        qty = request.POST['qty']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        cart_item = CartItems.objects.create(cart=cart, rooms=room)
        CheckIn = datetime.datetime.strptime(checkin, "%m/%d/%Y").date()
        CheckOut = datetime.datetime.strptime(checkout, "%m/%d/%Y").date()
        timedeltaSum = CheckOut - CheckIn
        stay_duration = timedeltaSum.days

        if stay_duration == 0:
            stay_duration += 1

        cart_item.quantity = qty
        cart_item.CheckIn = CheckIn
        cart_item.CheckOut = CheckOut
        cart_item.stay_duration = stay_duration
        cart_item.save()
        return HttpResponseRedirect(reverse("cart"))

    return HttpResponseRedirect(reverse("cart"))


# def reservation_details(request, id):
#     global new_reservation
#     """Display all hotels"""
#
#     context = {'booking': Reservation.objects.get(reservation_id=new_reservation)}
#     return render(request, 'hotels/reservation_details.html', context)
