
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hitcount.views import HitCountDetailView

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Hotels, Room, Packages, HotelPackages, Slider

from django.db.models import Min, Q, Max
from .filters import HotelFilter, PackagesFilter

today = datetime.date.today().strftime("%m/%d/%Y")
tomorrow = (datetime.date.today() +
            datetime.timedelta(days=1)).strftime("%m/%d/%Y")


def get_lowest_price(all_hotels, is_conference_room=False):
    """
    Function to get the lowest room price of a hotel
    """
    lowest_prices = {}
    for i in all_hotels:
        if Room.objects.filter(hotel=i.id).exists():
            price = Room.objects.filter(hotel=i.id)
            price = price.filter(is_conference_room)
            try:
                lowest_prices[i.name] = price[0].room_Price
            except:
                pass
        return lowest_prices


def home(request):

    hotels = Hotels.objects.filter(featured=True)
    search = request.session.get('search', None)
    hotels = hotels.filter(has_conference=False)
    packages = Packages.objects.filter(featured=True)
    conference_hotels = Hotels.objects.filter(
        Q(has_conference=True) & Q(featured=True))

    if search:
        last_search_results = []
        last_search_results = Hotels.objects.filter(Q(city__icontains=search) | Q(
            name__icontains=search) | Q(country__icontains=search))
        last_search_results = last_search_results.annotate(lowest_price=Min(
            'room__room_Price')).order_by('lowest_price')
    else:
        last_search_results = Hotels.objects.filter(
            active=True)
        last_search_results = sorted(
            last_search_results, key=lambda hotel: hotel.hit_count.hits_in_last(days=7), reverse=True)

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

    last_searched_lowest_prices = {}
    for i in last_search_results:
        if Room.objects.filter(hotel=i.id).exists():
            price = Room.objects.filter(hotel=i.id)
            price = price.filter(is_conference_room=False)
            try:
                last_searched_lowest_prices[i.name] = price[0].room_Price
            except:
                pass

    context = {
        'min': HotelPackages.objects.all().aggregate(Min('package_Price')),
        'sliders': Slider.objects.all(), 'hotels': hotels,
        'lowest_prices': lowest_prices,
        'last_searched_hotels': last_search_results,
        'p_lowest_prices': p_lowest_prices,
        'last_searched_lowest_prices': last_searched_lowest_prices,
        'c_lowest_prices': c_lowest_prices,
        'conference_hotels': conference_hotels,
        'packages': packages,
        'time': HotelPackages.objects.all().aggregate(Min('duration')),
        'title': 'Hotels, Safaris, Meetings, Events and cheap vacation packages'
    }
    return render(request, 'hotels/home.html', context)


def company(request):
    return render(request, 'hotels/company.html', {'title': 'About'})


def privacy(request):
    return render(request, 'hotels/privacy.html', {'title': 'Privacy Policy'})


def conference_hotels(request):
    """Display all conference venues"""
    hotels = Hotels.objects.filter(has_conference=True)
    hotels_filter = HotelFilter(request.GET, queryset=hotels)
    page = request.GET.get('page')
    paginator = Paginator(hotels_filter.qs, 9)

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

    checkin = request.session.get('checkin', today)
    checkin = datetime.datetime.strptime(checkin, "%m/%d/%Y")
    checkout = request.session.get('checkout', tomorrow)
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
        checkin = request.GET.get('checkin', today)
        checkin = request.session['checkin', tomorrow]
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
        hotels = Hotels.objects.filter(is_apartment=False)
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
            checkin = self.request.session.get('checkin', today)
            context['checkin'] = datetime.datetime.strptime(
                checkin, "%m/%d/%Y")
            checkout = self.request.session.get('checkout', tomorrow)
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
            checkin = self.request.session.get('checkin', today)
            context['checkin'] = datetime.datetime.strptime(
                checkin, "%m/%d/%Y")
            checkout = self.request.session.get('checkout', tomorrow)
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
                price = Room.objects.filter(hotel=i.id)
                price = price.filter(is_apartment=True)
                try:
                    lowest_prices[i.name] = price[0].room_Price
                except:
                    pass

        context['min'] = Room.objects.filter(
            is_apartment=True).aggregate(Min('room_Price'))

        context['lowest_prices'] = lowest_prices

        return context


def search(request):  # Accomodation search
    checkin = request.session.get('checkin', today)
    request.session['checkin'] = checkin
    checkout = request.session.get('checkout', tomorrow)
    request.session['checkout'] = checkout
    adult = request.GET.get('adult')
    request.session['adult'] = adult
    child = request.GET.get('child')
    request.session['child'] = child
    room = request.GET.get('room')
    request.session['room'] = room
    search = request.GET.get('search')
    request.session['search'] = search

    search_text = request.GET.get('search', None)

    if search_text:
        results = Hotels.objects.filter(Q(city__icontains=search_text) | Q(
            name__icontains=search_text) | Q(country__icontains=search_text) | Q(address__icontains=search_text))
        hotels_filter = HotelFilter(request.GET, queryset=results)

    else:
        results = Hotels.objects.all()
        hotels_filter = HotelFilter(request.GET, queryset=results)

    page = request.GET.get('page', 1)
    paginator = Paginator(hotels_filter.qs, 9)
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
            price = Room.objects.filter(hotel=i.id)
            price = price.filter(is_conference_room=False)
            try:
                lowest_prices[i.name] = price[0].room_Price
            except:
                pass
    hotel_count = Hotels.objects.all().count()
    conference_count = Hotels.objects.filter(has_conference=True).count()
    apartment_count = Hotels.objects.filter(is_apartment=True).count()
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
    checkin = request.session.get('checkin', today)
    request.session['checkin'] = checkin
    checkout = request.session.get('checkout', tomorrow)
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
    paginator = Paginator(hotels_filter.qs, 9)
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

    checkin = request.session.get('checkin', today)
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


class HotelsDetailView(HitCountDetailView):
    """List all details of the hotel"""
    model = Hotels
    count_hit = True

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

        checkin = self.request.session.get('checkin', today)
        self.request.session['checkin'] = checkin
        context['checkin'] = datetime.datetime.strptime(
            checkin, "%m/%d/%Y")
        checkout = self.request.session.get('checkout', tomorrow)
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


class ApartmentDetailView(HitCountDetailView):
    """List all details of the apartment"""
    model = Hotels
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(ApartmentDetailView, self).get_context_data(
            *args, **kwargs)
        lowest_prices = {}
        for i in Hotels.objects.filter(is_apartment=True):
            if Room.objects.filter(Q(is_apartment=True) & Q(hotel=i.id)).exists():
                price = Room.objects.filter(hotel=i.id)
                price = price.filter(is_apartment=True)
                try:
                    lowest_prices[i.name] = price[0].room_Price
                except:
                    pass

        context['hotels'] = Hotels.objects.filter(is_apartment=True)
        context['min'] = Room.objects.filter(
            Q(is_apartment=True) & Q(hotel=i.id)).aggregate(Min('room_Price'))
        context['lowest_prices'] = lowest_prices
        context['title'] = self.get_object().name
        checkin = self.request.session.get('checkin', today)
        self.request.session['checkin'] = checkin
        context['checkin'] = datetime.datetime.strptime(
            checkin, "%m/%d/%Y")
        checkout = self.request.session.get('checkout', tomorrow)
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


class ConferenceHotelsDetailView(HitCountDetailView):
    """List all details of the hotel"""
    model = Hotels
    count_hit = True
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

        checkin = self.request.GET.get('checkin', today)
        self.request.session['checkin'] = checkin
        context['checkin'] = datetime.datetime.strptime(
            checkin, "%m/%d/%Y")
        checkout = self.request.GET.get('checkout', tomorrow)
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
            checkin = self.request.session.get('checkin', today)
            checkin = datetime.datetime.strptime(checkin, "%Y-%m-%d")
            context['checkin'] = checkin
            is_conference = False
            self.request.session['is_conference'] = is_conference
            context['is_conference'] = is_conference
        except:
            pass

        return context


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
    return render(request, 'hotels/package_list.html', context)


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
