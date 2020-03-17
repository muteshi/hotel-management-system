from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Booking, ConferenceReservation


class BookingForm(forms.ModelForm):
    """Room form details"""
    class Meta:
        model = Booking
        fields = ('title','first_name','last_name','mobile_Number','email','payment_option','special_requests')


        widgets = {
            
            'special_requests': forms.Textarea(
                attrs={
                'placeholder': 'Enter your special requests here. Kindly note requests are not guaranteed',
                'rows':4, 'cols':15
                }),

        }


class ConferenceBookingForm(forms.ModelForm):
    """Conference Room form details"""
    class Meta:
        model = ConferenceReservation
        fields = ('first_name','last_name','organisation_name','mobile_Number','email', 
                    'attachment', 'name_of_guests',
                    'start_time')

        help_texts = {
            'attachment': _('Upload a cheque of proforma invoice'),
            'organisation_name': _('Enter the name of your organisation'),
            'mobile_Number': _('Enter mobile number of the contact person'),

            
        }


        widgets = {
            
            'name_of_guests': forms.Textarea(
                attrs={
                'placeholder': 'Enter name of your guests each on new line',
                'rows':10, 'cols':15
                }),

        }


    

