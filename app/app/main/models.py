from django.contrib.auth.models import User
from django.db import models


class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=128, null=False, blank=False)
    value = models.TextField(max_length=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["created_by", "key"]
