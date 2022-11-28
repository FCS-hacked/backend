from datetime import datetime, timedelta

import jwt
from rest_framework.exceptions import AuthenticationFailed

from backend.settings import RSA_private_key_obj, RSA_public_key_obj


def generate_user_jwt(user):
    from authentication.models import PersonalUser, Organization
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
        'exp': datetime.now() + timedelta(hours=2),
        'two_factor_enabled': user.two_factor_enabled,
    }
    return jwt.encode(payload, RSA_private_key_obj, algorithm='RS256')


def validate_user_jwt(token):
    from authentication.models import CustomUser
    payload = jwt.decode(token, RSA_public_key_obj, algorithms=['RS256'])
    custom_user = CustomUser.objects.get(id=payload['id'])
    if not custom_user.is_active:
        raise AuthenticationFailed("User is not active")
    return custom_user


def check_password(password, encoded, setter=None, preferred="default"):
    """
    Return a boolean of whether the raw password matches the three
    part encoded digest.

    If setter is specified, it'll be called when you need to
    regenerate the password.
    """
    from django.contrib.auth.hashers import is_password_usable
    if password is None or not is_password_usable(encoded):
        return False

    from django.contrib.auth.hashers import get_hasher
    preferred = get_hasher(preferred)
    try:
        from django.contrib.auth.hashers import identify_hasher
        hasher = identify_hasher(encoded)
    except ValueError:
        # encoded is gibberish or uses a hasher that's no longer installed.
        return False

    hasher_changed = hasher.algorithm != preferred.algorithm
    must_update = hasher_changed or preferred.must_update(encoded)
    is_correct = hasher.verify(password, encoded)

    # If the hasher didn't change (we don't protect against enumeration if it
    # does) and the password should get updated, try to close the timing gap
    # between the work factor of the current encoded password and the default
    # work factor.
    if not is_correct and not hasher_changed and must_update:
        hasher.harden_runtime(password, encoded)

    if setter and is_correct and must_update:
        setter(password)
    return is_correct
