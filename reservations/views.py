import datetime
from datetime import timedelta, date
from django.shortcuts import render


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
