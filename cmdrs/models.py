import hashlib
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Commander(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    api_token = models.CharField(max_length=64, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.api_token:
            unique = str(uuid.uuid4())
            self.api_token = hashlib.md5(unique).hexdigest()

        self.updated = timezone.now()
        return super(Commander, self).save(*args, **kwargs)
