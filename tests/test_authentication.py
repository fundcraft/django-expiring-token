from unittest import mock
from unittest.mock import patch

import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from drf_expiring_token.authentication import ExpiringTokenAuthentication
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

        self.test_instance = ExpiringTokenAuthentication()

        self.key = 'jhfbgkjasnlkfmlkn'

    def _create_token(self):
        return ExpiringToken.objects.create(
            user=self.user,
            key=self.key
        )

    def test_valid_token(self):
        """Check that a valid token authenticates correctly."""
        self.token = self._create_token()
        result = self.test_instance.authenticate_credentials(self.key)

        self.assertEqual(result[0], self.user)
        self.assertEqual(result[1], self.token)

    def test_invalid_token(self):
        """Check that an invalid token does not authenticated."""
        try:
            self.test_instance.authenticate_credentials('xyz789')
        except AuthenticationFailed as e:
            self.assertEqual(e.__str__(), 'Invalid Token')
        else:
            self.fail("AuthenticationFailed not raised.")

    def test_inactive_user(self):
        """Check that a token for an inactive user cannot authenticate."""
        self.token = self._create_token()

        # Make the user inactive
        self.user.is_active = False
        self.user.save()

        try:
            self.test_instance.authenticate_credentials(self.key)
        except AuthenticationFailed as e:
            self.assertEqual(e.__str__(), 'User is not active')
        else:
            self.fail("AuthenticationFailed not raised.")

    def test_expired_token(self):
        """Check that an expired token cannot authenticate."""
        with patch('django.utils.timezone.now',
                   mock.MagicMock(return_value=timezone.datetime(2020, 8, 17, 8, 1, 0, tzinfo=pytz.UTC))):
            self.token = self._create_token()

        with patch('django.utils.timezone.now',
                   mock.MagicMock(return_value=timezone.datetime(2020, 8, 17 , 8, 1, 40, tzinfo=pytz.UTC))):
            try:
                self.test_instance.authenticate_credentials(self.key)
            except AuthenticationFailed as e:
                self.assertEqual(e.__str__(), 'The Token is expired')
            else:
                self.fail("AuthenticationFailed not raised.")
