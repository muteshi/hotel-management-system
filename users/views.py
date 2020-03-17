from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from users.forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from users.tokens import account_activation_token


from users.models import UserProfile
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


def register(request):
    """Registration view"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            user.save()



            current_site = settings.SITE_URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token =  account_activation_token.make_token(user)
            context = {"current_site": current_site,"name": name, 'uid':uid, 'token':token}
            subject = 'Activate Your Account at Marvellous Ventures'
            message = render_to_string('users/account_activation_email.html', context)
            plain_message = strip_tags(message)
            mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], html_message=message)
            messages.info(request, ('Account created successfully. Please go to your email to verify your account.'))
            return redirect('login')
        else:
            print (form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed. Finish creating your profile below'))
            return redirect('dashboard')
        else:
            messages.error(request, ('The confirmation link was invalid, possibly because it has already expired.'))
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

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
