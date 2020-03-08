import datetime
from datetime import timedelta, time
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.db.models import Min

from django.contrib.auth.decorators import login_required
from hotels.models import Cart
from .models import Reservation, PackageReservation
from .forms import BookingForm
from .utils import id_generator, pack_id_generator
from hotels.models import Room, CartItems, HotelPackages, CartPackageItems


def new_booking(request):
    """Record new room booking information"""
    try:
        the_id = request.session['cart_id'] #capture the information on the current cart
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('cart'))

    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.cart = cart
            booking.reservation_id = id_generator()
            booking.final_total =cart.total
            booking.save()

            #Send email on Successfull room booking
            name = form.cleaned_data.get('last_name')
            title = form.cleaned_data.get('title')
            email = form.cleaned_data.get('email')
            order_number = booking.reservation_id
            items = cart.cartitems_set.all()[0]
            context = {"name": name,"items": items, 'cart':cart, 'title': title.capitalize(), 'order_number': order_number}
            message = render_to_string("reservations/room_reservation_success.html", context)
            plain_message = strip_tags(message)
            subject = f"Your booking details for {items}"
            mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], html_message=message)

            #if user checks register_as_user register user 



            del request.session['cart_id']
            del request.session['items_total']
            return redirect('booking-success')
    else:
        form = BookingForm()

    return render(request, 'reservations/booking_new.html', {'form': form, 'cart': cart, 
                                                                'min': Room.objects.all().aggregate(Min('room_Price')),
                                                                    })

def new_package_booking(request):
	"""Record new package booking information"""
	try:
		the_id = request.session['cart_id'] 
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
		return HttpResponseRedirect(reverse('cart'))

	form = BookingForm()
	if request.method == 'POST':
		form = BookingForm(request.POST)
		if form.is_valid():
			package_booking = form.save(commit=False)
			package_booking.cart = cart
			package_booking.reservation_id = id_generator()
			package_booking.final_total =cart.total
			package_booking.save()
			name = form.cleaned_data.get('last_name')
			order_number = package_booking.reservation_id
			title = form.cleaned_data.get('title')
			email = form.cleaned_data.get('email')
			items = cart.cartpackageitems_set.all()[0]
			context = {"name": name,"items": items, 'cart':cart, 'title': title.capitalize(), 'order_number': order_number }
			message = render_to_string("reservations/package_reservation_success.html", context)
			plain_message = strip_tags(message)
			subject = f"Your booking details for {items.hotel_package.package.title}"
			mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], html_message=message)
			del request.session['cart_id']
			del request.session['items_total']
			return redirect('booking-success')
	else:
		form = BookingForm()

	return render(request, 'reservations/package_booking_new.html', {'form': form, 'cart': cart, 
	                                                                'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
	                                                                    })



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



def booking_success(request):
    return render(request, 'reservations/booking_success.html')


