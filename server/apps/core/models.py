from django.db import models
from django.utils.text import slugify


class TimestampMixin(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, db_index=True
    )
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["is_active"]),
        ]

    def soft_delete(self):
        self.is_active = False
        self.save()


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, blank=True)

    _FALLBACK_FIELDS = ("title", "name", "label")

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            for field_name in self._FALLBACK_FIELDS:
                if hasattr(self, field_name):
                    source = getattr(self, field_name)
                    self.slug = slugify(source)
                    break
            else:
                raise ValueError(
                    f"No field found for slug generation in {self.__class__.__name__}. "
                    f"Define _fallback_fields or override save."
                )
        super().save(*args, **kwargs)
