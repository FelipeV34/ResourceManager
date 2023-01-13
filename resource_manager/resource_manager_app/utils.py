"""API utils."""

import string
from django.core.exceptions import ValidationError

ALPHABET = string.ascii_letters + string.digits


def letter_number_only_validator(value: str):
    """Raises ValidationError if the given value contains any character other than letters or numbers."""
    params = {"values": ""}
    for letter in value:
        if letter not in ALPHABET:
            params["values"] += letter

    if len(params["values"]) > 0:
        raise ValidationError("Values not allowed", params=params)
