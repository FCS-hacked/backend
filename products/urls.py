from django.urls import path
from rest_framework import routers

from backend import settings
from .views import ProductListCreateAPIView, list_pharmacy_products, create_order, \
    update_order_payment_id, OrderReadOnlyViewSet, mark_order_as_fulfilled, create_insurance_claim, \
    process_insurance_claim, list_insurance_claims

router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()
router.register('self/orders', OrderReadOnlyViewSet, basename='orders-self')

urlpatterns = [
    path('self/products/', ProductListCreateAPIView.as_view(), name='products-self'),
    path('products/<int:pharmacy_id>', list_pharmacy_products, name='products'),
    path('patients/create_order/', create_order, name='create_order'),
    path('patients/update_order_payment_id/', update_order_payment_id, name='update_order_payment_id'),
    path('pharmacies/mark-order-as-fulfilled/', mark_order_as_fulfilled, name='mark-order-as-fulfilled'),
    path('patients/create-insurance-claim/', create_insurance_claim, name='create-insurance-claim'),
    path('patients/process-insurance-claim/', process_insurance_claim, name='process-insurance-claim'),
    path('patients/list-insurance-claims/', list_insurance_claims, name='list-insurance-claims'),
]

urlpatterns += router.urls
