from django import forms
from django.contrib.auth.forms import PasswordChangeForm as _PasswordChangeForm
from django.contrib.auth.models import User


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class PasswordChangeForm(_PasswordChangeForm):
    pass
