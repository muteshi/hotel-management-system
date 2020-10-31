from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from users import views
from .views import (
    CreateUserFromMobileView,
    LogoutAndBlacklistRefreshTokenForUserView,
    CustomTokenObtainPairView,
    UserProfileListAPIView,
    UserTypesListAPIView,
    UserProfileDetailsAPIView,
    UserDeleteAPIView,
    UserPartialUpdateView,
    UserUpdateAPIView,
    ProfileUpdateAPIView,
)

app_name = 'user'

# router = DefaultRouter()
# router.register('accounts/', views.UserProfileViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('create/', views.CreateUserView.as_view(), name="user-create"),
    path('create-user-from-mobile/',
         views.CreateUserFromMobileView.as_view(), name="user-from-mobile-create"),
    path('token/', views.CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    # add path for google authentication
    path('user-exists/',
         views.UserExistsView.as_view(), name='user-exists'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/blacklist/',
         LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),

    path('login/', views.CreateTokenView.as_view()),

    path('users/', views.UserProfileListAPIView.as_view()),

    path('user/<int:pk>/', views.UserProfileDetailsAPIView.as_view()),


    path('user/<int:pk>/delete/', views.UserDeleteAPIView.as_view()),

    path('user/<int:pk>/partial-update/',
         views.UserPartialUpdateView.as_view()),

    path('user/<int:pk>/update/',
         views.UserUpdateAPIView.as_view()),

    path('user-profile/<int:pk>/update/',
         views.ProfileUpdateAPIView.as_view()),

    path('user-types/', views.UserTypesListAPIView.as_view()),


]
