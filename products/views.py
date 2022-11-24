from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.permissions import IsPharmacy
from products.models import Product
from products.serializers import ProductSerializer


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
