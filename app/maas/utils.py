from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 500


class StandardResultsOrdering(OrderingFilter):
    ordering_param = 'sort'
