from django.test import TestCase
from rest_framework.test import APIRequestFactory
from unittest.mock import patch

from apps.utils.permissions import (
    IsAuthenticatedByAuthServer,
    _extract_bearer_token,
    _is_admin_user,
)


class AuthServerPermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = IsAuthenticatedByAuthServer()

    def test_extract_bearer_token(self):
        self.assertEqual(
            _extract_bearer_token("Bearer abc.def.ghi"),
            "abc.def.ghi",
        )
        self.assertEqual(_extract_bearer_token("abc.def.ghi"), "abc.def.ghi")

    def test_is_admin_user_top_level_flag(self):
        self.assertTrue(_is_admin_user({"is_admin": True}))

    def test_is_admin_user_nested_role_general_admin(self):
        self.assertTrue(
            _is_admin_user({"user": {"role": "general_admin", "email": "a@b.com"}})
        )

    def test_is_admin_user_role_with_spaces(self):
        self.assertTrue(_is_admin_user({"user": {"role": "General Admin"}}))

    def test_is_admin_user_rejects_student(self):
        self.assertFalse(_is_admin_user({"user": {"role": "student"}}))

    @patch("apps.utils.permissions.requests.post")
    def test_permission_accepts_top_level_is_admin(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"is_admin": True}

        request = self.factory.post("/api/v2/cohort/portal-invite/send/")
        request.headers["Authorization"] = "Bearer test-token"

        self.assertTrue(self.permission.has_permission(request, None))
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args.kwargs
        self.assertEqual(call_kwargs["json"]["token"], "test-token")

    @patch("apps.utils.permissions.requests.post")
    def test_permission_accepts_general_admin_role(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "user": {"role": "general_admin", "email": "admin@example.com"}
        }

        request = self.factory.post("/api/v2/cohort/portal-invite/send/")
        request.headers["Authorization"] = "Bearer test-token"

        self.assertTrue(self.permission.has_permission(request, None))

    @patch("apps.utils.permissions.requests.post")
    def test_permission_denied_for_non_admin_role(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "user": {"role": "student", "email": "student@example.com"}
        }

        request = self.factory.post("/api/v2/cohort/portal-invite/send/")
        request.headers["Authorization"] = "Bearer test-token"

        self.assertFalse(self.permission.has_permission(request, None))
