from django.contrib import admin
from main.models import Dataset, Upload


class DatasetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dataset, DatasetAdmin)


class UploadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Upload, UploadAdmin)
