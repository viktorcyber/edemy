from core.serializers import DynamicFieldsModelSerializer
from courses.models import Category, Course


class CategorySerializer(DynamicFieldsModelSerializer):
    class Meta(DynamicFieldsModelSerializer.Meta):
        model = Category


class CourseSerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer(fields=("id", "slug", "name"))

    class Meta(DynamicFieldsModelSerializer.Meta):
        model = Course
