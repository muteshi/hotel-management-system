"""hotelsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from reservations import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include, url
from users.views import ActivateAccount

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate-account'),
    path('accounts/dashboard/', user_views.profile, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('', include('hotels.urls')),
    # path('checkout/', views.check_out, name='checkout'),
    path('hotels/rooms/checkout/', views.new_booking, name='booking-checkout'),
    path('hotels/conferencerooms/checkout/', views.new_conference_booking, name='conference-booking-checkout'),
    path('hotels/booking/success/', views.booking_success, name='booking-success'),
    # path('hotels/package/checkout/', views.package_check_out, name='package-checkout'),
    path('hotels/package/checkout/', views.new_package_booking, name='package-checkout'),
    url(r'^cart/(?P<slug>[\w-]+)/$', views.add_to_cart, name='update-booking-2'),
    url(r'^hotels/package/cart/(?P<id>[\w-]+)/$', views.package_add_to_cart, name='package-booking'),
    url(r'^hotels/conference/cart/(?P<slug>[\w-]+)/$', views.conference_add_to_cart, name='conference-update-booking-2'),
    path('hotels/bookings/<int:pk>/', views.check_out, name='single_order'),
]


urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# Will only apply when development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
