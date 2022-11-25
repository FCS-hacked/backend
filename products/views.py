from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

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
    return Response(OrderSerializer(order).data)


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
    order = Order.objects.get(order_id=order_id)
    order.razorpay_payment_id = payment_id
    order.save()
    return Response(OrderSerializer(order).data)


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
    order = Order.objects.get(order_id=order_id)
    # document = req
    order.status = Order.FULFILLED
    order.save()
    return Response(OrderSerializer(order).data)
