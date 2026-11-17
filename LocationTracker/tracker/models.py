from django.db import models
import uuid

class LocationShare(models.Model):

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    permission_granted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.token)