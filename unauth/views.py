from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.models import CustomUser, PersonalUser, Organization
from backend import settings
from unauth.utils import generate_user_jwt


@extend_schema(
    request=inline_serializer(
        name="Login",
        fields={
            "email": serializers.EmailField(),
            "password": serializers.CharField(),
        }
    )
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.verify_otp(request.META.get("HTTP_HOTP", "")):
        return Response({'error': 'Invalid HOTP or not HOTP present'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'token': generate_user_jwt(user)}, status=status.HTTP_200_OK)


@extend_schema(
    request=inline_serializer(
        name="Register as Personal User",
        fields={
            "email": serializers.EmailField(),
            "password1": serializers.CharField(),
            "password2": serializers.CharField(),
            "first_name": serializers.CharField(),
            "last_name": serializers.CharField(),
            "address": serializers.CharField(),
            "date_of_birth": serializers.DateField(),
            "category": serializers.ChoiceField(choices=PersonalUser.PersonalUserCategory.choices),
            "proof_of_identity": serializers.FileField(),
            "proof_of_address": serializers.FileField(),
            "health_license": serializers.FileField(),
            "organization": serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all()),
        }
    )
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_as_personal_user(request):
    mandatory_fields = ['email', 'password1', 'password2', 'category', 'address', 'date_of_birth', 'first_name',
                        'proof_of_address', 'proof_of_identity']
    for field in mandatory_fields:
        if field not in request.data:
            return Response({'error': f'{field} is missing'}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data.get('email')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    if password1 != password2:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    validate_password(password1)
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name', "")
    user = CustomUser.objects.create_user(email=email, password=password1, first_name=first_name, last_name=last_name,
                                          is_active=False, username=email)
    PersonalUser.objects.create(category=request.data.get('category'), address=request.data.get('address'),
                                date_of_birth=request.data.get('date_of_birth'),
                                proof_of_address=request.data.get('proof_of_address'),
                                proof_of_identity=request.data.get('proof_of_identity'), custom_user=user,
                                health_license=request.data.get('health_license', None),
                                organization=request.data.get('organization', None))
    send_mail(
        subject='User Registration',
        message=f'Your account has been registered successfully. Admin will verify your registration and activate your account. HOTP - {user.HOTP_secret}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response({'message': 'PersonalUser created successfully'}, status=status.HTTP_201_CREATED)


@extend_schema(
    request=inline_serializer(
        name="Register as Organization",
        fields={
            "email": serializers.EmailField(),
            "password1": serializers.CharField(),
            "password2": serializers.CharField(),
            "first_name": serializers.CharField(),
            "last_name": serializers.CharField(),
            "category": serializers.ChoiceField(choices=Organization.OrganizationCategory.choices),
            "licenses": serializers.FileField(),
            "permits": serializers.FileField(),
            "description": serializers.CharField(),
            "images": serializers.CharField(),
            "location": serializers.CharField(),
        }
    )
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_as_organization(request):
    mandatory_fields = ['email', 'password1', 'password2', 'category', 'description', 'images', 'first_name',]
    for field in mandatory_fields:
        if field not in request.data:
            return Response({'error': f'{field} is missing'}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data.get('email')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')
    if password1 != password2:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    validate_password(password1)
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name', "")
    user = CustomUser.objects.create_user(email=email, password=password1, first_name=first_name, last_name=last_name,
                                          is_active=False, username=email)
    Organization.objects.create(category=request.data.get('category'), licenses=request.data.get('licenses'),
                                permits=request.data.get('permits'), description=request.data.get('description'),
                                images=request.data.get('images'), location=request.data.get('location'),
                                custom_user=user)
    send_mail(
        subject='Organization Registration',
        message=f'Your organization has been registered successfully. Admin will verify your organization and activate your account. HOTP - {user.HOTP_secret}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response({'message': 'Organization created successfully'}, status=status.HTTP_201_CREATED)
