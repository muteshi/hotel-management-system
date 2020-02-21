from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Hotels, Room
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core import mail
from django.contrib import messages
from .forms import RoomForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import datetime

from .forms import PhotoForm
from .models import Photo, Cart, CartItems
from reservations.models import Reservation


def home(request):
    return render(request, 'hotels/home.html')


def company(request):
    return render(request, 'hotels/company.html', {'title': 'About'})

def hotels(request):
    """Display all hotels"""

    context = {
        'hotels': Hotels.objects.all()
    }
    return render(request, 'hotels/hotels.html', context)

def single(request, slug):
    """Display all hotels"""
    # hotel = Hotels.objects.all(slug=slug)
    context = {
        'hotels': Hotels.objects.all()
    }
    return render(request, 'hotels/hotels_detail.html', context)


class HotelsListView(ListView):
    """List select all hotels on the frontpage"""
    model = Hotels
    template_name = 'hotels/hotels.html'
    context_object_name = 'hotels'
    ordering = ['-date_posted']
    paginate_by = 1

def search_hotels(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']

    else:
        search_text = ''

    # search_text = {
    #         'name__contains':'search_text',
    #         'address__contains':'search_text',
    #         'city__contains':'search_text',
    # }

    hotels = Hotels.objects.filter(city__contains=search_text).order_by('name')

    return render(request, 'hotels/ajax_search.html', {'hotels': hotels})





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


class HotelsCreateView(LoginRequiredMixin, CreateView):
    """Creates hotels form"""
    model = Hotels

    fields = [
            'name',
            'address',
            'city',
            'country',
            'mobile_number',
            'property_photo',
            'star_rating',
            'description',
            'property_photo',
    ]

    def form_valid(self, form):
        form.instance.contact_person = self.request.user

        return super().form_valid(form)

class HotelsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update all details of the hotel"""
    model = Hotels
    fields = [
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
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        hotel = self.get_object()
        if self.request.user == hotel.contact_person:
            return True
        return False

    def get_success_url(self):
        return reverse('hotels-list')

class RoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update all details of the hotel"""
    model = Room
    fields = ('hotel','room_Type','room_Name','room_Capacity','room_Price','total_Rooms','room_details','room_photo',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        room = self.get_object()
        if self.request.user == room.user:
            return True
        return False

    def get_success_url(self):
        return reverse('room-list')



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
    success_url = '/hotels/rooms/'

    def test_func(self):
        room = self.get_object()
        if self.request.user == room.user:
            return True
        return False


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

            return redirect('room-list')
    else:
        form = RoomForm(request.user)

    return render(request, 'hotels/room_form.html', {'form': form})


class PhotoUploadView(LoginRequiredMixin,View):
    def get(self, request, pk):
        photos_list = Photo.objects.all()
        return render(self.request, 'hotels/uploads.html', {'photos': photos_list})

    def post(self, request, pk):
        """Handles photo uploads and assign them to the correct user and hotel"""
        form = PhotoForm(self.request.POST, self.request.FILES, self.request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            try:
                hotel = Hotels.objects.get(contact_person = self.request.user, id=self.kwargs.get('pk'))
            except Hotels.DoesNotExist:
                raise Http404
            photo.hotel = hotel
            photo.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))



# class ReviewCreateView(CreateView):
#
#     model = Review
#     fields = ['comment','rating']
#     #success_url = '/hotels/'
#     def get_success_url(self):
#         hotelid = self.kwargs['id']
#         url = reverse('hotel-detail', args=[hotelid])
#         return url
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.instance.hotel_id = self.kwargs['id']
#         return super(ReviewCreateView, self).form_valid(form)

def bookRoom(request):

    FirstDate = request.session['checkin']
    SecDate =  request.session['checkout']
    # #
    Checkin = datetime.datetime.strptime(FirstDate, "%Y-%m-%d").date()
    Checkout = datetime.datetime.strptime(SecDate, "%Y-%m-%d").date()
    timedeltaSum = Checkout - Checkin
    #
    StayDuration = timedeltaSum.days
    #
    Hotel = Hotels.objects.get(id = hotelid)
    theRoom = Room.objects.get(id = roomid)
    #
    price = theRoom.room_Price
    TotalCost = StayDuration * price

    context = {'checkin': Checkin, 'checkout':Checkout,'stayduration':StayDuration,'hotel':Hotel,'room':theRoom,'price':price,
    'totalcost':TotalCost}
    return render(request, 'hotels_detail', context)


def reservations(request):

    template = "hotels/reservations.html"
    context = {}
    return render(request, template, context)

def view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        for item in cart.cartitems_set.all():
            line_total = float(item.rooms.room_Price) * item.quantity * item.stay_duration
            new_total += line_total
        request.session['items_total'] = cart.cartitems_set.count()
        cart.total = new_total
        cart.save()
        context = {"cart": cart}
    else:
        empty_message = "You are yet to make any reservation"
        context = {"empty": True, "empty_message": empty_message}

    template = "hotels/booking.html"
    return render(request, template, context)


def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))

    cart_item = CartItems.objects.get(id = id)
    # cart_item.delete()
    cart_item.cart = None
    cart_item.save()

    return HttpResponseRedirect(reverse("cart"))
