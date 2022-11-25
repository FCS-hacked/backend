from django.urls import path
from rest_framework import routers

from backend import settings
from documents.views import DocumentReadOnlyViewSet, DocumentSelfViewSet, transfer_ownership

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()
router.register('documents-shared', DocumentReadOnlyViewSet, basename='documents-shared')
router.register('self/documents', DocumentSelfViewSet, basename='document-self')

urlpatterns = [
    path('self/transfer-ownership/<int:document_id>/', transfer_ownership, name='document-transfer-ownership'),
]

urlpatterns += router.urls
