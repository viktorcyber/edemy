import inngest.django
from accounts.apiviews import UserViewSet
from accounts.tasks import sync_user_from_clerk
from courses.apiviews import CategoryViewSet, CourseViewSet
from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from config.client import inngest_client

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("users", UserViewSet, basename="user")
router.register("categories", CategoryViewSet, basename="category")
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    inngest.django.serve(
        inngest_client,
        [sync_user_from_clerk],
    ),
    path("", include(router.urls)),
]
