from django.http import QueryDict
from rest_framework import viewsets
from rest_framework.request import Request

from .models import Document
from .serializers import DocumentSelfSerializer


class DocumentSelfViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSelfSerializer

    def get_queryset(self):
        return Document.objects.filter(custom_user=self.request.user)

    def create(self, request: Request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            # Making QueryDict mutable to pass owner into the serializer
            request._full_data = request.data.copy()
        request.data["custom_user"] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        raise NotImplementedError("Updating documents is not supported")


class DocumentReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSelfSerializer

    def get_queryset(self):
        return Document.objects.filter(shared_with=self.request.user)
