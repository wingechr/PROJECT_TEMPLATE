from django.contrib import admin
from main.models import UserData


class UserDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserData, UserDataAdmin)
