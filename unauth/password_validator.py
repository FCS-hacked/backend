from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UnauthPasswordValidator:
    def validate(self, password: str):
        if password.lower() == password or password.upper() == password or \
                len({'!', '$', '%', '*', '(', '#', ')', '@', '^', '&'}.intersection(password)):
            raise ValidationError(
                _("Password must contain at least one uppercase and lowercase letter and one of !@#$%^&*()."),
                code="password_no_upper_lower_special_character",
            )

    def get_help_text(self):
        pass
