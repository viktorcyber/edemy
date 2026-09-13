from rest_framework import serializers
from courses.models import Category, Course
from core.serializers import DynamicFieldsModelSerializer


class CategorySerializer(DynamicFieldsModelSerializer):
    class Meta(DynamicFieldsModelSerializer.Meta):
        model = Category


class CourseSerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer(fields=("id", "slug", "name"))

    class Meta(DynamicFieldsModelSerializer.Meta):
        model = Course
