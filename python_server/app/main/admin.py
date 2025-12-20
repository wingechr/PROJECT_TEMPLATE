"""Register models for admin interface."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

User = get_user_model()

admin.site.site_header = settings.SITE_TITLE
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = settings.SITE_TITLE
admin.site.site_url = None  #  type:ignore removes "View Site" link


class UserAdmin(DefaultUserAdmin):
    """We need special user admin class to properly handle password encryption"""

    # add language in new section "Additional info"
    fieldsets = tuple(DefaultUserAdmin.fieldsets or []) + [
        ("Additional info", {"fields": ("language",)}),
    ]  # type:ignore

    # add language,email in creation
    add_fieldsets = DefaultUserAdmin.add_fieldsets + (
        (None, {"fields": ("language", "email")}),
    )


admin.site.register(User, UserAdmin)
