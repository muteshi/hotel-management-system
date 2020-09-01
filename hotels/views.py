import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect, HttpResponseRedirect, Http404, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Hotels, Room, Packages, Itinirery, HotelPackages, CartPackageItems, Slider, ConferenceRoom, CartConferenceItems
from django.http import JsonResponse
from django.views import View
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core import mail
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RoomForm, PhotoForm, PackageForm, HotelPackagesForm, ItinireryForm, ConferenceRoomForm, HotelsForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from django.db.models import Min, Q
from .filters import HotelFilter, PackagesFilter


from .models import Photo, Cart, CartItems
from reservations.models import Reservation


def home(request):

    hotels = Hotels.objects.filter(featured=True)
    hotels = hotels.filter(has_conference=False)
    packages = Packages.objects.filter(featured=True)
    conference_hotels = Hotels.objects.filter(
        Q(has_conference=True) & Q(featured=True))

    p_lowest_prices = {}
    for i in packages:
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            p_lowest_prices[i.title] = price

    c_lowest_prices = {}
    for i in conference_hotels:
        if Room.objects.filter(hotel=i.id).exists():
            price = Room.objects.filter(hotel=i.id)
            price = price.filter(is_conference_room=True)
            try:
                c_lowest_prices[i.name] = price[0].room_Price
            except:
                pass

    lowest_prices = {}
    for i in hotels:
        if Room.objects.filter(hotel=i.id).exists():
            price = Room.objects.filter(hotel=i.id)
            price = price.filter(is_conference_room=False)
            try:
                lowest_prices[i.name] = price[0].room_Price
            except:
                pass

    context = {
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'sliders': Slider.objects.all(), 'hotels': hotels,
        'lowest_prices': lowest_prices,
        'p_lowest_prices': p_lowest_prices,
        'c_lowest_prices': c_lowest_prices,
        'conference_hotels': conference_hotels,
        'packages': packages,
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'title': 'Hotels, Safaris, Meetings, Events and cheap vacation packages'
    }
    return render(request, 'hotels/home.html', context)


def company(request):
    return render(request, 'hotels/company.html', {'title': 'About'})


def conference_hotels(request):
    """Display all conference venues"""
    hotels = Hotels.objects.filter(has_conference=True)
    hotels_filter = HotelFilter(request.GET, queryset=hotels)
    page = request.GET.get('page')
    paginator = Paginator(hotels_filter.qs, 3)

    try:
        hotel = paginator.page(page)
    except PageNotAnInteger:
        hotel = paginator.page(1)
    except EmptyPage:
        hotel = paginator.page(paginator.num_pages)
    rooms = Hotels.objects.filter(has_conference=True).annotate(
        min_price=Min('room__room_Price'))
    lowest_prices = {}
    for i in Hotels.objects.filter(has_conference=True):
        if Room.objects.filter(hotel=i.id).exists():
            price = Room.objects.filter(hotel=i.id)
            price = price.filter(is_conference_room=True)
            try:
                lowest_prices[i.name] = price[0].room_Price
            except:
                pass

    tomorrow = (datetime.date.today() +
                datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    today = datetime.date.today().strftime("%m/%d/%Y")
    checkin = request.session['checkin'] if (
        'checkin' in request.session and request.session['checkin'] != None) else today
    checkin = datetime.datetime.strptime(checkin, "%m/%d/%Y")
    checkout = request.session['checkout'] if 'checkout' in request.session else tomorrow
    checkout = datetime.datetime.strptime(checkout, "%m/%d/%Y")
    timedeltaSum = checkout-checkin
    StayDuration = 1 if timedeltaSum.days == 0 else timedeltaSum.days

    context = {
        'hotels_filter': hotels_filter,
        'min': Room.objects.filter(is_conference_room=True).aggregate(Min('room_Price')),
        'lowest_prices': lowest_prices,
        'hotels': hotel,
        'paginator': paginator,
        'title': 'Meetings, Team Building, Conference rooms, Events and more..',
        'checkin': checkin,
        'checkout': checkout,
        'StayDuration': StayDuration

    }
    return render(request, 'hotels/conference_hotels.html', context)


def package_main_list(request):
    """Display all packages according to the chosen criteria"""

    packages = Packages.objects.all()
    packages_filter = PackagesFilter(request.GET, queryset=packages)
    paginator = Paginator(packages_filter.qs, 9)
    page = request.GET.get('page')
    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    try:
        checkin = request.GET.get('checkin')
        checkin = request.session['checkin']
        checkin = datetime.datetime.strptime(checkin, "%m/%d/%Y")
    except:
        pass

    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.title] = price

    context = {
        'packages': packages,
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'lowest_prices': lowest_prices,
        'paginator': paginator,
        'packages_filter': packages_filter,
        'title': 'Honeymoon deals, Easter offers, Coast deals and more..'
    }
    return render(request, 'hotels/packages.html', context)


def single(request, slug):
    """Display all hotels"""
    # hotel = Hotels.objects.all(slug=slug)
    context = {
        'hotels': Hotels.objects.all()
    }
    return render(request, 'hotels/hotels_detail.html', context)


class HotelsListView(ListView):
    """Displays all hotels on /hotels page"""
    model = Hotels
    template_name = 'hotels/hotels.html'
    context_object_name = 'hotels'
    ordering = ['-created_at']
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(HotelsListView, self).get_context_data(*args, **kwargs)
        hotels = Hotels.objects.all()
        hotels_filter = HotelFilter(self.request.GET, queryset=hotels)
        page = self.request.GET.get('page')
        paginator = Paginator(hotels_filter.qs, self.paginate_by)

        try:
            hotel = paginator.page(page)
        except PageNotAnInteger:
            hotel = paginator.page(1)
        except EmptyPage:
            hotel = paginator.page(paginator.num_pages)

        context['hotels'] = hotel
        context['hotels_filter'] = hotels_filter
        context['paginator'] = paginator
        context['title'] = 'Cheapest hotels in Kenya and East Africa'
        try:
            checkin = self.request.session['checkin']
            context['checkin'] = datetime.datetime.strptime(
                checkin, "%m/%d/%Y")
            checkout = self.request.session['checkout']
            context['checkout'] = datetime.datetime.strptime(
                checkout, "%m/%d/%Y")
            timedeltaSum = datetime.datetime.strptime(
                checkout, "%m/%d/%Y") - datetime.datetime.strptime(checkin, "%m/%d/%Y")
            context['StayDuration'] = 1 if timedeltaSum.days == 0 else timedeltaSum.days
        except:
            pass

        lowest_prices = {}
        for i in Hotels.objects.all():
            if Room.objects.filter(hotel=i.id).exists():
                price = Room.objects.filter(hotel=i.id)
                price = price.filter(is_conference_room=False)
                try:
                    lowest_prices[i.name] = price[0].room_Price
                except:
                    pass

        context['min'] = Room.objects.all().aggregate(Min('room_Price'))

        context['lowest_prices'] = lowest_prices

        return context


class ApartmentListView(ListView):
    """Displays all apartments on /apartment page"""
    model = Hotels
    template_name = 'hotels/apartments.html'
    context_object_name = 'apartments'
    ordering = ['-created_at']
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(ApartmentListView, self).get_context_data(
            *args, **kwargs)
        hotels = Hotels.objects.filter(is_apartment=True)
        hotels_filter = HotelFilter(self.request.GET, queryset=hotels)
        page = self.request.GET.get('page')
        paginator = Paginator(hotels_filter.qs, self.paginate_by)

        try:
            hotel = paginator.page(page)
        except PageNotAnInteger:
            hotel = paginator.page(1)
        except EmptyPage:
            hotel = paginator.page(paginator.num_pages)

        context['hotels'] = hotel
        context['hotels_filter'] = hotels_filter
        context['paginator'] = paginator
        context['title'] = 'Apartments, Villas and more...'
        try:
            checkin = self.request.session['checkin']
            context['checkin'] = datetime.datetime.strptime(
                checkin, "%m/%d/%Y")
            checkout = self.request.session['checkout']
            context['checkout'] = datetime.datetime.strptime(
                checkout, "%m/%d/%Y")
            timedeltaSum = datetime.datetime.strptime(
                checkout, "%m/%d/%Y") - datetime.datetime.strptime(checkin, "%m/%d/%Y")
            context['StayDuration'] = 1 if timedeltaSum.days == 0 else timedeltaSum.days
        except:
            pass

        lowest_prices = {}
        for i in Hotels.objects.filter(is_apartment=True):
            if Room.objects.filter(hotel=i.id).exists():
                price = Room.objects.filter(hotel=i.id)[0].room_Price
                lowest_prices[i.name] = price

        context['min'] = Room.objects.filter(
            is_apartment=True).aggregate(Min('room_Price'))

        context['lowest_prices'] = lowest_prices

        return context


class CityHotelsListView(ListView):
    """Displays hotels in a specific town/city"""
    model = Hotels
    template_name = 'hotels/hotels_by_city.html'
    context_object_name = 'hotels'
    ordering = ['-created_at']
    paginate_by = 9

    def get_queryset(self):
        hotel_by_city = get_object_or_404(Hotels, slug=self.kwargs.get('slug'))
        return Hotels.objects.filter(city=hotel_by_city.city).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super(HotelsListView, self).get_context_data(*args, **kwargs)
        hotels = Hotels.objects.all()
        paginator = Paginator(hotels, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            hotel = paginator.page(page)
        except PageNotAnInteger:
            hotel = paginator.page(1)
        except EmptyPage:
            hotel = paginator.page(paginator.num_pages)

        context['hotels'] = hotel

        lowest_prices = {}
        for i in Hotels.objects.all():
            if Room.objects.filter(hotel=i.id).exists():
                price = Room.objects.filter(hotel=i.id)[0].room_Price
                lowest_prices[i.name] = price

        context['min'] = Room.objects.all().aggregate(Min('room_Price'))
        context['lowest_prices'] = lowest_prices
        context['hotels_by_city'] = hotels_by_city

        return context


def search(request):  # Accomodation search
    checkin = request.GET.get('checkin')
    request.session['checkin'] = checkin
    checkout = request.GET.get('checkout')
    request.session['checkout'] = checkout
    adult = request.GET.get('adult')
    request.session['adult'] = adult
    child = request.GET.get('child')
    request.session['child'] = child
    room = request.GET.get('room')
    request.session['room'] = room
    search = request.GET.get('search')
    request.session['search'] = search

    try:
        search_text = request.GET.get('search')
        # print(search_text)

    except:
        search_text = None

    if search_text:
        results = Hotels.objects.filter(Q(city__icontains=search_text) | Q(
            name__icontains=search_text) | Q(country__icontains=search_text))
        hotels_filter = HotelFilter(request.GET, queryset=results)

    else:
        results = Hotels.objects.all()
        hotels_filter = HotelFilter(request.GET, queryset=results)

    page = request.GET.get('page', 1)
    paginator = Paginator(hotels_filter.qs, 3)
    template = 'hotels/search_results.html'
    try:
        hotels = paginator.page(page)
    except PageNotAnInteger:
        hotels = paginator.page(1)
    except EmptyPage:
        hotels = paginator.page(paginator.num_pages)
    lowest_prices = {}
    for i in Hotels.objects.all():
        if Room.objects.filter(hotel=i.id).exists():
            price = Room.objects.filter(hotel=i.id)[0].room_Price
            lowest_prices[i.name] = price
    hotel_count = Hotels.objects.all().count()
    conference_count = Hotels.objects.filter(has_conference=True).count()
    apartment_count = Hotels.objects.filter(is_apartment=True).count()
    print(apartment_count)
    context = {
        'hotels': hotels,
        'hotel_count': hotel_count,
        'conference_count': conference_count,
        'apartment_count': apartment_count,
        'hotels_filter': hotels_filter,
        'lowest_prices': lowest_prices,
        'search_text': search_text,
        'paginator': paginator,
        'title': f'Search results for {search_text}'
    }

    return render(request, template, context)


def search_conference_venues(request):  # Search meeting venues
    checkin = request.GET.get('checkin')
    request.session['checkin'] = checkin
    checkout = request.GET.get('checkout')
    request.session['checkout'] = checkout
    adult = request.GET.get('adult')
    request.session['adult'] = adult
    child = request.GET.get('child')
    request.session['child'] = child
    room = request.GET.get('room')
    request.session['room'] = room
    search = request.GET.get('search')
    request.session['search'] = search
    try:
        search_text = request.GET.get('search')
    except:
        search_text = None

    if search_text:
        results = Hotels.objects.filter(Q(city__icontains=search_text) | Q(
            name__icontains=search_text) | Q(country__icontains=search_text) & Q(has_conference=True))
        hotels_filter = HotelFilter(request.GET, queryset=results)

    else:
        results = Hotels.objects.filter(has_conference=True)
        hotels_filter = HotelFilter(request.GET, queryset=results)

    page = request.GET.get('page', 1)
    paginator = Paginator(hotels_filter.qs, 3)
    template = 'hotels/search_conference_venues.html'
    try:
        hotels = paginator.page(page)
    except PageNotAnInteger:
        hotels = paginator.page(1)
    except EmptyPage:
        hotels = paginator.page(paginator.num_pages)
    lowest_prices = {}
    for i in Hotels.objects.filter(has_conference=True):
        if Room.objects.filter(hotel=i.id).exists():
            price = Room.objects.filter(Q(hotel=i.id) & Q(
                is_conference_room=True))[0].room_Price
            lowest_prices[i.name] = price
    context = {
        'hotels': hotels,
        'hotels_filter': hotels_filter,
        'lowest_prices': lowest_prices,
        'search_text': search_text,
        'paginator': paginator,
        'title': f'Search results for {search_text}'
    }

    return render(request, template, context)


def search_packages(request):  # Search packages
    checkin = request.GET.get('checkin')
    request.session['checkin'] = checkin
    guests = request.GET.get('guests')
    request.session['guests'] = guests
    search = request.GET.get('search')
    request.session['search'] = search
    try:
        search_text = request.GET.get('search')
    except:
        search_text = None

    if search_text:
        results = Packages.objects.filter(Q(city__icontains=search_text))
        packages_filter = PackagesFilter(request.GET, queryset=results)

    else:
        results = Packages.objects.all()
        packages_filter = PackagesFilter(request.GET, queryset=results)

    page = request.GET.get('page', 1)
    paginator = Paginator(packages_filter.qs, 9)
    template = 'hotels/search_packages.html'
    try:
        packages = paginator.page(page)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)
    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.title] = price
    context = {
        'packages': packages,
        'packages_filter': packages_filter,
        'lowest_prices': lowest_prices,
        'search_text': search_text,
        'paginator': paginator,
        'title': f'Search results for {search_text}'
    }

    return render(request, template, context)


class RoomListView(LoginRequiredMixin, ListView):
    """List select all rooms"""
    model = Room
    template_name = 'hotels/room_list.html'
    context_object_name = 'rooms'
    # ordering = ['-date_posted']
    # paginate_by = 1

    def get_queryset(self):
        user = self.request.user
        queryset = Room.objects.filter(user=user)
        return queryset


class HotelsDetailView(DetailView):
    """List all details of the hotel"""
    model = Hotels

    def get_context_data(self, *args, **kwargs):
        context = super(HotelsDetailView, self).get_context_data(
            *args, **kwargs)
        lowest_prices = {}
        for i in Hotels.objects.all():
            if Room.objects.filter(hotel=i.id).exists():
                price = Room.objects.filter(hotel=i.id)
                price = price.filter(is_conference_room=False)
                try:
                    lowest_prices[i.name] = price[0].room_Price
                except:
                    pass

        context['hotels'] = Hotels.objects.all()
        context['min'] = Room.objects.all().aggregate(Min('room_Price'))
        context['lowest_prices'] = lowest_prices
        context['title'] = self.get_object().name
        tomorrow = (datetime.date.today() +
                    datetime.timedelta(days=1)).strftime("%m/%d/%Y")
        today = datetime.date.today().strftime("%m/%d/%Y")
        checkin = self.request.GET.get(
            'checkin') if self.request.GET else today
        self.request.session['checkin'] = checkin
        context['checkin'] = datetime.datetime.strptime(
            checkin, "%m/%d/%Y")
        checkout = self.request.GET.get(
            'checkout') if self.request.GET else tomorrow
        self.request.session['checkout'] = checkout
        context['checkout'] = datetime.datetime.strptime(
            checkout, "%m/%d/%Y")

        timedeltaSum = datetime.datetime.strptime(
            checkout, "%m/%d/%Y") - datetime.datetime.strptime(checkin, "%m/%d/%Y")
        context['StayDuration'] = 1 if timedeltaSum.days == 0 else timedeltaSum.days
        is_conference = False
        self.request.session['is_conference'] = is_conference
        context['is_conference'] = is_conference

        return context


class ApartmentDetailView(DetailView):
    """List all details of the apartment"""
    model = Hotels

    def get_context_data(self, *args, **kwargs):
        context = super(ApartmentDetailView, self).get_context_data(
            *args, **kwargs)
        lowest_prices = {}
        for i in Hotels.objects.filter(is_apartment=True):
            if Room.objects.filter(Q(is_apartment=True) & Q(hotel=i.id)).exists():
                price = Room.objects.filter(Q(is_apartment=True) & Q(hotel=i.id))[
                    0].room_Price
                lowest_prices[i.name] = price

        context['hotels'] = Hotels.objects.filter(is_apartment=True)
        context['min'] = Room.objects.filter(
            Q(is_apartment=True) & Q(hotel=i.id)).aggregate(Min('room_Price'))
        context['lowest_prices'] = lowest_prices
        context['title'] = self.get_object().name
        tomorrow = (datetime.date.today() +
                    datetime.timedelta(days=1)).strftime("%m/%d/%Y")
        today = datetime.date.today().strftime("%m/%d/%Y")

        checkin = self.request.GET.get(
            'checkin') if self.request.GET else today
        print(checkin)
        self.request.session['checkin'] = checkin
        print(checkin)
        context['checkin'] = datetime.datetime.strptime(
            checkin, "%m/%d/%Y")
        checkout = self.request.GET.get(
            'checkout') if self.request.GET else tomorrow
        self.request.session['checkout'] = checkout
        context['checkout'] = datetime.datetime.strptime(
            checkout, "%m/%d/%Y")

        timedeltaSum = datetime.datetime.strptime(
            checkout, "%m/%d/%Y") - datetime.datetime.strptime(checkin, "%m/%d/%Y")
        context['StayDuration'] = 1 if timedeltaSum.days == 0 else timedeltaSum.days
        is_conference = False
        self.request.session['is_conference'] = is_conference
        context['is_conference'] = is_conference

        return context


class ConferenceHotelsDetailView(DetailView):
    """List all details of the hotel"""
    model = Hotels
    template_name = 'hotels/conference_hotel_details.html'

    def get_context_data(self, *args, **kwargs):

        context = super(ConferenceHotelsDetailView,
                        self).get_context_data(*args, **kwargs)
        lowest_prices = {}
        for i in Hotels.objects.all():
            if Room.objects.filter(hotel=i.id).exists():
                price = Room.objects.filter(hotel=i.id)
                price = price.filter(is_conference_room=True)
                try:
                    lowest_prices[i.name] = price[0].room_Price
                except:
                    pass

        context['hotels'] = Hotels.objects.all()
        context['min'] = Room.objects.filter(is_conference_room=True
                                             ).aggregate(Min('room_Price'))
        context['lowest_prices'] = lowest_prices
        context['title'] = self.get_object().name
        is_conference = True
        self.request.session['is_conference'] = is_conference
        context['is_conference'] = is_conference
        tomorrow = (datetime.date.today() +
                    datetime.timedelta(days=1)).strftime("%m/%d/%Y")
        today = datetime.date.today().strftime("%m/%d/%Y")
        checkin = self.request.GET.get(
            'checkin') if self.request.GET else today
        self.request.session['checkin'] = checkin
        context['checkin'] = datetime.datetime.strptime(
            checkin, "%m/%d/%Y")
        checkout = self.request.GET.get(
            'checkout') if self.request.GET else tomorrow
        self.request.session['checkout'] = checkout
        context['checkout'] = datetime.datetime.strptime(
            checkout, "%m/%d/%Y")
        timedeltaSum = datetime.datetime.strptime(
            checkout, "%m/%d/%Y") - datetime.datetime.strptime(checkin, "%m/%d/%Y")
        context['StayDuration'] = 1 if timedeltaSum.days == 0 else timedeltaSum.days
        is_conference = True
        self.request.session['is_conference'] = is_conference
        context['is_conference'] = is_conference

        return context


class PackagesDetailView(DetailView):
    """List all details of the hotel"""
    model = Packages

    def get_context_data(self, *args, **kwargs):
        context = super(PackagesDetailView, self).get_context_data(
            *args, **kwargs)
        lowest_prices = {}
        for i in Packages.objects.all():
            if HotelPackages.objects.filter(package=i.id).exists():
                price = HotelPackages.objects.filter(package=i.id)[
                    0].package_Price
                lowest_prices[i.title] = price

        context['packages'] = Packages.objects.all()
        context['lowest_prices'] = lowest_prices
        context['title'] = self.get_object().title
        today = str(datetime.date.today())

        try:
            checkin = self.request.session['checkin'] if 'checkin' in self.request.session else today
            checkin = datetime.datetime.strptime(checkin, "%Y-%m-%d")
            context['checkin'] = checkin
            is_conference = False
            self.request.session['is_conference'] = is_conference
            context['is_conference'] = is_conference
        except:
            pass

        return context


class HotelsCreateView(LoginRequiredMixin, CreateView):
    """Creates hotels form"""
    model = Hotels
    form_class = HotelsForm

    def form_valid(self, form):
        hotel = form.save(commit=False)
        hotel.contact_person = self.request.user
        hotel.save()
        # messages.success(self.request, f'You have successfully created {self.hotel.name}!')
        # Send email on Successfull property creation
        property_url = "%s/%s" % (settings.SITE_URL,
                                  reverse("hotel-detail", args=[hotel.slug]))
        context = {"property_url": property_url,
                   "user":  hotel.contact_person.name, }
        message = render_to_string(
            "hotels/property_register_success.html", context)
        plain_message = strip_tags(message)
        subject = f"Registration details for {hotel.name}"
        mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                       hotel.contact_person.email], html_message=message)

        return super().form_valid(form)


class HotelsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update all details of the hotel"""
    model = Hotels
    template_name = "hotels/edit_hotel.html"
    context_object_name = 'hotel'
    fields = [
        'name',
        'name',
        'address',
        'city',
        'country',
        'mobile_number',
        'description',
        'star_rating',
        'property_photo',
    ]

    def form_valid(self, form):
        hotel = form.save(commit=False)
        hotel.last_modified = timezone.now()
        hotel.contact_person = self.request.user
        hotel.save()
        return redirect("hotel-detail", hotel.slug)

    def test_func(self):
        hotel = self.get_object()
        if self.request.user == hotel.contact_person:
            return True
        return False


class RoomUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update all details of the hotel"""
    model = Room
    template_name = "hotels/edit_room.html"
    context_object_name = 'room'
    fields = ('room_type', 'room_Name', 'max_adults', 'room_Price',
              'total_Rooms', 'room_details', 'room_photo',)

    def form_valid(self, form):
        room = form.save(commit=False)
        room.last_modified = timezone.now()
        room.user = self.request.user
        room.save()
        return redirect("hotel-detail", room.hotel.slug)

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.user:
            return True
        return False


class ConferenceRoomUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update all details of the conference room"""
    model = ConferenceRoom
    fields = ('room_Name', 'room_Capacity', 'room_Price',
              'room_discount', 'room_photo', 'room_details',)
    template_name = "hotels/edit_conferenceroom.html"
    success_message = "%(room_Name)s was updated successfully"
    context_object_name = 'conference_room'

    def form_valid(self, form):
        room = form.save(commit=False)
        room.last_modified = timezone.now()
        room.user = self.request.user
        room.save()
        return redirect("conference-hotel-detail", room.hotel.slug)

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.user:
            return True
        return False


class HotelsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a hotel"""
    model = Hotels
    success_url = '/hotels/'

    def test_func(self):
        hotel = self.get_object()
        if self.request.user == hotel.contact_person:
            return True
        return False


class RoomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a room"""
    model = Room

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(RoomDeleteView, self).get_context_data(**kwargs)
        context[next] = self.request.POST.get('previous_page')
        return context

    def get_success_url(self):
        redirect_to = self.request.POST.get('previous_page')
        return redirect_to


@login_required
def new_room(request):
    if request.method == 'POST':
        form = RoomForm(request.user,
                        request.POST,
                        request.FILES
                        )
        if form.is_valid():
            room = form.save(commit=False)
            room.user = request.user
            room.save()
            room_Name = form.cleaned_data.get('room_Name')
            room_type = form.cleaned_data.get('room_type')
            messages.success(
                request, f'You have successfully created {room_Name}-{room_type} room!')

            return redirect("hotel-detail", room.hotel.slug)
    else:
        form = RoomForm(request.user)

    return render(request, 'hotels/room_form.html', {'form': form})


@login_required
def new_conferenceroom(request):
    if request.method == 'POST':
        cform = ConferenceRoomForm(request.user,
                                   request.POST,
                                   request.FILES
                                   )
        if cform.is_valid():
            room = cform.save(commit=False)
            room.user = request.user
            room.conference = True
            room.save()

            return redirect("conference-hotel-detail", room.hotel.slug)
    else:
        cform = ConferenceRoomForm(request.user)

    return render(request, 'hotels/conferenceroom_form.html', {'cform': cform})


class ConferenceRoomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a room"""
    model = ConferenceRoom

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.user:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ConferenceRoomDeleteView,
                        self).get_context_data(**kwargs)
        context[next] = self.request.POST.get('previous_page')
        return context

    def get_success_url(self):
        redirect_to = self.request.POST.get('previous_page')
        return redirect_to


class PhotoUploadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        photos_list = Photo.objects.all()
        return render(self.request, 'hotels/uploads.html', {'photos': photos_list})

    def post(self, request, pk):
        """Handles photo uploads and assign them to the correct user and hotel"""
        form = PhotoForm(self.request.POST,
                         self.request.FILES, self.request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            try:
                hotel = Hotels.objects.get(
                    contact_person=self.request.user, id=self.kwargs.get('pk'))
            except Hotels.DoesNotExist:
                raise Http404
            photo.hotel = hotel
            photo.save()
            data = {'is_valid': True, 'name': photo.file.name,
                    'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


def bookRoom(request):

    FirstDate = request.session['checkin']
    SecDate = request.session['checkout']
    # #
    Checkin = datetime.datetime.strptime(FirstDate, "%Y-%m-%d").date()
    Checkout = datetime.datetime.strptime(SecDate, "%Y-%m-%d").date()
    timedeltaSum = Checkout - Checkin
    #
    StayDuration = timedeltaSum.days
    #
    Hotel = Hotels.objects.get(id=hotelid)
    theRoom = Room.objects.get(id=roomid)
    #
    price = theRoom.room_Price
    TotalCost = StayDuration * price

    context = {'checkin': Checkin, 'checkout': Checkout, 'stayduration': StayDuration, 'hotel': Hotel, 'room': theRoom, 'price': price,
               'totalcost': TotalCost}
    return render(request, 'hotels_detail', context)


def reservations(request):

    template = "hotels/reservations.html"
    context = {}
    return render(request, template, context)

# room reservation


def view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        for item in cart.cartitems_set.all():
            line_total = float(item.rooms.room_Price) * \
                item.quantity * item.stay_duration
            new_total += line_total
        request.session['items_total'] = cart.cartitems_set.count()
        cart.total = new_total
        cart.save()
        context = {"cart": cart}
    else:
        empty_message = "You are yet to make any reservation"
        context = {"empty": True, "empty_message": empty_message,
                   "title": "Room Reservation"}

    template = "hotels/booking.html"
    return render(request, template, context)


# package reservation
def package_view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        for item in cart.cartpackageitems_set.all():
            line_total = float(
                item.hotel_package.package_Price) * item.quantity
            new_total += line_total
        request.session['items_total'] = cart.cartpackageitems_set.count()
        cart.total = new_total
        cart.save()
        context = {"cart": cart}
    else:
        empty_message = "You are yet to make any reservation"
        context = {"empty": True, "empty_message": empty_message,
                   "title": "Package Reservation"}

    template = "hotels/package_booking.html"
    return render(request, template, context)

# Conference room reservation


def conference_view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        line_total = 0.00
        s_room_total = 0.00
        d_room_total = 0.00

        for item in cart.cartconferenceitems_set.all():

            line_total = float(item.rooms.room_Price) * \
                item.guests * item.conference_duration
            request.session['line_total'] = line_total

            if item.single_room != None:
                s_room_total = float(item.single_room_price) * item.nights * float(
                    item.single_room_total) * float(100 - (item.rooms.room_discount))/100
                request.session['s_room_total'] = s_room_total
            else:
                s_room_total = 0.00

            if item.double_room != None:
                d_room_total = float(item.double_room_price) * item.nights * float(
                    item.double_room_total) * float(100 - (item.rooms.room_discount))/100
                request.session['d_room_total'] = d_room_total

            else:
                d_room_total = 0.00

            new_total = line_total + s_room_total + d_room_total
            request.session['discount'] = int(item.rooms.room_discount)

        request.session['items_total'] = cart.cartconferenceitems_set.count()

        cart.total = new_total
        cart.save()
        context = {"cart": cart, "line_total": line_total,
                   "s_room_total": s_room_total, "d_room_total": d_room_total}
    else:
        empty_message = "You are yet to make any conference room reservation"
        context = {"empty": True, "empty_message": empty_message,
                   "title": "Meeting Room Reservation"}

    template = "hotels/conference-booking.html"
    return render(request, template, context)


def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))

    cart_item = CartItems.objects.get(id=id)
    # cart_item.delete()
    cart_item.cart = None
    cart_item.save()

    return HttpResponseRedirect(reverse("cart"))


# Remove from package cart

def remove_from_packagecart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("package-cart"))

    cart_package_item = CartPackageItems.objects.get(id=id)
    # cart_item.delete()
    cart_package_item.cart = None
    cart_package_item.save()

    return HttpResponseRedirect(reverse("package-cart"))


def remove_from_conferencecart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("conference-cart"))

    cart_item = CartConferenceItems.objects.get(id=id)
    # cart_item.delete()
    cart_item.cart = None
    cart_item.save()

    return HttpResponseRedirect(reverse("conference-cart"))


class PackagesCreateView(LoginRequiredMixin, CreateView):
    """Creates hotels form"""
    model = Packages

    fields = ('title', 'package_type', 'city',
              'country', 'description', 'cover_photo',)

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class HotelPackagesCreateView(LoginRequiredMixin, CreateView):
    """Creates hotels form"""
    model = HotelPackages

    form_class = HotelPackagesForm

    def form_valid(self, form):

        hotel_package = form.save(commit=False)
        try:
            package = Packages.objects.get(
                user=self.request.user, id=self.kwargs.get('pk'))

        except Packages.DoesNotExist:
            raise Http404
        hotel_package.package = package
        hotel_package.user = self.request.user
        hotel_package.save()

        return super().form_valid(form)


class ItinireryCreateView(LoginRequiredMixin, CreateView):
    """Creates hotels form"""
    model = Itinirery

    fields = ('title', 'description', 'package_photo', 'description',)

    def form_valid(self, form):

        itinirery = form.save(commit=False)
        try:
            pack = Packages.objects.get(
                user=self.request.user, id=self.kwargs.get('pk'))
        except Packages.DoesNotExist:
            raise Http404
        itinirery.package = pack
        itinirery.user = self.request.user
        itinirery.save()

        return HttpResponseRedirect(reverse("package-list"))


# class PackageListView(LoginRequiredMixin, ListView):
#     """List select all rooms"""
#     model = Packages
#     template_name = 'hotels/package_list.html'
#     context_object_name = 'packages'
#     # ordering = ['-date_posted']
#     # paginate_by = 1


def package_list(request):
    """Display all packages according to the chosen criteria"""

    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.name] = price

    context = {
        'packages': Packages.objects.all(),
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'lowest_prices': lowest_prices,
    }
    return render(request, 'hotels/package_list.html', context)


def package_honeymoon_list(request):
    """Display all packages according to the chosen criteria"""
    packages = Packages.objects.all()
    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.title] = price

    context = {
        'packages': packages,
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'lowest_prices': lowest_prices,
        "title": "Honeymoon Packages"
    }
    return render(request, 'hotels/package_honeymoon_list.html', context)


def package_easter_list(request):
    """Display all packages according to the chosen criteria"""
    packages = Packages.objects.all()
    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.title] = price

    context = {
        'packages': packages,
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'lowest_prices': lowest_prices,
        "title": "Easter Packages"
    }
    return render(request, 'hotels/package_easter_list.html', context)


def package_christmas_list(request):
    """Display all packages according to the chosen criteria"""
    packages = Packages.objects.all()
    empty_message = "Sorry, no packages in this category"
    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.title] = price

    context = {
        'empty_message': empty_message,
        'packages': packages,
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'lowest_prices': lowest_prices,
        "title": "Christmas Packages"
    }
    return render(request, 'hotels/package_christmas_list.html', context)


def package_coast_list(request):
    """Display all packages according to the chosen criteria"""
    packages = Packages.objects.all()
    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.title] = price

    context = {
        'packages': packages,
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'lowest_prices': lowest_prices,
        "title": "Coast Packages"
    }
    return render(request, 'hotels/package_coast_list.html', context)


def package_selfdrive_list(request):
    """Display all packages according to the chosen criteria"""
    packages = Packages.objects.all()
    lowest_prices = {}
    for i in Packages.objects.all():
        if HotelPackages.objects.filter(package=i.id).exists():
            price = HotelPackages.objects.filter(package=i.id)[0].package_Price
            lowest_prices[i.title] = price

    context = {
        'packages': packages,
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'lowest_prices': lowest_prices,
        "title": "Weekend Gateways Packages"
    }
    return render(request, 'hotels/package_selfdrive_list.html', context)
