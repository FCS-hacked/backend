from django.urls import path
from rest_framework import routers

from backend import settings
from . import views

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()
router.register('organizations', views.OrganizationReadOnlyViewSet, basename='organizations')
router.register('self/organization', views.OrganizationSelfViewSet, basename='organization-self')
router.register('self/personal-user', views.PersonalUserSelfViewSet, basename='personal-user-self')
router.register('professionals', views.ProfessionalReadOnlyViewSet, basename='professionals')

urlpatterns = [
    path('send-hotp-email/', views.send_hotp_email, name='send-hotp-email'),
    path('get-details-from-metamask/', views.get_details_from_metamask, name='get-details-from-metamask'),
]

urlpatterns += router.urls
