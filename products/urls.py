from django.urls import path
from rest_framework import routers

from backend import settings
from .views import ProductListCreateAPIView, list_pharmacy_products, create_order

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()

urlpatterns = [
    path('self/products/', ProductListCreateAPIView.as_view(), name='products-self'),
    path('products/<int:pharmacy_id>', list_pharmacy_products, name='products'),
    path('patients/<int:pharmacy_id>', create_order, name='products'),
]

urlpatterns += router.urls
