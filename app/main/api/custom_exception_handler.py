from __future__ import unicode_literals
from django.db import IntegrityError
from rest_framework.views import Response, exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, IntegrityError) and not response:
        response = Response(
            {
                'It seems there is a conflict between the data you are trying to save and your current data. Please review your entries and try again.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return response
