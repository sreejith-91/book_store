from django.utils.crypto import get_random_string
from django.utils.text import slugify
import re
EMAIL_REGEX = re.compile('^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$')
def generate_slug(slug_name=None, string_length=15):
    """

    :param slug_name:
    :param string_length:
    :return: slug_generated
    """
    unique_ids = get_random_string(length=string_length)
    if slug_name:
        slug_generated = slugify(slug_name) + "-" + unique_ids
    else:
        slug_generated = unique_ids
    return slug_generated

def validate_email(value):
    response = False
    if bool(EMAIL_REGEX.match(str(value))):
        response = True
    return response