from django.contrib.auth.models import User
from django.test import TestCase

from cmdrs.models import Commander

from ..forms import SignupForm


class TestSignupForm(TestCase):
    def test_save(self):
        # Sanity check.
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='DavidBraben')

        with self.assertRaises(Commander.DoesNotExist):
            Commander.objects.get(name='Braben')

        form = SignupForm({
            'username': 'DavidBraben',
            'email': 'david@frontier.co.uk',
            'commander_name': 'Braben',
            'password1': "#cobra4lyfe",
            'password2': "#cobra4lyfe",
        })

        self.assertTrue(form.is_valid())

        # Trigger the save.
        form.save()

        # Make sure they are found. If not, an exception will be thrown, which is
        # good enough for a failed test.
        user = User.objects.get(username='DavidBraben')
        cmdr = Commander.objects.get(name='Braben')

        # Make sure the relation exists.
        self.assertEqual(user.pk, cmdr.user.pk)
