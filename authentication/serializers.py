from authentication.models import CustomUser, Organization, PersonalUser
from rest_framework import serializers


class CustomUserExternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'wallet_address')


class OrganizationExternalSerializer(serializers.ModelSerializer):
    custom_user_detailed = CustomUserExternalSerializer(read_only=True, source='custom_user')

    class Meta:
        model = Organization
        fields = ('id', 'category', 'description', 'images', 'location', 'custom_user_detailed')


class PersonalUserExternalSerializer(serializers.ModelSerializer):
    organization_detailed = OrganizationExternalSerializer(read_only=True, source='organization')
    custom_user_detailed = CustomUserExternalSerializer(read_only=True, source='custom_user')

    class Meta:
        model = PersonalUser
        fields = ('id', 'address', 'category', 'organization_detailed', 'custom_user_detailed')


class PersonalUserSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalUser
        fields = "__all__"


class OrganizationSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
