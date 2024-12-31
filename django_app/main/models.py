from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField


class User(AbstractUser):
    # objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    # additional fields
    language = CharField(
        max_length=2,
        choices=[(code, name) for code, name in settings.LANGUAGES],
        null=False,
        default="en",
    )
