from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from authentication.models import Organization, PersonalUser
from authentication.serializers import OrganizationExternalSerializer, PersonalUserExternalSerializer


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
