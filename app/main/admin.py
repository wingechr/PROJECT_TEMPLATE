from django.contrib import admin
from main.models import UserData


class VersionAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserData, VersionAdmin)
