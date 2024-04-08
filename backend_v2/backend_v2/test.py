from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .permissions import IsAuthenticatedByAuthServer
from unittest.mock import patch
import requests_mock

class PermissionTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_permission(self):
        # Mock the response from the authentication server
        with requests_mock.mock() as m:
            # Mocking a successful token verification response
            m.post('http://example.com/api/token/verify/', status_code=200, json={'is_admin': True})

            # Create a request with a mock token in the headers
            request = self.factory.get('/')
            request.headers['Authorization'] = 'Bearer mock_token'

            # Instantiate the permission class
            permission = IsAuthenticatedByAuthServer()

            # Check if the permission is granted
            has_permission = permission.has_permission(request, None)

            # Assert that the permission is granted (True)
            self.assertTrue(has_permission)

    def test_permission_failure(self):
        # Mock the response from the authentication server
        with requests_mock.mock() as m:
            # Mocking a failed token verification response
            m.post('http://example.com/api/token/verify/', status_code=401)

            # Create a request with a mock token in the headers
            request = self.factory.get('/')
            request.headers['Authorization'] = 'Bearer mock_token'

            # Instantiate the permission class
            permission = IsAuthenticatedByAuthServer()

            # Check if the permission is granted
            has_permission = permission.has_permission(request, None)

            # Assert that the permission is denied (False)
            self.assertFalse(has_permission)
