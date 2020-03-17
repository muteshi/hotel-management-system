from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Photo, Room, Hotels, Packages, Itinirery, HotelPackages, ConferenceRoom


class HotelsForm(forms.ModelForm):
    """Room form details"""
    class Meta:
        model = Hotels
        fields = (
            'name',
            'address',
            'city',
            'country',
            'mobile_number',
            'property_photo',
            'star_rating',
            'description',
    )

        help_texts = {
            'name': _('Enter the name of your hotel'),
            'address': _('Street address e.g Mombasa Rd'),
            'city': _('Enter the city or town where hotel is located'),
            'country': _('Country where located'),
            'property_photo': _('Upload main hotel photo'),
            'star_rating': _('Hotels star rating'),
            'mobile_number': _('We will use this to confirm this listing'),
            'description': _('A brief description of the hotel'),
            
        }


    # def __init__(self, user, *args, **kwargs):
    #     super(RoomForm, self).__init__(*args, **kwargs)
    #     self.fields['hotel'].queryset = Hotels.objects.filter(contact_person=user)




class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )


class RoomForm(forms.ModelForm):
    """Room form details"""
    class Meta:
        model = Room
        fields = ('hotel','room_Type','room_Name','room_Capacity','room_Price','total_Rooms','room_details','room_photo',)

        help_texts = {
            'hotel': _('Select hotel for this room'),
            'room_Type': _('Select the type of this room'),
            'room_Name': _('Enter a custom name for this room'),
            'room_Capacity': _('Enter max number of guests in this room'),
            'total_Rooms': _('Enter total number of this room'),
            'room_details': _('A brief description of the room'),
            'room_Price': _('Enter the price of the room per night'),
        }


    def __init__(self, user, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['hotel'].queryset = Hotels.objects.filter(contact_person=user)




    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


class PackageForm(forms.ModelForm):
    """Room form details"""
    class Meta:
        model = Packages
        fields = ('title','package_type', 'city', 'country','description',)

class DateInput(forms.DateInput):
    input_type = 'date'


class HotelPackagesForm(forms.ModelForm):
    """Room form details"""
    class Meta:
        model = HotelPackages
        fields = ('hotel','package_Price','duration','meal_Plans','start_Date','end_Date',)

        help_texts = {
            'package_Price': _('Price per person etc'),
            'duration': _('Enter number of nights applicable to this offer'),
            'start_Date': _('When this offer is effective'),
            'end_Date': _('When this offer ends'),
        }

        widgets = {
            'start_Date': DateInput(),
            'end_Date': DateInput(),
            'meal_Plans': forms.Textarea(
                attrs={
                'placeholder': 'What meal plans do you offer for this package? Each item on new line',
                'rows':4, 'cols':15
                }),
        }


        # def clean(self):
        #     data = self.cleaned_data["start_Date", "end_Date"]
        #     if "end_Date" < "start_Date":
        #         raise forms.ValidationError("End date cannot be lower than start date!")
                
        #     return data




class ItinireryForm(forms.ModelForm):
    """This is a form that will allow Itinerary to be added to a package"""
    class Meta:
        model = Itinirery
        fields = ('title','package','description','package_photo',)

        help_texts = {
            'title': _('e.g DAY 1: Departure from Nairobi to Dubai'),
            'description': _('Describe activities happening during this day'),
        }
        #Link itinireray to the appropriate user and package
        def __init__(self, user, *args, **kwargs):
            super(ItinireryForm, self).__init__(*args, **kwargs)
            self.fields['package'].queryset = Packages.objects.filter(user=user)


class ConferenceRoomForm(forms.ModelForm):
    """Form to be displayed on the frontend to enable conference room creation"""
    class Meta:
        model = ConferenceRoom
        fields = ('hotel','room_Name','room_Capacity','room_Price', 'room_discount', 'room_photo','room_details',)

        help_texts = {
            'room_Price': _('Enter price of the room per person'),
            'room_discount': _('Enter a discont % that will apply e.g 10'),
            'room_Name': _('Enter the name of the room')
            
        }

        widgets = {
            'room_details': forms.Textarea(
                attrs={
                'placeholder': 'Please enter features of the room. Enter each on new line. e.g Projector etc',
                'rows':4, 'cols':15
                }),
        }

    def __init__(self, user, *args, **kwargs):
        super(ConferenceRoomForm, self).__init__(*args, **kwargs)
        self.fields['hotel'].queryset = Hotels.objects.filter(contact_person=user)





