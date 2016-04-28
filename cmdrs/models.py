import hashlib
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Commander(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    api_token = models.CharField(max_length=64, blank=True, db_index=True)
    created = models.DateTimeField(default=timezone.now, db_index=True)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.name

    def generate_token(self):
        unique = str(uuid.uuid4())
        return hashlib.md5(unique).hexdigest()

    def save(self, *args, **kwargs):
        if not self.api_token:
            self.api_token = self.generate_token()

        self.updated = timezone.now()
        return super(Commander, self).save(*args, **kwargs)
