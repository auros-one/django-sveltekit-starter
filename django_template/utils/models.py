import datetime
import uuid

from django.db import models


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def deleted(self):
        return super().get_queryset().filter(deleted=True)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = BaseModelManager()

    class Meta:
        ordering = ["-created"]
        abstract = True

    def save(self, *args, **kwargs):
        if self.deleted:
            self.deleted_at = datetime.datetime.now(datetime.UTC)
        else:
            self.deleted_at = None
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
