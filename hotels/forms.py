from .models import Photo, Room, Hotels
from django import forms


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
