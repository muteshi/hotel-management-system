from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Photo, Room, Hotels, Packages, Itinirery, HotelPackages



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )


class RoomForm(forms.ModelForm):
    """Room form details"""
    class Meta:
        model = Room
        fields = ('hotel','room_Type','room_Name','room_Capacity','room_Price','total_Rooms','room_details','room_photo',)

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
        fields = ('title','package_type','description',)

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
    """Room form details"""
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





