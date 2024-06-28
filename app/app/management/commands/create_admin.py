from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token

from app.settings import ADMIN_PASSWORD, ADMIN_TOKEN

ADMIN_NAME = "admin"


class Command(BaseCommand):
    """Create admin user if not exist"""

    def handle(self, *args, **options):
        try:
            User.objects.create_user(  # use create_user! (password hashing and so on)
                username=ADMIN_NAME,
                password=ADMIN_PASSWORD,
                is_staff=True,
                is_active=True,
                is_superuser=True,
            ).save()
        except IntegrityError:
            print(f"User {ADMIN_NAME} already exists")

        user = User.objects.get(username=ADMIN_NAME)

        # add token
        try:
            Token(user=user, key=ADMIN_TOKEN).save()
        except IntegrityError:
            print(f"Token for {ADMIN_NAME} already exists")
