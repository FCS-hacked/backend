from rest_framework import routers

from .views import OrganizationReadOnlyViewSet, ProfessionalReadOnlyViewSet

router = routers.DefaultRouter()
router.register('organizations', OrganizationReadOnlyViewSet, basename='organizations')
router.register('professionals', ProfessionalReadOnlyViewSet, basename='professionals')

urlpatterns = [

]

urlpatterns += router.urls
