from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PostPagination(PageNumberPagination):
    """
  custom paginator of Posts Route
  """
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100

    def get_paginated_response(self, data):
        print(self.request.path)

        return Response({
            'posts':
            data,
            'total':
            self.page.paginator.count,
            'pageNumber':
            self.request.query_params.get('page', 1),
            'pageSize':
            self.request.query_params.get('pageSize', 10),
            'pageCount':
            self.page.paginator.num_pages,
        })
