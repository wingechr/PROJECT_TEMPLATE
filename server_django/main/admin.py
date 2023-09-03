from django.contrib import admin  # noqa
from django.contrib.contenttypes.models import ContentType


class ContentTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(ContentType, ContentTypeAdmin)
