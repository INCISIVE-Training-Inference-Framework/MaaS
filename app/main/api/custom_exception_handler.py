from __future__ import unicode_literals

import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import Response, exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, IntegrityError) and not response:
        response = Response(
            {
                f'It seems there is a conflict between the data you are trying to save and your current data. Please review your entries and try again. {exc}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    if response:
        logger.error(response.data)
    return response
