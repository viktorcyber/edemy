from core.paginators import DynamicPaginationMixin, StandardResultsSetPagination
from courses.models import Category, Course
from courses.serializers import CategorySerializer, CourseSerializer
from elasticsearch_dsl import Q
from rest_framework import generics, viewsets


class CategoryViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    """List view for categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(DynamicPaginationMixin, viewsets.ReadOnlyModelViewSet):
    """Read-only view set for courses"""

    queryset = Course.objects.all().order_by("-date_created")
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def generate_q_expression(self, query):
        return Q(
            "multi_match",
            query=query,
            fields=[
                "name",
                "description",
            ],
            fuzziness="auto",
        )
