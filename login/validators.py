from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator


def validate_password_strength(value):
    """Validates that a password is as least 6 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 6
    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters long.').format(min_length))

    max_length = 50
    if len(value) > max_length:
        raise ValidationError(_('Password must be at most {0} characters long.').format(max_length))

    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must contain at least 1 letter.'))

    # check for upper case
    if not any(char.isupper() for char in value):
        raise ValidationError(_('Password must contain at least 1 upper case.'))

    # check for lower case
    if not any(char.islower() for char in value):
        raise ValidationError(_('Password must contain at least 1 lower case.'))

    # check for special character
    specialCharacters = ['$', '#', '@', '!', '*']
    if not any(char in specialCharacters for char in value):
        raise ValidationError(_('Password must contain at least 1 special character ($, #, @, !, *)'))


def validate_confirm_password(confirm_password,password):
    if password != confirm_password:
        raise ValidationError("Password and Confirm Password does not match")

phone_regex = RegexValidator(regex=r'\+?1?\s*\(?-*\.*(\d{2,5})\)?\.*-*\s*(\d{2,5})\.*-*\s*(\d{3,5})$', message="Phone number must be entered in the format: '+999-999-9999'. Up to 15 digits allowed.")



