import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from core.models import TimestampMixin, IsActiveMixin, SlugMixin


User = get_user_model()


class Category(SlugMixin, TimestampMixin, IsActiveMixin):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Course(SlugMixin, TimestampMixin, IsActiveMixin):
    class Level(models.TextChoices):
        BEGINNER = "BEGINNER", _("Beginner")
        INTERMEDIATE = "INTERMEDIATE", _("Intermediate")
        ADVANCED = "ADVANCED", _("Advanced")

    class Status(models.TextChoices):
        DRAFT = "DRAFT", _("Draft")
        PUBLISHED = "PUBLISHED", _("Published")
        ARCHIVED = "ARCHIVED", _("Archived")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
    )
    level = models.CharField(
        max_length=20, choices=Level.choices, default=Level.BEGINNER
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator_courses"
    )

    layout = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")
        indexes = [
            models.Index(fields=["status", "date_created"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title


class Chapter(TimestampMixin, IsActiveMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="chapters"
    )

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "position"], name="unique_chapter_position_per_course"
            )
        ]


class Lesson(TimestampMixin, IsActiveMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(max_length=500, blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
    is_preview_free = models.BooleanField(default=False)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name="lessons"
    )

    ai_quizzes = models.JSONField(
        default=list, blank=True, help_text="[ {question, options: [], answer} ]"
    )

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["chapter", "position"],
                name="unique_lesson_position_per_chapter",
            )
        ]
