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


class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ExampleDataset(models.Model):
    id = models.AutoField(primary_key=True)
    upload = models.ForeignKey(to=Upload, on_delete=models.DO_NOTHING)
    example_key_field_1 = models.CharField(max_length=128)
    example_value_field_1 = models.FloatField(null=True, blank=True)

    class Meta:
        # upload + all key fields
        # key_fields = ["example_key_field_1"]
        unique_together = ["upload", "example_key_field_1"]
