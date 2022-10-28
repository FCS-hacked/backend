from rest_framework import permissions
from rest_framework.request import Request

from authentication.models import PersonalUser, Organization


class IsPatient(permissions.BasePermission):
    """
    Global permission check to check for patients .
    """

    def has_permission(self, request, view):
        return PersonalUser.objects.filter(custom_user=request.user,
                                           category=PersonalUser.PersonalUserCategory.PATIENT).exists()


class IsProfessional(permissions.BasePermission):
    """
    Global permission check to check for professionals .
    """

    def has_permission(self, request, view):
        return PersonalUser.objects.filter(custom_user=request.user,
                                           category=PersonalUser.PersonalUserCategory.PROFESSIONAL).exists()


class IsOrganization(permissions.BasePermission):
    """
    Global permission check to check for organizations .
    """

    def has_permission(self, request, view):
        return Organization.objects.filter(custom_user=request.user).exists()


class IsHospital(permissions.BasePermission):
    """
    Global permission check to check for hospitals .
    """

    def has_permission(self, request, view):
        return Organization.objects.filter(custom_user=request.user,
                                           category=Organization.OrganizationCategory.HOSPITAL).exists()


class IsPharmacy(permissions.BasePermission):
    """
    Global permission check to check for pharmacies .
    """

    def has_permission(self, request, view):
        return Organization.objects.filter(custom_user=request.user,
                                           category=Organization.OrganizationCategory.PHARMACY).exists()


class IsInsurance(permissions.BasePermission):
    """
    Global permission check to check for insurance .
    """

    def has_permission(self, request, view):
        return Organization.objects.filter(custom_user=request.user,
                                           category=Organization.OrganizationCategory.INSURANCE).exists()


class HasHOTPInUnsafeMethods(permissions.BasePermission):
    """
    Global permission check to check for HOTP in unsafe methods .
    """

    def has_permission(self, request: Request, view):
        return request.method in permissions.SAFE_METHODS or request.user.verify_otp(request.META.get("HTTP_HOTP", ""))
