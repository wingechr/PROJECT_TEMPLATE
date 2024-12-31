from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str,
    token: str = None,
    is_superuser: bool = False,
    is_staff: bool = False,
):
    try:
        User.objects.create_user(  # use create_user! (password hashing and so on)
            username,
            password=password,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
        ).save()
    except IntegrityError:
        print(f"User {username} already exists")

    user = User.objects.get(email=email)

    # add token
    if token:
        try:
            Token(user=user, key=token).save()
        except IntegrityError:
            print(f"Token for {username} already exists")


class Command(BaseCommand):
    """Create admin user if not exist"""

    def handle(self, *args, **options):
        # create admin user
        create_user(
            username=settings.ADMIN_NAME,
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
            token=settings.ADMIN_TOKEN,
            is_superuser=True,
            is_staff=True,
        )
        # create test user
        create_user(
            username=settings.TESTUSER_NAME,
            email=settings.TESTUSER_MAIL,
            password=settings.TESTUSER_PASSWORD,
            is_superuser=False,
            is_staff=False,
        )
