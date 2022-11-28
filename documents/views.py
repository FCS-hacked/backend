import hashlib
import time

from django.core.exceptions import BadRequest
from django.http import QueryDict
from django_sendfile import sendfile
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from authentication.models import CustomUser, PersonalUser, Organization
from backend import settings
from backend.permissions import HasHOTPInUnsafeMethods
from products.models import Order
from .models import Document
from .serializers import DocumentSelfSerializer


class DocumentSelfViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSelfSerializer
    permission_classes = (IsAuthenticated, HasHOTPInUnsafeMethods)

    def get_queryset(self):
        return Document.objects.filter(custom_user=self.request.user)

    def create(self, request: Request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            # Making QueryDict mutable to pass owner into the serializer
            request._full_data = request.data.copy()
        request.data["custom_user"] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        if len(request.data) != 1 or "shared_with" not in request.data:
            raise Exception("Only shared_with field can be updated")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance: Document = self.get_object()
        if Order.objects.filter(invoice=instance).exists() or Order.objects.filter(prescription=instance).exists():
            raise PermissionDenied("Document is linked to an order and cannot be deleted")
        return Response(status=204)


class DocumentReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSelfSerializer

    def get_queryset(self):
        return Document.objects.filter(shared_with=self.request.user)


@api_view(['PATCH'])
def transfer_ownership(request, document_id):
    """
    Transfer ownership of a document to another user
    {
        "document_id": 1,
        "custom_user_email": "a@b.c"
    }
    """
    custom_user_email = request.data["custom_user_email"]
    document = Document.objects.get(id=document_id)
    if document.custom_user != request.user:
        raise BadRequest("You don't own this document")
    if Order.objects.filter(invoice=document).exists() or Order.objects.filter(prescription=document).exists():
        raise BadRequest("This document is attached to an order")
    document.shared_with.add(document.custom_user)
    document.custom_user = CustomUser.objects.get(email=custom_user_email)
    document.save()
    return Response(status=HTTP_201_CREATED)


@api_view(['POST'])
def check_signature(request, document_id):
    """
        Check if a document has been signed by the user. To be called after signing a document on Metamask
    """
    document: Document = Document.objects.get(id=document_id)
    if not document.custom_user == request.user and not document.shared_with.filter(id=request.user.id).exists():
        raise PermissionDenied("You don't have access to this document")
    if document.is_signed_by(request.user):
        if PersonalUser.objects.filter(custom_user=request.user).exists():
            signer = PersonalUser.objects.get(custom_user=request.user)
            if signer.category == PersonalUser.PersonalUserCategory.PROFESSIONAL:
                document.signed_by_professional = True
        elif Organization.objects.filter(custom_user=request.user).exists():
            signer = Organization.objects.get(custom_user=request.user)
            if signer.category == Organization.OrganizationCategory.PHARMACY:
                document.signed_by_pharmacy = True
            elif signer.category == Organization.OrganizationCategory.HOSPITAL:
                document.signed_by_hospital = True
            elif signer.category == Organization.OrganizationCategory.INSURANCE:
                document.signed_by_insurance_firm = True
        return Response({"signed": True}, status=HTTP_201_CREATED)
    return Response({"signed": False}, status=HTTP_400_BAD_REQUEST)


def media(request):
    url = request.GET.get("url")
    print(type(url), url)
    s = request.GET.get("s")
    time_value, hash_value = s.split("0x")
    payload = url + time_value + settings.SECRET_KEY
    if hash_value != hashlib.sha256(payload.encode()).hexdigest():
        raise BadRequest("Invalid signature")
    if int(time_value) + 120 < int(time.time()):
        raise BadRequest("Link expired" + str(time_value) + hash_value)
    return sendfile(request, "/".join(url.split("/")[2:]))
