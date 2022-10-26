from rest_framework import routers

from .views import OrganizationReadOnlyViewSet, ProfessionalReadOnlyViewSet, OrganizationSelfViewSet, \
    PersonalUserSelfViewSet

router = routers.DefaultRouter()
router.register('organizations', OrganizationReadOnlyViewSet, basename='organizations')
router.register('self/organization', OrganizationSelfViewSet, basename='organization-self')
router.register('self/personal-user', PersonalUserSelfViewSet, basename='personal-user-self')
router.register('professionals', ProfessionalReadOnlyViewSet, basename='professionals')

urlpatterns = [

]

urlpatterns += router.urls
