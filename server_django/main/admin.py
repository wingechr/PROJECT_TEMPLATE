from django.contrib import admin

from . import models


class ExampleAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Example, ExampleAdmin)
