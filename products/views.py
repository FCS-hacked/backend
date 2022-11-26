from django.core.exceptions import BadRequest
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from authentication.models import Organization
from backend.permissions import IsPharmacy, IsPatient, IsInsurance
from documents.models import Document
from products.models import Product, Order, InsuranceClaim
from products.serializers import ProductSerializer, OrderSerializer, InsuranceClaimSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsPharmacy]

    def get_queryset(self):
        return Product.objects.filter(pharmacies=self.request.user.organization)

    def perform_create(self, serializer):
        serializer.save(pharmacies=[self.request.user.organization])


@api_view(['GET'])
def list_pharmacy_products(request, pharmacy_id):
    """
    List all products of a pharmacy
    'products/<pharmacy_id: int>'
    """
    pharmacy_id = int(pharmacy_id)
    products = Product.objects.filter(pharmacies=pharmacy_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsPatient])
def create_order(request):
    """
    Create an order
    {
      "product_quantities": [(product_id, quantity), (product_id, quantity), ...]
      "pharmacy_id": 1,
      "prescription_id": 1
    }
    """
    product_quantities = request.data['product_quantities']
    pharmacy_id = request.data['pharmacy_id']
    prescription_id = request.data['prescription_id']
    buyer = request.user.personal_user
    if len(product_quantities) == 0:
        return Response({'error': 'No products selected'}, status=HTTP_400_BAD_REQUEST)
    order = Order.create_order(buyer, product_quantities, pharmacy_id, prescription_id)
    return Response(OrderSerializer(order).data, status=HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsPatient])
def update_order_payment_id(request):
    """
    Update order status to paid
    {
      "payment_id": 1,
      "order_id": 1
    }
    """
    payment_id = request.data['payment_id']
    order_id = request.data['order_id']
    order = Order.objects.get(id=order_id)
    if order.status != Order.OrderStatus.PENDING and order.buyer != request.user.personal_user:
        raise BadRequest('Order is not pending')
    order.razorpay_payment_id = payment_id
    order.save()
    if order.status != Order.OrderStatus.PAID:
        return Response({'error': 'Order not paid'}, status=HTTP_400_BAD_REQUEST)
    return Response(OrderSerializer(order).data, status=HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsPharmacy])
def mark_order_as_fulfilled(request):
    """
    Update order status to fulfilled
    {
      "order_id": 1,
      "invoice_id": 9 <document_id>
    }
    """
    order_id = request.data['order_id']
    order = Order.objects.get(id=order_id)
    if order.status != Order.OrderStatus.PAID:
        raise BadRequest('Order is not paid')
    order.invoice = Document.objects.get(id=request.data['invoice_id'])
    order.save()
    return Response(OrderSerializer(order).data, status=HTTP_201_CREATED)


class OrderReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsPatient | IsPharmacy]

    def get_queryset(self):
        if Organization.objects.filter(custom_user=self.request.user,
                                       category=Organization.OrganizationCategory.PHARMACY).exists():
            return Order.objects.filter(pharmacy=self.request.user.organization).exclude(
                status=Order.OrderStatus.PENDING)
        elif self.request.user.personal_user:
            return Order.objects.filter(buyer=self.request.user.personal_user)


@api_view(['POST'])
@permission_classes([IsPatient])
def create_insurance_claim(request):
    """
    Create insurance document
    {
      "provider_email": a@b.com,
      "order_id": 1
    }
    """
    order_id = request.data['order_id']
    provider_email = request.data['provider_email']
    order = Order.objects.get(id=order_id)
    if order.status != Order.OrderStatus.FULFILLED:
        raise BadRequest('Order is not fulfilled')
    if request.user.personal_user != order.buyer:
        raise BadRequest('User is not the buyer')
    insurance_claim = InsuranceClaim.create_claim(order_id, provider_email)
    return Response(InsuranceClaimSerializer(insurance_claim).data, status=HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsInsurance])
def process_insurance_claim(request):
    """
    Approve insurance claim
    {
      "insurance_claim_id": 1,
      "accepted": true/false
    }
    """
    insurance_claim_id = request.data['insurance_claim_id']
    accepted = request.data['accepted']
    insurance_claim = InsuranceClaim.objects.get(id=insurance_claim_id)
    if insurance_claim.provider != request.user.organization:
        raise BadRequest('User is not the provider')
    insurance_claim.process_claim(accepted=accepted)
    return Response(InsuranceClaimSerializer(insurance_claim).data, status=HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsPharmacy | IsPatient])
def list_insurance_claims(request):
    """
    List insurance claims for a insurance provider or patient
    """
    if Organization.objects.filter(custom_user=request.user,
                                   category=Organization.OrganizationCategory.INSURANCE).exists():
        claims = InsuranceClaim.objects.filter(provider=request.user.organization)
    else:
        claims = InsuranceClaim.objects.filter(order__buyer=request.user.personal_user)
    return Response(InsuranceClaimSerializer(claims, many=True).data, status=HTTP_201_CREATED)
