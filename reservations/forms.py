from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Booking


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
