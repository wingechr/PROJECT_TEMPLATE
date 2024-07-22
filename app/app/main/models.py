from django.contrib.auth.models import User
from django.db import models


class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    upload = models.ForeignKey(
        to=Upload, on_delete=models.DO_NOTHING, related_name="datasets"
    )
    key = models.CharField(max_length=128)
    value = models.JSONField(null=False, blank=True)

    class Meta:
        # upload + all key fields
        # key_fields = ["example_key_field_1"]
        unique_together = ["upload", "key"]

    @property
    def timestamp(self):
        return self.upload.timestamp


class UserSetting(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=128)
    value = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "key"]
