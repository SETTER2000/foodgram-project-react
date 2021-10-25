from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationAll(PageNumberPagination):
    page_size = 6
    max_page_size = 300


class PaginationNull(PageNumberPagination):
    """Без пагинации."""

    def get_paginated_response(self, data):
        return Response(data)



class FoodgramPagination(PageNumberPagination):

    page_size = 10
    page_query_param = "page"
    page_size_query_param = "limit"