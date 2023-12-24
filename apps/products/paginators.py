# DRF
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList


class ProductPageNumberPaginator(PageNumberPagination):
    page_size_query_param: str = 'size'
    page_query_param: str = 'page'
    max_page_size: int = 3
    page_size: int = 3

    def get_paginated_response(self, data: ReturnList) -> Response:
        request = self.request
        query_params = request.query_params.copy()
        latitude = query_params.get('latitude')
        longitude = query_params.get('longitude')

        extra_context = {
            'latitude': latitude,
            'longitude': longitude
        }

        if latitude and longitude:
            query_params.pop('latitude')
            query_params.pop('longitude')

        url = f"{request.path}?{query_params.urlencode()}"

        response = Response(
            {
                'pagination': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'pages': self.page.paginator.num_pages,
                    'count': self.page.paginator.count
                },
                'results': data,
                'url': url
            },
            context=extra_context
        )
        return response