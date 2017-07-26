from django.core.exceptions import ValidationError

def validate_even(value):
    # takes in a function and validates whatever that value actually is
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

def validate_email(value):
    email = value
    if ".edu" in email:
        raise ValidationError("We do not accept .edu email")

CATEGORIES = ['Mexican', 'Asian', 'American', 'Whatever']

def validate_category(value):
    cat = value.capitalize()
    # capitalize() capitalizes just the first letter of the word 
    if not value in CATEGORIES and not cat in CATEGORIES:
        raise ValidationError(f"{value} not a valid category")
    # return cat
    # All validation does is check to make sure that the condition is true (it's only looking for a raised
    # validation error, nothing else) so returning cat here won't save the capitalized form of your category word. 
    # At the moment all lower case returns valid even though in CATEGORIES the first letter is capitalized, 
    # however it saves in the database as small letters. So when you want to modify the data itself you can do it
    # inside of the pre_save/post_save receiver