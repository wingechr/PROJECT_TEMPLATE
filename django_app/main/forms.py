from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.forms import CharField, PasswordInput


class RegistrationForm(UserCreationForm):

    # remove radio buttons: "Password-based authentication:"
    usable_password = None

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "language",
            "password1",
            "password2",
        ]


class UserPasswordChangeForm(PasswordChangeForm):
    # overwrite from PasswordChangeForm
    old_password = CharField(
        label="Old password",
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"}),
        required=False,
    )

    class Meta:
        model = get_user_model()


class UserProfileForm(UserChangeForm):
    # Overwrite from UserChangeForm
    password = None

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "language"]
