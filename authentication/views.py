from django.core.mail import send_mail
from django.http import QueryDict
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.models import Organization, PersonalUser
from authentication.serializers import OrganizationExternalSerializer, PersonalUserExternalSerializer, \
    PersonalUserSelfSerializer, OrganizationSelfSerializer
from backend import settings


class OrganizationReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationExternalSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Organization.objects.filter(custom_user__is_active=True)


class ProfessionalReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PersonalUser.objects.all()
    serializer_class = PersonalUserExternalSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PersonalUser.objects.filter(is_active=True,
                                           category=PersonalUser.PersonalUserCategory.PROFESSIONAL)


class PersonalUserSelfViewSet(viewsets.ModelViewSet):
    # Set user as personal user post-registration
    queryset = PersonalUser.objects.all()
    serializer_class = PersonalUserSelfSerializer

    def get_queryset(self):
        return PersonalUser.objects.filter(custom_user=self.request.user)

    def create(self, request: Request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            # Making QueryDict mutable to pass owner into the serializer
            request._full_data = request.data.copy()
        request.data["custom_user"] = request.user.id
        request.data["is_active"] = False
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            # Making QueryDict mutable to pass owner into the serializer
            request._full_data = request.data.copy()
        request.data["custom_user"] = request.user.id
        request.data["is_active"] = False
        return super().update(request, *args, **kwargs)


class OrganizationSelfViewSet(viewsets.ModelViewSet):
    # Set user as org post-registration
    queryset = Organization.objects.all()
    serializer_class = OrganizationSelfSerializer

    def get_queryset(self):
        return Organization.objects.filter(custom_user=self.request.user)

    def create(self, request: Request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            # Making QueryDict mutable to pass owner into the serializer
            request._full_data = request.data.copy()
        request.data["custom_user"] = request.user.id
        request.data["is_active"] = False
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            # Making QueryDict mutable to pass owner into the serializer
            request._full_data = request.data.copy()
        request.data["custom_user"] = request.user.id
        request.data["is_active"] = False
        return super().update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_hotp_email(request):
    # Send HOTP to the user's email
    hotp_string = request.user.initialize_hotp()
    send_mail(
        'HOTP code',
        f'Your HOTP code is {hotp_string}',
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False,
    )
    return Response(status=status.HTTP_201_CREATED)
