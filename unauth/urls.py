from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register-as-personal-user/', views.register_as_personal_user, name='register-as-personal-user'),
    path('register-as-organization/', views.register_as_organization, name='register-as-organization'),
]

urlpatterns += router.urls
