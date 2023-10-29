from django import forms
from users.models import UserProfile, Profile
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    """Handles users registration"""
    email = forms.EmailField()

    class Meta:
        """Defines fields needed"""
        model = UserProfile
        fields = [
            'name',
            'email',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        """Save data to the database if safe"""
        user = super(RegistrationForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """Used for updating user profile"""
    email = forms.EmailField()

    class Meta:
        """Defines fields needed"""
        model = UserProfile
        fields = [
            'name',
            'email'
        ]


class ProfileUpdateForm(forms.ModelForm):
    """Used to update profile form"""
    class Meta:
        model = Profile
        fields = ['image',
                  'address',
                  'city',
                  'country',
                  'telephone_Number'
                  ]
