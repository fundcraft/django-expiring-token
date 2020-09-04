from unittest import mock
from unittest.mock import patch

import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from drf_expiring_token.authentication import ExpiringTokenAuthentication, is_token_expired
from drf_expiring_token.models import ExpiringToken


class ExpiringTokenAuthenticationTestCase(TestCase):

    """Test the authentication class directly."""

    def setUp(self):
        """Create a user and associated token."""
        self.username = 'test_username'
        self.email = 'test@g.com'
        self.password = 'test_password'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.key = 'jhfbgkjasnlkfmlkn'

        self.test_instance = ExpiringTokenAuthentication()

    def _create_token(self):
        self.token = ExpiringToken.objects.create(
            user=self.user,
            key=self.key
        )

    def test_non_expired(self):
        self._create_token()
        self.assertFalse(is_token_expired(self.token))

    def test_expired_token(self):
        with patch('django.utils.timezone.now',
                   mock.MagicMock(return_value=timezone.datetime(2020, 8, 17, 8, 1, 0, tzinfo=pytz.UTC))):
            self._create_token()
        with patch('django.utils.timezone.now',
                   mock.MagicMock(return_value=timezone.datetime(2020, 8, 17, 8, 1, 40, tzinfo=pytz.UTC))):
            self.assertTrue(is_token_expired(self.token))
