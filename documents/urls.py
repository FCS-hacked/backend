from django.urls import path
from rest_framework import routers

from backend import settings
from .views import DocumentReadOnlyViewSet, DocumentSelfViewSet, transfer_ownership, check_signature, media

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()
router.register('documents-shared', DocumentReadOnlyViewSet, basename='documents-shared')
router.register('self/documents', DocumentSelfViewSet, basename='document-self')

urlpatterns = [
    path('self/transfer-ownership/<int:document_id>/', transfer_ownership, name='document-transfer-ownership'),
    path('self/check-signature/<int:document_id>/', check_signature, name='document-check-signature'),
    path('media/', media, name='document-media'),
]

urlpatterns += router.urls
