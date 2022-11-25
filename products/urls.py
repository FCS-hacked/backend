from django.urls import path
from rest_framework import routers

from backend import settings
from .views import ProductListCreateAPIView

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()

urlpatterns = [
    path('self/products/', ProductListCreateAPIView.as_view(), name='products-self'),
    path('products/<int:pharmacy_id>', ProductListCreateAPIView.as_view(), name='products'),
]

urlpatterns += router.urls
