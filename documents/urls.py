from rest_framework import routers

from backend import settings
from documents.views import DocumentReadOnlyViewSet, DocumentSelfViewSet

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()
router.register('documents-shared', DocumentReadOnlyViewSet, basename='documents-shared')
router.register('self/documents', DocumentSelfViewSet, basename='document-self')

urlpatterns = [

]

urlpatterns += router.urls
