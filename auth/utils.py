import string
import random
import re

def generate_random_pw(length: int=16) -> str:
    """
    Generates a random password.

    Parameters
    ----------
    length: int
        The length of the returned password.
    Returns
    -------
    str
        The randomly generated password.
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length)).replace(' ','')

def validate_email(email):
    # Regular expression for validating an email
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # If the string matches the regular expression, it's a valid email
    return re.match(email_regex, email) is not None