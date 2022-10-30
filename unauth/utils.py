from datetime import datetime, timedelta

import jwt

from authentication.models import PersonalUser, Organization, CustomUser
from backend.settings import RSA_private_key_obj, RSA_public_key_obj


def generate_user_jwt(user):
    if PersonalUser.objects.filter(custom_user=user).exists():
        type_of_user = "1"
        category = PersonalUser.objects.get(custom_user=user).category
    elif Organization.objects.filter(custom_user=user).exists():
        type_of_user = "2"
        category = Organization.objects.get(custom_user=user).category
    else:
        raise Exception("User type not found")
    payload = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'type': type_of_user,
        'category': category,
        'exp': datetime.now() + timedelta(hours=1)
    }
    return jwt.encode(payload, RSA_private_key_obj, algorithm='RS256')


def validate_user_jwt(token):
    payload = jwt.decode(token, RSA_public_key_obj, algorithms=['RS256'])
    return CustomUser.objects.get(id=payload['id'])
