from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('organizations', views.OrganizationReadOnlyViewSet, basename='organizations')
router.register('self/organization', views.OrganizationSelfViewSet, basename='organization-self')
router.register('self/personal-user', views.PersonalUserSelfViewSet, basename='personal-user-self')
router.register('professionals', views.ProfessionalReadOnlyViewSet, basename='professionals')

urlpatterns = [
    path('send-hotp-email/', views.send_hotp_email, name='send-hotp-email'),
]

urlpatterns += router.urls
