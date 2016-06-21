from django.db import transaction
from django import forms

from registration.forms import RegistrationForm

from cmdrs.models import Commander


class SignupForm(RegistrationForm):
    commander_name = forms.CharField(
        help_text='This should match your in-game Commander Name (minus the '
                  'CMDR portion)'
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def save(self):
        with transaction.atomic():
            user = super(SignupForm, self).save()
            Commander.objects.create(
                user=user,
                name=self.cleaned_data['commander_name']
            )

        return user
