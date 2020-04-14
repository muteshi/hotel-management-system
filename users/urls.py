from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from users import views

app_name = 'user'

# router = DefaultRouter()
# router.register('accounts/', views.UserProfileViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('create/', views.CreateUserView.as_view(), name="create"),
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),

    path('login/', views.CreateTokenView.as_view()),

]
