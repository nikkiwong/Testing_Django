from django.core.exceptions import ValidationError

def validate_even(value):
    # takes in a function and validates whatever that value actually is
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

def clean_email(value):
    email = value
    if ".edu" in email:
        raise ValidationError("We do not accept .edu email")