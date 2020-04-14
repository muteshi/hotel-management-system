from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register('account/create', views.UserProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('account/login/', views.UserLoginApiView.as_view()),

]
