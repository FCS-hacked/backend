from django.core.mail import send_mail
from django.http import QueryDict
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.models import Organization, PersonalUser, CustomUser
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
        return PersonalUser.objects.filter(custom_user__is_active=True,
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_details_from_metamask(request):
    """
    Returns a list of ids from metadata
    Input: {metamask_ids: [0x1, 0x2]}
    Output: [{
            "first_name": "first",
            "last_name": "last",
            "email": "a@b.com",
        }, {...}, ...]
    """

    def metamask_id_to_custom_user(metamask_id):
        try:
            custom_user: CustomUser = CustomUser.objects.get(metamask_id=metamask_id)
            return {
                "first_name": custom_user.first_name,
                "last_name": custom_user.last_name,
                "email": custom_user.email,
            }
        except CustomUser.DoesNotExist:
            return {
                "first_name": "Anon",
                "last_name": "ymous",
                "email": "anonymous@example.com",
            }

    metamask_ids = request.data["metamask_ids"]
    if metamask_ids is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    profile_data = list(map(metamask_id_to_custom_user, metamask_ids))
    return Response(profile_data)


@api_view(['PATCH'])
def patch_custom_user(request):
    """
    Changes the wallet address and two_factor_enabled of the user
    {
        "wallet_address": "0x1234567890",
        "two_factor_enabled": true/false
    }
    """
    wallet_address = request.data.get("wallet_address", request.user.wallet_address)
    two_factor_enabled = request.data.get("two_factor_enabled", request.user.two_factor_enabled)
    request.user.wallet_address = wallet_address
    request.user.two_factor_enabled = two_factor_enabled
    request.user.save()
    return Response(status=status.HTTP_201_CREATED)
