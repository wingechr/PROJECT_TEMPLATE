# coding: utf-8
import logging  # noqa

from django.contrib.auth.models import User
from django.db import models  # noqa


class Example(models.Model):
    summary = models.CharField(max_length=32)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (("assign_task", "Assign task"),)
