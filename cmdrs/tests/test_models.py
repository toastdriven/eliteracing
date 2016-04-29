import hashlib
import mock
import uuid

from django.test import TestCase

from ..models import Commander


class CommanderTestCase(TestCase):
    def test_generate_token(self):
        with mock.patch.object(uuid, 'uuid4', return_value='a_test'):
            cmdr = Commander(
                name='Branch'
            )
            self.assertEqual(
                cmdr.generate_token(),
                hashlib.md5('a_test').hexdigest()
            )

    def test_save(self):
        # We need to ensure tokens get auto-populated here.
        cmdr = Commander.objects.create(
            name='Branch'
        )
        self.assertTrue(len(cmdr.api_token) > 0)
