import datetime
from datetime import timedelta, date
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.db.models import Min
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from hotels.models import Cart
from .models import Reservation, PackageReservation, ConferenceReservation
from .forms import BookingForm, ConferenceBookingForm
from .utils import id_generator, pack_id_generator
from hotels.models import Room, CartItems, HotelPackages, CartPackageItems, ConferenceRoom, CartConferenceItems


def hotel_room_booking_checkout(request):
    try:
        checkin = request.session['checkin']
        checkin = datetime.datetime.strptime(checkin, "%m/%d/%Y")
        checkout = request.session['checkout']
        checkout = datetime.datetime.strptime(checkout, "%m/%d/%Y")
        timedeltaSum = checkout - checkin
        StayDuration = timedeltaSum.days
        if (StayDuration == 0):
            StayDuration = 1

    except:
        pass

    context = {"checkin": checkin, 'title': 'Marvellous Ventures:Checkout',
               "checkout": checkout, "StayDuration": StayDuration, }
    template = "reservations/booking_form.html"

    return render(request, template, context)


def hotel_package_booking_checkout(request):
    template = "reservations/package_booking_form.html"

    return render(request, template)


def new_booking(request):
    """Record new room booking information"""
    try:
        # capture the information on the current cart
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('cart'))

    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # booking.cart = cart
            booking.reservation_id = id_generator()
            # booking.final_total =cart.total
            booking.save()

            # Send email on Successfull room booking
            name = form.cleaned_data.get('last_name')
            title = form.cleaned_data.get('title')
            email = form.cleaned_data.get('email')
            order_number = booking.reservation_id
            items = cart.cartitems_set.all()[0]
            context = {"name": name, "items": items, 'cart': cart,
                       'title': title.capitalize(), 'order_number': order_number}
            message = render_to_string(
                "reservations/room_reservation_success.html", context)
            plain_message = strip_tags(message)
            subject = f"Your booking details for {items}"
            mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                           email], html_message=message)

            # if user checks register_as_user register user

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
            package_booking.final_total = cart.total
            package_booking.save()
            name = form.cleaned_data.get('last_name')
            order_number = package_booking.reservation_id
            title = form.cleaned_data.get('title')
            email = form.cleaned_data.get('email')
            items = cart.cartpackageitems_set.all()[0]
            context = {"name": name, "items": items, 'cart': cart,
                       'title': title.capitalize(), 'order_number': order_number}
            message = render_to_string(
                "reservations/package_reservation_success.html", context)
            plain_message = strip_tags(message)
            subject = f"Your booking details for {items.hotel_package.package.title}"
            mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                           email], html_message=message)
            del request.session['cart_id']
            del request.session['items_total']
            return redirect('booking-success')
    else:
        form = BookingForm()

    return render(request, 'reservations/package_booking_new.html', {'form': form, 'cart': cart,
                                                                     'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
                                                                     })


def new_conference_booking(request):
    """Record new room booking information"""

    line_total = request.session.get('line_total')
    s_room_total = request.session.get('s_room_total')
    d_room_total = request.session.get('d_room_total')
    discount = request.session.get('discount')

    try:
        # capture the information on the current cart
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('conference-cart'))

    form = ConferenceBookingForm()
    if request.method == 'POST':
        form = ConferenceBookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.cart = cart
            booking.reservation_id = id_generator()
            booking.final_total = cart.total
            booking.save()

            # Send email on Successfull room booking
            name = form.cleaned_data.get('last_name')
            title = form.cleaned_data.get('organisation_name')
            email = form.cleaned_data.get('email')
            time = form.cleaned_data.get('start_time')
            guests = form.cleaned_data.get('name_of_guests')
            guests = guests.split('\n')
            order_number = booking.reservation_id
            items = cart.cartconferenceitems_set.all()[0]
            context = {"name": name, "items": items, 'cart': cart, 'title': title, 'order_number': order_number,
                       'time': time, 'guests': guests, 's_room_total': s_room_total, 'line_total': line_total, 'd_room_total': d_room_total}
            message = render_to_string(
                "reservations/meeting_room_reservation_email.html", context)
            plain_message = strip_tags(message)
            subject = f"Your booking details for {items}"
            mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                           email], html_message=message)

            # if user checks register_as_user register user

            del request.session['cart_id']
            del request.session['items_total']
            del request.session['s_room_total']
            del request.session['d_room_total']
            del request.session['discount']
            del request.session['line_total']
            return redirect('booking-success')
    else:
        form = ConferenceBookingForm()

    return render(request, 'reservations/conference_booking_new.html', {'form': form, 'cart': cart, 'line_total': line_total, ''
                                                                        'min': ConferenceRoom.objects.all().aggregate(Min('room_Price')),
                                                                        'd_room_total': d_room_total, 's_room_total': s_room_total,
                                                                        'discount': discount,
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
        new_reservation.final_total = cart.total
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


# checkout for package booking

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
        new_reservation.final_total = cart.total
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
# Create  reservation order
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

    # Capture users booking details from the booking form
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


# Add to cart package reservation
def package_add_to_cart(request, id):
    request.session.set_expiry(1800)
# Create  reservation order
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

    # Capture users booking details from the booking form
    if request.method == "POST":
        qty = request.POST['qty']
        checkin = request.POST['checkin']
        cart_package_item = CartPackageItems.objects.create(
            cart=cart, hotel_package=package)
        CheckIn = datetime.datetime.strptime(checkin, "%m/%d/%Y").date()
        stay_duration = package.duration

        cart_package_item.quantity = qty
        cart_package_item.CheckIn = CheckIn
        cart_package_item.CheckOut = CheckIn + timedelta(days=stay_duration)
        cart_package_item.save()
        return HttpResponseRedirect(reverse("package-cart"))

    return HttpResponseRedirect(reverse("package-cart"))


def booking_success(request):
    try:
        del request.session['checkin']
        del request.session['checkout']
        del request.session['adult']
        del request.session['child']
        del request.session['room']
        del request.session['is_conference']
    except:
        pass

    return render(request, 'reservations/booking_success.html')


def conference_add_to_cart(request, slug):
    request.session.set_expiry(1800)

# Create  reservation order
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    request.session['cart_id']
    cart = Cart.objects.get(id=the_id)
    # conference room
    try:
        room = ConferenceRoom.objects.get(slug=slug)
    except ConferenceRoom.DoesNotExist:
        pass
    except:
        pass

    # Capture users booking details from the booking form
    if request.method == "POST":

        checkin = request.POST['checkin']
        checkout = request.POST.get('checkout')
        guests = request.POST.get('qty')

        if not (checkin and guests and checkout):
            return redirect("conference-hotel-detail", room.hotel.slug)

        single_room = request.POST.get('single_hotel_room')
        if not single_room:
            single_room = None
        double_room = request.POST.get('double_hotel_room')
        if not double_room:
            double_room = None
        double_room_total = request.POST.get('double-guests')
        if not double_room_total:
            double_room_total = 0
        single_room_total = request.POST.get('single-guests')
        if not single_room_total:
            single_room_total = 0
        nights = request.POST.get('nights')
        if not nights:
            nights = 0
        RoomCheckIn = request.POST.get('checkindate')
        if not RoomCheckIn:
            RoomCheckIn = None

        cart_item = CartConferenceItems.objects.create(cart=cart, rooms=room)

        if RoomCheckIn != None:
            RoomCheckIn = datetime.datetime.strptime(
                RoomCheckIn, "%Y-%m-%d").date()
            present = datetime.datetime.now().date()
            if RoomCheckIn < present:
                messages.error(
                    request, f'You have selected a date in the past!')
                return redirect("conference-hotel-detail", room.hotel.slug)

        CheckIn = datetime.datetime.strptime(checkin, "%m/%d/%Y").date()

        CheckOut = datetime.datetime.strptime(checkout, "%m/%d/%Y").date()
        timedeltaSum = CheckOut - CheckIn
        conference_duration = timedeltaSum.days

        if conference_duration == 0:
            conference_duration += 1

        cart_item.guests = guests
        # get the primary key from the selected room
        if single_room != None:
            single_room = single_room.split('-')[0]
            cart_item.single_room = (
                Room.objects.get(id=int(single_room))).room_Name
            single_room_price = single_room.split('-')[0]
            cart_item.single_room_price = (Room.objects.get(
                id=int(single_room_price))).room_Price
            cart_item.single_room_total = int(single_room_total)
            cart_item.RoomCheckIn = RoomCheckIn
            cart_item.RoomCheckOut = RoomCheckIn + timedelta(days=int(nights))
            cart_item.nights = int(nights)

        if double_room != None:
            double_room_price = double_room.split('-')[0]
            cart_item.double_room_price = (Room.objects.get(
                id=int(double_room_price))).room_Price
            double_room = double_room.split('-')[0]
            cart_item.double_room = (
                Room.objects.get(id=int(double_room))).room_Name
            cart_item.double_room_total = int(double_room_total)
            cart_item.RoomCheckIn = RoomCheckIn
            cart_item.RoomCheckOut = RoomCheckIn + timedelta(days=int(nights))
            cart_item.nights = int(nights)

        if (double_room == None) and (single_room == None):
            cart_item.RoomCheckIn = None
            cart_item.RoomCheckOut = None
            cart_item.nights = 0

        cart_item.CheckIn = CheckIn
        cart_item.CheckOut = CheckOut
        cart_item.conference_duration = conference_duration

        cart_item.save()
        return HttpResponseRedirect(reverse("conference-cart"))

    return HttpResponseRedirect(reverse("conference-cart"))
