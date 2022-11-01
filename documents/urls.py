from rest_framework import routers

from documents.views import DocumentReadOnlyViewSet, DocumentSelfViewSet

router = routers.DefaultRouter()
router.register('documents-shared', DocumentReadOnlyViewSet, basename='documents-shared')
router.register('self/documents', DocumentSelfViewSet, basename='document-self')

urlpatterns = [

]

urlpatterns += router.urls
