from django.contrib.auth.models import User
from django.test import TestCase
from django.test import override_settings
import anyfield_auth_backend

@override_settings(AUTHENTICATION_BACKENDS=['anyfield_auth_backend.anyfield_auth.AnyfieldAuthBackend',])
class BaseBackendTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user1', email='kauan@maxttor.com', password="123",
                                            first_name="Kauan")
        cls.user = User.objects.create_user(username='user2', email='rodrigo@maxttor.com', password="456",
                                            first_name="Kauan")

    def test_username_login(self):
        anyfield_auth_backend.AUTH_ANYFIELDS = ['username']
        anyfield_auth_backend.AUTH_ANYFIELDS_ONLY_UNIQUE_USERS = True
        self.assertFalse(self.client.login(username='user1', password='WRONG_PASSWORD'))
        self.assertFalse(self.client.login(username='kauan@maxttor.com', password='123'))
        self.assertTrue(self.client.login(username='user1', password='123'))

    def test_multiple_fields_login(self):
        anyfield_auth_backend.AUTH_ANYFIELDS = ['username', 'first_name', 'email']
        anyfield_auth_backend.AUTH_ANYFIELDS_ONLY_UNIQUE_USERS = True
        self.assertFalse(self.client.login(username='user1', password='WRONG_PASSWORD'))
        self.assertTrue(self.client.login(username='kauan@maxttor.com', password='123'))
        self.assertTrue(self.client.login(username='user1', password='123'))

        # first_name match more than one user and fail
        self.assertFalse(self.client.login(username='Kauan', password='123'))

        # If unique_users = False.
        anyfield_auth_backend.AUTH_ANYFIELDS_ONLY_UNIQUE_USERS = False
        # Both users could be successful authenticated!
        self.assertTrue(self.client.login(username='Kauan', password='123'))
        self.assertTrue(self.client.login(username='Kauan', password='456'))
