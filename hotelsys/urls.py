from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from reservations import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include
from users.views import ActivateAccount

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/activate/<uidb64>/<token>/',
         ActivateAccount.as_view(), name='activate-account'),
    path('accounts/dashboard/', user_views.profile, name='dashboard'),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('', include('hotels.urls')),
    path('api/account/', include('users.urls')),
    path('api/', include('hotels.api.urls'), name='hotels-api'),
    path('api/', include('reservations.api.urls'), name='reservations-api'),
    # path('checkout/', views.check_out, name='checkout'),

    path('hotels/hotel-room-checkout/',
         views.hotel_room_booking_checkout, name='hotel-room-checkout'),
    path('packages/hotel-package-checkout/',
         views.hotel_package_booking_checkout, name='hotel-package-checkout'),

    path('hotels/booking/success/', views.booking_success, name='booking-success'),
    # path('hotels/package/checkout/', views.package_check_out, name='package-checkout'),


]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Will only apply when development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
