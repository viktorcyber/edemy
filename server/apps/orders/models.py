import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.models import TimestampMixin, IsActiveMixin, SlugMixin
from courses.models import Course


User = get_user_model()


class Purchase(SlugMixin, TimestampMixin, IsActiveMixin):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        COMPLETED = "completed", _("Completed")
        FAILED = "failed", _("Failed")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    xp_earned = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="purchases"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_user_course_enrollment"
            )
        ]


class CourseProgress(SlugMixin, TimestampMixin, IsActiveMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progresses")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="user_progresses"
    )
    is_completed = models.BooleanField(default=False)

    completed_lessons = models.JSONField(default=list, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_user_course_progress"
            )
        ]
