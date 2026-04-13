from django.core.paginator import EmptyPage
from rest_framework import pagination
from rest_framework.response import Response

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
    message = None

    def paginate_queryset(self, queryset, request, view=None):

        """
        Paginate the queryset if required, either returning a page object,
        or `None` if pagination is not configured for this view.

        :param queryset: The queryset to paginate
        :param request: The request object that is used to determine the page number
        :param view: The view object that is used to determine the page number
        :return: A page object if pagination is configured for this view, or `None` otherwise
        """
        self.queryset = queryset
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)

        try:
            self.page = paginator.page(page_number)
        except EmptyPage:
            self.page = paginator.page(paginator.num_pages)

        return list(self.page)
    
    def get_paginated_response(self, data):
        """
        Returns a paginated response as a rest_framework.response.Response object.

        The response will contain the following keys in the response data:

        - status: a string describing the status of the response
        - links: a dictionary containing links to the next and previous pages
        - count: the total number of objects in the result set
        - total_pages: the total number of pages in the result set
        - current_page: the number of the current page in the result set
        - results: a list of objects in the current page of the result set

        :param data: the list of objects to be paginated
        :return: a Response object containing the paginated data
        """
        return Response(
            {
                "status": "success",
                "message": self.message or "Data fetched successfully",
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data,
            }
        )