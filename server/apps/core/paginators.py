from rest_framework.pagination import (
    CursorPagination,
)
from rest_framework.pagination import (
    PageNumberPagination as BasePageNumberPagination,
)
from rest_framework.response import Response


class DynamicPaginationMixin:
    @property
    def pagination_class(self):
        if not hasattr(self, "request") or self.request is None:
            return getattr(self, "_default_pagination_class", None)

        user_agent = self.request.META.get("HTTP_USER_AGENT").lower()
        if "mobile" in user_agent or "dart" in user_agent:
            return CursorPagination

        return getattr(self, "_default_pagination_class", None)

    @pagination_class.setter
    def pagination_class(self, value):
        self._default_pagination_class = value


class PageNumberPagination(BasePageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "user-agent": self.request.META.get("HTTP_USER_AGENT").lower(),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page_size": self.page_size,
                "count": self.page.paginator.count,
                "results": data,
            }
        )


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    max_page_size = 100
