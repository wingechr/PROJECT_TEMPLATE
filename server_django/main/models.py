from django.contrib.auth.models import User
from django.db import models


class Version(models.Model):
    version = models.CharField(
        max_length=128, null=False, blank=False, primary_key=True
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
