from django.contrib.auth.models import User
from django.db import transaction
from django import forms

from cmdrs.models import Commander


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField()
    commander_name = forms.CharField(help_text='This should match your in-game Commander Name')
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super(RegistrationForm, self).clean()
        password = cleaned.get('password')
        confirm_password = cleaned.get('confirm_password')

        if not password:
            raise forms.ValidationError(
                "Passwords can not be empty/blank."
            )

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned

    def create_user(self):
        with transaction.atomic():
            user = User(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                is_active=False
            )
            user.set_password(self.cleaned_data['password'])
            user.save()

            cmdr = Commander.objects.create(
                name=self.cleaned_data['commander_name']
            )

        return user
