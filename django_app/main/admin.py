from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

# from django.contrib.admin import ModelAdmin

User = get_user_model()

admin.site.site_header = settings.SITE_TITLE  # + " Admin"
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = settings.SITE_TITLE
admin.site.site_url = None  # remove "View Site" link


admin.site.register(User)
