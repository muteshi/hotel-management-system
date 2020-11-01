import json
import urllib
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from users.forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from rest_framework.mixins import UpdateModelMixin


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from hotels.api.permissions import IsOwnerOrReadOnly,  IsAdminOrOwner, IsAdmin
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserDetailsSerializer,
    ProfileSerializer,
    UserTypesSerializers
)
from rest_framework_simplejwt.views import TokenObtainPairView


from users import models
from reservations.models import Booking
from users import permissions


from users.models import UserProfile, Profile, UserTypes
from django.contrib.auth import login
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core import mail
from django.views import View
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activation_token

from users import serializers
from rest_framework_jwt import views as jwt_views


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class GoogleView(APIView):

    def post(self, request):

        payload = {'access_token': request.data.get(
            "token")}  # validate the token

        r = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {
                'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = models.UserProfile.objects.get(email=data['email'])
        except models.UserProfile.DoesNotExist:
            user = models.UserProfile()
            user.email = data['email']
            user.is_active = True
            # provider random default password
            user.password = make_password(
                BaseUserManager().make_random_password())
            user.name = data['name']
            user.save()

        # generate token without username & password
        token = RefreshToken.for_user(user)

        token['name'] = user.name
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        response = {}
        response['email'] = user.email
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)


def register(request):
    """Registration view"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            user = form.save(commit=False)
            user.is_active = False
            user.is_staff = True
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            user.save()
            profile = Profile.objects.filter(user=user)[0]
            usertype = UserTypes.objects.filter(name='Company')[0]
            profile.user_type = usertype
            profile.save()

            current_site = settings.SITE_URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            context = {"current_site": current_site,
                       "name": name, 'uid': uid, 'token': token}
            subject = 'Activate Your Account at Marvellous Ventures'
            message = render_to_string(
                'users/account_activation_email.html', context)
            plain_message = strip_tags(message)
            mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [
                           email], html_message=message)
            messages.info(
                request, ('Account created successfully. Please go to your email to verify your account.'))
            return redirect('bookings-home')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        current_site = settings.SITE_URL
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            # login(request, user)
            messages.success(
                request, ('Your account has been confirmed. You can login by clicking on the login button above'))
            return redirect('bookings-home')
        else:
            messages.error(
                request, ('The confirmation link was invalid, possibly because it has already expired.'))
            return redirect('register')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    bookings = Booking.objects.filter(user=request.user)

    context = {
        'bookings': bookings,
        'u_form': u_form,
        'p_form': p_form

    }

    return render(request, 'users/profile.html', context)


class UserProfileListAPIView(ListAPIView):
    """Displays list of users"""

    serializer_class = serializers.ProfileDetailsSerializer
    permission_classes = ()

    def get_queryset(self, *args, **kwargs):
        if (self.request.user) and (self.request.user.is_superuser):
            profiles = models.UserProfile.objects.all()
        else:
            profiles = models.UserProfile.objects.filter(
                Q(parent=self.request.user.id) | Q(id=self.request.user.id))

        return profiles


class UserProfileDetailsAPIView(RetrieveAPIView):
    """Displays details of  a specific user"""
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.ProfileDetailsSerializer
    permission_classes = ()


class UserTypesListAPIView(ListAPIView):
    """Displays types of users"""
    queryset = models.UserTypes.objects.all()
    serializer_class = serializers.UserTypesSerializers
    permission_classes = ()


class UserUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of a user"""
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = ()


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    """Updates details of a user profile"""
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileUpdateSerializer
    permission_classes = ()


class CreateUserView(generics.CreateAPIView):
    """Handle creating new user in the system from web"""

    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class CreateUserFromMobileView(generics.CreateAPIView):
    """Handle creating new user in the system from mobile"""

    serializer_class = serializers.UserProfileSerializer
    # queryset = models.Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class UserPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.ActivateSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializers):
        serializers.save()


class UserDeleteAPIView(DestroyAPIView):
    """Deletes a user object"""
    queryset = UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (IsAdminOrOwner,)


class CreateTokenView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = serializers.CustomTokenObtainPairSerializer
