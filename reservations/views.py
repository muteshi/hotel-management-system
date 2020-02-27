from datetime import timedelta
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from hotels.models import Cart
from .models import Reservation, PackageReservation
import time, datetime
from .utils import id_generator, pack_id_generator
from hotels.models import Room, CartItems, HotelPackages, CartPackageItems



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

    except:
        return HttpResponseRedirect(reverse('cart'))


    if new_reservation.status == "Finished":

        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse('cart'))

    context = {"cart": cart, "reservation": new_reservation}
    template = "hotels/checkout.html"

    return render(request, template, context)


#checkout for package booking

@login_required
def package_check_out(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
       
    except:
        the_id = None
        return HttpResponseRedirect(reverse('package-cart'))

    try:
        new_reservation = PackageReservation.objects.get(cart=cart)

    except PackageReservation.DoesNotExist:
        new_reservation = PackageReservation()
        new_reservation.cart = cart
        new_reservation.user = request.user
        new_reservation.reservation_id = pack_id_generator()
        new_reservation.final_total =cart.total
        # new_reservation.status = "Finished"
        new_reservation.payment_option = "pay_on_checkin"
        new_reservation.save()

    except:
        return HttpResponseRedirect(reverse('package-cart'))


    if new_reservation.status == "Finished":

        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse('package-cart'))

    context = {"cart": cart, "reservation": new_reservation}
    template = "hotels/package_checkout.html"

    return render(request, template, context)


def add_to_cart(request, slug):
    request.session.set_expiry(1800)
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


#Add to cart package reservation
def package_add_to_cart(request, id):
    request.session.set_expiry(1800)
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
        package = HotelPackages.objects.get(id=id)
    except HotelPackages.DoesNotExist:
        pass
    except:
        pass

    #Capture users booking details from the booking form
    if request.method == "POST":
        qty = request.POST['qty']
        checkin = request.POST['checkin']
        cart_package_item = CartPackageItems.objects.create(cart=cart, hotel_package=package)
        CheckIn = datetime.datetime.strptime(checkin, "%m/%d/%Y").date()
        stay_duration = package.duration

       

        cart_package_item.quantity = qty
        cart_package_item.CheckIn = CheckIn
        cart_package_item.CheckOut = CheckIn + timedelta(days=stay_duration)
        cart_package_item.save()
        return HttpResponseRedirect(reverse("package-cart"))

    return HttpResponseRedirect(reverse("package-cart"))


