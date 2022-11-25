from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from authentication.models import Organization
from backend.permissions import IsPharmacy, IsPatient
from products.models import Product, Order
from products.serializers import ProductSerializer, OrderSerializer


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


@permission_classes([IsPatient])
@api_view(['POST'])
def create_order(request):
    """
    Create an order
    {
      "product_quantities": [(product_id, quantity), (product_id, quantity), ...]
      "pharmacy_id": 1
    }
    """
    product_quantities = request.data['product_quantities']
    pharmacy_id = request.data['pharmacy_id']
    buyer = request.user.personal_user
    if len(product_quantities) == 0:
        return Response({'error': 'No products selected'}, status=HTTP_400_BAD_REQUEST)
    order = Order.create_order(buyer, product_quantities, pharmacy_id)
    return Response(OrderSerializer(order).data, status=HTTP_201_CREATED)


# TODO: Endpoint to be called when order is fulfilled, to upload and sign invoice


@permission_classes([IsPatient])
@api_view(['POST'])
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
        return Response({'error': 'Order is not pending'}, status=HTTP_400_BAD_REQUEST)
    order.razorpay_payment_id = payment_id
    order.save()
    if order.status != Order.OrderStatus.PAID:
        return Response({'error': 'Order not paid'}, status=HTTP_400_BAD_REQUEST)
    return Response(OrderSerializer(order).data, status=HTTP_201_CREATED)


@permission_classes([IsPharmacy])
@api_view(['POST'])
def mark_order_as_fulfilled(request):
    """
    Update order status to fulfilled
    {
      "order_id": 1,
      "invoice": FileUpload
    }
    """
    order_id = request.data['order_id']
    order = Order.objects.get(id=order_id)
    if order.status != Order.OrderStatus.PAID:
        return Response({'error': 'Order is not paid'}, status=HTTP_400_BAD_REQUEST)
    # document = req
    order.status = Order.OrderStatus.FULFILLED
    order.save()
    return Response(OrderSerializer(order).data, status=HTTP_201_CREATED)


class OrderReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsPatient | IsPharmacy]

    def get_queryset(self):
        if Organization.objects.filter(custom_user=self.request.user,
                                       category=Organization.OrganizationCategory.PHARMACY).exists():
            return Order.objects.filter(pharmacy=self.request.user.organization)
        elif self.request.user.personal_user:
            return Order.objects.filter(buyer=self.request.user.personal_user)
