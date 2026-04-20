from unittest.mock import MagicMock, Mock, patch

import requests
from django.test import SimpleTestCase, TestCase, override_settings
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.test import APIClient

from cohort import views as cohort_views
from .helpers.portal import (
    create_portal_onboarding_invite,
    is_zk_course_name,
    normalize_approval_status,
)


class VerifyPaymentSerializerTests(SimpleTestCase):
    def test_accepts_email_with_optional_payment_id_and_status(self):
        from cohort.serializers import VerifyPaymentByEmailSerializer

        s = VerifyPaymentByEmailSerializer(
            data={
                "email": "user@example.com",
                "paymentId": "fiat-1776441344601-zve4ev",
                "status": True,
            }
        )
        self.assertTrue(s.is_valid(), s.errors)
        self.assertEqual(s.validated_data["email"], "user@example.com")
        self.assertEqual(s.validated_data["paymentId"], "fiat-1776441344601-zve4ev")
        self.assertTrue(s.validated_data["status"])

    def test_email_only_is_valid(self):
        from cohort.serializers import VerifyPaymentByEmailSerializer

        s = VerifyPaymentByEmailSerializer(data={"email": "user@example.com"})
        self.assertTrue(s.is_valid(), s.errors)


@override_settings(
    SECURE_SSL_REDIRECT=False,
    PORTAL_ONBOARDING_URL="",
    PORTAL_INTERNAL_API_KEY="",
)
class VerifyPaymentAndConfirmationPaymentStatusTests(TestCase):
    """
    Payment portal must mark the correct Participant row paid when one email has
    multiple registrations; send-confirmation must set payment_status as well.
    """

    VERIFY_URL = "/api/v2/cohort/participant/verify-payment-by-email/"
    API_KEY = "test-verify-payment-key"

    def setUp(self):
        self.client = APIClient()
        from cohort.models import Course, Participant, Registration

        self.reg_old = Registration.objects.create(
            name="Web3 Cohort XIV", cohort="Cohort-XIV", is_open=True
        )
        self.reg_new = Registration.objects.create(
            name="Web3 Cohort XV", cohort="Cohort-XV", is_open=True
        )
        self.course_old = Course.objects.create(
            name="Web3 Cohort XIV Course",
            description="Desc",
            extra_info="Extra",
            registration=self.reg_old,
        )
        self.course_new = Course.objects.create(
            name="Web3 Cohort XV Course",
            description="Desc",
            extra_info="Extra",
            registration=self.reg_new,
        )
        # Older row: still unpaid (the one the user paid for)
        self.participant_unpaid = Participant.objects.create(
            name="Jane",
            email="dup@example.com",
            wallet_address="0xaaa",
            registration=self.reg_old,
            course=self.course_old,
            cohort="Cohort-XIV",
            venue="online",
            payment_status=False,
        )
        # Newer row: already paid (e.g. another cohort) — email-only verify must not target this
        self.participant_paid_newer = Participant.objects.create(
            name="Jane",
            email="dup@example.com",
            wallet_address="0xaaa",
            registration=self.reg_new,
            course=self.course_new,
            cohort="Cohort-XV",
            venue="online",
            payment_status=True,
        )

    def _verify_post(self, payload):
        return self.client.post(
            self.VERIFY_URL,
            payload,
            format="json",
            headers={"API-Key": self.API_KEY},
        )

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_targets_unpaid_row_when_newer_paid_exists(
        self, mock_handle_success
    ):
        mock_handle_success.side_effect = (
            lambda participant, serialized, serializer_class: serializer_class.Retrieve(
                participant
            ).data
        )

        response = self._verify_post({"email": "dup@example.com"})

        self.assertEqual(response.status_code, 200)
        self.participant_unpaid.refresh_from_db()
        self.assertTrue(self.participant_unpaid.payment_status)
        self.participant_paid_newer.refresh_from_db()
        self.assertTrue(self.participant_paid_newer.payment_status)
        mock_handle_success.assert_called_once()

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    def test_verify_payment_respects_status_false(self):
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()

        response = self._verify_post(
            {"email": "dup@example.com", "status": False}
        )

        self.assertEqual(response.status_code, 200)
        self.participant_unpaid.refresh_from_db()
        self.assertFalse(self.participant_unpaid.payment_status)

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_idempotent_when_already_paid(self, mock_handle):
        self.participant_unpaid.payment_status = True
        self.participant_unpaid.save()

        response = self._verify_post({"email": "dup@example.com"})

        self.assertEqual(response.status_code, 200)
        mock_handle.assert_not_called()


class PortalInviteHelperTests(SimpleTestCase):
    def test_is_zk_course_name_detects_zk_course(self):
        self.assertTrue(is_zk_course_name("Zero Knowledge Bootcamp"))
        self.assertTrue(is_zk_course_name("ZK Cohort XIV"))
        self.assertFalse(is_zk_course_name("Web3 Cohort XIV"))

    @override_settings(PORTAL_ONBOARDING_URL="", PORTAL_INTERNAL_API_KEY="")
    def test_create_portal_onboarding_invite_returns_none_without_config(self):
        participant = Mock(
            id=12,
            email="student@example.com",
            cohort="Cohort-XIV",
            status="accepted",
            course=Mock(),
        )
        participant.name = "Student Example"
        participant.course.name = "Web3 Cohort XIV"

        activation_url = create_portal_onboarding_invite(participant)

        self.assertIsNone(activation_url)

    def test_normalize_approval_status_aliases(self):
        self.assertEqual(normalize_approval_status("accepted"), "approved")
        self.assertEqual(normalize_approval_status("APPROVED"), "approved")
        self.assertEqual(normalize_approval_status("declined"), "rejected")
        self.assertEqual(normalize_approval_status("suspended"), "revoked")
        self.assertEqual(normalize_approval_status(""), "approved")


class RegistrationEmailTemplateTests(SimpleTestCase):
    def test_non_zk_templates_render_activation_url_when_present(self):
        activation_url = "https://portal.example.com/activate?token=abc"
        template_names = [
            "cohort/web3_registration_email.html",
            "cohort/rust_registration_email.html",
            "other_registration_email.html",
        ]

        for template_name in template_names:
            with self.subTest(template_name=template_name):
                rendered = render_to_string(
                    template_name,
                    {"name": "Student Example", "activation_url": activation_url},
                )

                self.assertIn("Activate your student portal account", rendered)
                self.assertIn(activation_url, rendered)

    def test_web2_welcome_templates_are_static_no_portal_activation_block(self):
        for template_name in (
            "cohort/web2_launchpad_registration_email.html",
            "cohort/web2_advanced_frontend_registration_email.html",
            "cohort/web2_advanced_backend_registration_email.html",
        ):
            with self.subTest(template_name=template_name):
                rendered = render_to_string(template_name, {})
                self.assertIn("Hi there,", rendered)
                self.assertNotIn("Activate your student portal account", rendered)

    @patch("cohort.helpers.model.base.EmailMessage")
    @patch("cohort.helpers.model.base.render_to_string")
    @patch("cohort.models.Course.objects.get")
    def test_web2_registration_success_mail_static_context_and_template(
        self, mock_course_get, mock_render, mock_email_cls
    ):
        mock_render.return_value = "<html></html>"
        mock_email_cls.return_value = MagicMock()
        mock_course = MagicMock()
        mock_course.name = "Web2 Advanced Frontend"
        mock_course_get.return_value = mock_course

        from cohort.helpers.model.base import send_registration_success_mail

        send_registration_success_mail(
            "student@example.com",
            1,
            "Ignored Name",
            activation_url="https://portal.example.com/activate",
        )

        mock_render.assert_called_once()
        self.assertEqual(
            mock_render.call_args[0][0],
            "cohort/web2_advanced_frontend_registration_email.html",
        )
        self.assertEqual(mock_render.call_args[0][1], {})

    def test_send_participant_details_is_noop(self):
        from cohort.helpers.model.base import send_participant_details

        self.assertIsNone(
            send_participant_details(
                "student@example.com",
                1,
                {"name": "Student", "email": "student@example.com"},
            )
        )

    def test_non_zk_templates_hide_activation_url_when_missing(self):
        template_names = [
            "cohort/web3_registration_email.html",
            "cohort/rust_registration_email.html",
            "other_registration_email.html",
        ]

        for template_name in template_names:
            with self.subTest(template_name=template_name):
                rendered = render_to_string(
                    template_name,
                    {"name": "Student Example", "activation_url": None},
                )

                self.assertNotIn("Activate your student portal account", rendered)
                self.assertNotIn("portal.example.com/activate", rendered)

    @patch("apps.cohort.helpers.portal.requests.post")
    @override_settings(
        PORTAL_ONBOARDING_URL="http://localhost:8000/api/v1/onboarding/invite",
        PORTAL_INTERNAL_API_KEY="secret-key",
        PORTAL_REQUEST_TIMEOUT=5,
    )
    def test_create_portal_onboarding_invite_returns_activation_url(self, mock_post):
        response = Mock()
        response.json.return_value = {
            "activation_url": "https://portal.example.com/activate?token=abc"
        }
        response.raise_for_status.return_value = None
        mock_post.return_value = response

        participant = Mock(
            id=22,
            email="student@example.com",
            cohort="Cohort-XIV",
            status="accepted",
            course=Mock(),
        )
        participant.name = "Student Example"
        participant.course.name = "Web3 Cohort XIV"

        activation_url = create_portal_onboarding_invite(participant)

        self.assertEqual(
            activation_url, "https://portal.example.com/activate?token=abc"
        )
        mock_post.assert_called_once_with(
            "http://localhost:8000/api/v1/onboarding/invite",
            json={
                "email": "student@example.com",
                "full_name": "Student Example",
                "cohort": "Cohort-XIV",
                "course_name": "Web3 Cohort XIV",
                "external_student_id": "22",
                "source_system": "backend_v2",
                "source_email": "student@example.com",
                "approval_status": "approved",
            },
            headers={"X-Internal-API-Key": "secret-key"},
            timeout=(5.0, 5.0),
        )

    @patch("apps.cohort.helpers.portal.requests.post")
    @override_settings(
        PORTAL_ONBOARDING_URL="http://localhost:8000/api/v1/onboarding/invite",
        PORTAL_INTERNAL_API_KEY="secret-key",
        PORTAL_REQUEST_TIMEOUT=5,
    )
    def test_create_portal_onboarding_invite_skips_zk_courses(self, mock_post):
        participant = Mock(
            id=30,
            email="zkstudent@example.com",
            cohort="ZK-XIV",
            status="accepted",
            course=Mock(),
        )
        participant.name = "ZK Student"
        participant.course.name = "ZK Cohort XIV"

        activation_url = create_portal_onboarding_invite(participant)

        self.assertIsNone(activation_url)
        mock_post.assert_not_called()

    @patch("apps.cohort.helpers.portal.requests.post")
    @override_settings(
        PORTAL_ONBOARDING_URL="http://localhost:8000/api/v1/onboarding/invite",
        PORTAL_INTERNAL_API_KEY="secret-key",
        PORTAL_REQUEST_TIMEOUT=5,
    )
    def test_create_portal_onboarding_invite_returns_none_on_request_failure(
        self, mock_post
    ):
        mock_post.side_effect = requests.RequestException("network failure")

        participant = Mock(
            id=44,
            email="student@example.com",
            cohort="Cohort-XIV",
            status="accepted",
            course=Mock(),
        )
        participant.name = "Student Example"
        participant.course.name = "Web3 Cohort XIV"

        activation_url = create_portal_onboarding_invite(participant)

        self.assertIsNone(activation_url)

    @patch("apps.cohort.helpers.portal.send_mail")
    @patch("apps.cohort.helpers.portal.requests.post")
    @override_settings(
        PORTAL_ONBOARDING_URL="http://localhost:8000/api/v1/onboarding/invite",
        PORTAL_INTERNAL_API_KEY="secret-key",
        PORTAL_REQUEST_TIMEOUT=5,
        OPERATIONS_ALERT_EMAILS=["ops@example.com"],
        DEFAULT_FROM_EMAIL="noreply@example.com",
    )
    def test_create_portal_onboarding_invite_emails_ops_on_final_failure(
        self, mock_post, mock_send_mail
    ):
        mock_post.side_effect = requests.RequestException("network failure")

        participant = Mock(
            id=44,
            email="student@example.com",
            cohort="Cohort-XIV",
            status="accepted",
            course=Mock(),
        )
        participant.name = "Student Example"
        participant.course.name = "Web3 Cohort XIV"

        activation_url = create_portal_onboarding_invite(participant)

        self.assertIsNone(activation_url)
        mock_send_mail.assert_called_once()
        kwargs = mock_send_mail.call_args[1]
        self.assertEqual(kwargs["recipient_list"], ["ops@example.com"])
        self.assertIn("Participant ID: 44", kwargs["message"])

    @patch("apps.cohort.helpers.portal.requests.post")
    @override_settings(
        PORTAL_ONBOARDING_URL="http://localhost:8000/api/v1/onboarding/invite",
        PORTAL_INTERNAL_API_KEY="secret-key",
        PORTAL_REQUEST_TIMEOUT=5,
        PORTAL_REQUEST_MAX_RETRIES=2,
        PORTAL_REQUEST_RETRY_BACKOFF_SECONDS=0,
        PORTAL_REQUEST_RETRY_STATUS_CODES=(503,),
    )
    def test_create_portal_onboarding_invite_retries_retryable_http_error(self, mock_post):
        retryable_response = Mock(status_code=503)
        retryable_error = requests.HTTPError(response=retryable_response)

        success_response = Mock()
        success_response.raise_for_status.return_value = None
        success_response.json.return_value = {
            "activation_url": "https://portal.example.com/activate?token=retry-success"
        }

        first_response = Mock()
        first_response.raise_for_status.side_effect = retryable_error

        mock_post.side_effect = [first_response, success_response]

        participant = Mock(
            id=46,
            email="student@example.com",
            cohort="Cohort-XIV",
            status="accepted",
            course=Mock(),
        )
        participant.name = "Student Example"
        participant.course.name = "Web3 Cohort XIV"

        activation_url = create_portal_onboarding_invite(participant)

        self.assertEqual(
            activation_url,
            "https://portal.example.com/activate?token=retry-success",
        )
        self.assertEqual(mock_post.call_count, 2)

    @patch("apps.cohort.helpers.portal.requests.post")
    @override_settings(
        PORTAL_ONBOARDING_URL="http://localhost:8000/api/v1/onboarding/invite",
        PORTAL_INTERNAL_API_KEY="secret-key",
        PORTAL_REQUEST_TIMEOUT=5,
        PORTAL_REQUEST_MAX_RETRIES=3,
        PORTAL_REQUEST_RETRY_BACKOFF_SECONDS=0,
        PORTAL_REQUEST_RETRY_STATUS_CODES=(503,),
    )
    def test_create_portal_onboarding_invite_does_not_retry_non_retryable_http_error(
        self, mock_post
    ):
        non_retryable_response = Mock(status_code=400)
        non_retryable_error = requests.HTTPError(response=non_retryable_response)

        failed_response = Mock()
        failed_response.raise_for_status.side_effect = non_retryable_error
        mock_post.return_value = failed_response

        participant = Mock(
            id=47,
            email="student@example.com",
            cohort="Cohort-XIV",
            status="accepted",
            course=Mock(),
        )
        participant.name = "Student Example"
        participant.course.name = "Web3 Cohort XIV"

        activation_url = create_portal_onboarding_invite(participant)

        self.assertIsNone(activation_url)
        self.assertEqual(mock_post.call_count, 1)


@override_settings(SECURE_SSL_REDIRECT=False)
class RescheduleAssessmentEndpointTests(TestCase):
    """
    Tests for POST /api/v2/cohort/participant/reschedule/
    Resolves the latest Participant row for the email (by created_at).
    Email sending is mocked so no real SMTP calls are made.
    """

    ENDPOINT = "/api/v2/cohort/participant/reschedule/"

    VALID_PAYLOAD = {
        "email": "student@example.com",
        "name": "John Doe",
        "cohort": "Web3 Cohort XIV",
        "assessment_link": "https://calendly.com/web3bridge/assessment",
    }

    def setUp(self):
        self.client = APIClient()
        from cohort.models import Registration, Course, Participant

        self.registration = Registration.objects.create(
            name="Web3 Cohort XIV", cohort="Cohort-XIV", is_open=True
        )
        self.course = Course.objects.create(
            name="Web3 Development",
            description="Learn Web3",
            extra_info="Extra",
            registration=self.registration,
        )
        self.participant = Participant.objects.create(
            name="John Doe",
            email="student@example.com",
            wallet_address="0x123",
            registration=self.registration,
            course=self.course,
            cohort="Web3 Cohort XIV",
            venue="online",
        )
        self.other_participant = Participant.objects.create(
            name="Jane Roe",
            email="other@example.com",
            wallet_address="0x456",
            registration=self.registration,
            course=self.course,
            cohort="Web3 Cohort XIV",
            venue="online",
        )

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_valid_request_returns_200_and_sends_email(self, mock_send):
        response = self.client.post(self.ENDPOINT, self.VALID_PAYLOAD, format="json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once_with(
            "student@example.com",
            "John Doe",
            "Web3 Cohort XIV",
            "https://calendly.com/web3bridge/assessment",
        )

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_response_contains_success_message(self, mock_send):
        response = self.client.post(self.ENDPOINT, self.VALID_PAYLOAD, format="json")

        self.assertIn("email sent", response.json()["data"]["message"].lower())

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_missing_email_returns_400(self, mock_send):
        payload = {**self.VALID_PAYLOAD}
        payload.pop("email")
        response = self.client.post(self.ENDPOINT, payload, format="json")

        self.assertEqual(response.status_code, 400)
        mock_send.assert_not_called()

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_missing_name_returns_400(self, mock_send):
        payload = {**self.VALID_PAYLOAD}
        payload.pop("name")
        response = self.client.post(self.ENDPOINT, payload, format="json")

        self.assertEqual(response.status_code, 400)
        mock_send.assert_not_called()

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_cohort_field_optional_latest_participant_used(self, mock_send):
        payload = {**self.VALID_PAYLOAD}
        payload.pop("cohort")
        response = self.client.post(self.ENDPOINT, payload, format="json")

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once_with(
            "student@example.com",
            "John Doe",
            "Web3 Cohort XIV",
            "https://calendly.com/web3bridge/assessment",
        )

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_missing_assessment_link_returns_400(self, mock_send):
        payload = {**self.VALID_PAYLOAD}
        payload.pop("assessment_link")
        response = self.client.post(self.ENDPOINT, payload, format="json")

        self.assertEqual(response.status_code, 400)
        mock_send.assert_not_called()

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_invalid_email_returns_400(self, mock_send):
        payload = {**self.VALID_PAYLOAD, "email": "not-an-email"}
        response = self.client.post(self.ENDPOINT, payload, format="json")

        self.assertEqual(response.status_code, 400)
        mock_send.assert_not_called()

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_invalid_assessment_link_returns_400(self, mock_send):
        payload = {**self.VALID_PAYLOAD, "assessment_link": "not-a-url"}
        response = self.client.post(self.ENDPOINT, payload, format="json")

        self.assertEqual(response.status_code, 400)
        mock_send.assert_not_called()

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_second_reschedule_is_blocked(self, mock_send):
        # First reschedule — should succeed
        self.client.post(self.ENDPOINT, self.VALID_PAYLOAD, format="json")

        # Second reschedule with same email — should be blocked
        response = self.client.post(self.ENDPOINT, self.VALID_PAYLOAD, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("already rescheduled", response.json()["message"].lower())
        # Email sent only once (first request)
        mock_send.assert_called_once()

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_different_email_can_still_reschedule(self, mock_send):
        # First participant reschedules
        self.client.post(self.ENDPOINT, self.VALID_PAYLOAD, format="json")

        # Different participant — should be allowed
        different_payload = {
            **self.VALID_PAYLOAD,
            "email": "other@example.com",
            "name": "Jane Roe",
        }
        response = self.client.post(self.ENDPOINT, different_payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_send.call_count, 2)

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_reschedule_without_matching_participant_returns_404(self, mock_send):
        payload = {
            **self.VALID_PAYLOAD,
            "email": "unknown@example.com",
        }
        response = self.client.post(self.ENDPOINT, payload, format="json")
        self.assertEqual(response.status_code, 404)
        mock_send.assert_not_called()

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_reschedule_allowed_again_after_delete_and_re_register(self, mock_send):
        """Deleting a participant clears CASCADE reschedule; same email can reschedule on new row."""
        from cohort.models import AssessmentReschedule, Participant

        self.client.post(self.ENDPOINT, self.VALID_PAYLOAD, format="json")
        self.assertTrue(
            AssessmentReschedule.objects.filter(participant=self.participant).exists()
        )

        self.participant.delete()

        Participant.objects.create(
            name="John Doe",
            email="student@example.com",
            wallet_address="0x999",
            registration=self.registration,
            course=self.course,
            cohort="Web3 Cohort XIV",
            venue="online",
        )

        response = self.client.post(self.ENDPOINT, self.VALID_PAYLOAD, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_send.call_count, 2)

    @patch("cohort.views.send_reschedule_assessment_email")
    def test_latest_participant_wins_when_same_email_two_registrations(self, mock_send):
        """Stale cohort in payload must not bind to an older row; latest created_at wins."""
        from cohort.models import AssessmentReschedule, Course, Participant, Registration

        reg_old = Registration.objects.create(
            name="Old Cohort", cohort="Cohort-XIII", is_open=True
        )
        course_old = Course.objects.create(
            name="Old Course",
            description="Old",
            extra_info="Extra",
            registration=reg_old,
        )
        Participant.objects.create(
            name="John Doe",
            email="student@example.com",
            wallet_address="0xold",
            registration=reg_old,
            course=course_old,
            cohort="Old Cohort Label",
            venue="online",
        )

        reg_new = Registration.objects.create(
            name="Web3 Cohort XV", cohort="Cohort-XV", is_open=True
        )
        course_new = Course.objects.create(
            name="Solidity",
            description="S",
            extra_info="Extra",
            registration=reg_new,
        )
        newer = Participant.objects.create(
            name="John Doe",
            email="student@example.com",
            wallet_address="0xnew",
            registration=reg_new,
            course=course_new,
            cohort="Web3 Cohort XV",
            venue="online",
        )

        payload = {
            **self.VALID_PAYLOAD,
            "cohort": "Old Cohort Label",
        }
        response = self.client.post(self.ENDPOINT, payload, format="json")
        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once_with(
            "student@example.com",
            "John Doe",
            "Web3 Cohort XV",
            "https://calendly.com/web3bridge/assessment",
        )
        self.assertTrue(
            AssessmentReschedule.objects.filter(participant=newer).exists()
        )


class RescheduleAssessmentTemplateTests(SimpleTestCase):
    """Verify the email template renders all key content correctly."""

    TEMPLATE = "cohort/reschedule_assessment_email.html"

    def test_template_renders_student_name(self):
        rendered = render_to_string(self.TEMPLATE, {
            "name": "John Doe",
            "cohort": "Web3 Cohort XIV",
            "assessment_link": "https://calendly.com/web3bridge/assessment",
        })
        self.assertIn("John Doe", rendered)

    def test_template_renders_cohort(self):
        rendered = render_to_string(self.TEMPLATE, {
            "name": "John Doe",
            "cohort": "Web3 Cohort XIV",
            "assessment_link": "https://calendly.com/web3bridge/assessment",
        })
        self.assertIn("Web3 Cohort XIV", rendered)

    def test_template_renders_assessment_link(self):
        link = "https://calendly.com/web3bridge/assessment"
        rendered = render_to_string(self.TEMPLATE, {
            "name": "John Doe",
            "cohort": "Web3 Cohort XIV",
            "assessment_link": link,
        })
        self.assertIn(link, rendered)

    def test_template_mentions_3_days(self):
        rendered = render_to_string(self.TEMPLATE, {
            "name": "John Doe",
            "cohort": "Web3 Cohort XIV",
            "assessment_link": "https://calendly.com/web3bridge/assessment",
        })
        self.assertIn("3 days", rendered)


@override_settings(SECURE_SSL_REDIRECT=False)
class SubmitAssessmentEndpointTests(TestCase):
    """Tests for POST /api/v2/cohort/participant/submit-assessment/"""

    ENDPOINT = "/api/v2/cohort/participant/submit-assessment/"
    API_KEY = "EY63JDFEE9GKNJDBDJ"

    def setUp(self):
        self.client = APIClient()
        # Create prerequisite objects
        from cohort.models import Registration, Course, Participant
        self.registration = Registration.objects.create(
            name="Web3 Cohort XIV", cohort="Cohort-XIV", is_open=True
        )
        self.course = Course.objects.create(
            name="Web3 Development",
            description="Learn Web3",
            extra_info="Extra",
            registration=self.registration,
        )
        self.participant = Participant.objects.create(
            name="John Doe",
            email="john@example.com",
            wallet_address="0x123",
            registration=self.registration,
            course=self.course,
            cohort="Cohort-XIV",
            venue="online",
        )

    def _post(self, payload, api_key=None):
        key = api_key if api_key is not None else self.API_KEY
        return self.client.post(
            self.ENDPOINT, payload, format="json", headers={"API-Key": key}
        )

    def _post_no_key(self, payload):
        return self.client.post(self.ENDPOINT, payload, format="json")

    @patch("cohort.views.send_assessment_passed_email")
    def test_pass_creates_assessment_and_sends_passed_email(self, mock_passed):
        payload = {"email": "john@example.com", "score": "85.50", "passed": True}
        response = self._post(payload)

        self.assertEqual(response.status_code, 201)
        from cohort.models import Assessment
        self.assertTrue(Assessment.objects.filter(participant=self.participant, passed=True).exists())
        mock_passed.assert_called_once()

    @patch("cohort.views.send_assessment_passed_email")
    def test_breakdown_persisted_and_passed_to_email(self, mock_passed):
        breakdown = {"logic": 40, "solidity": 45}
        payload = {
            "email": "john@example.com",
            "score": "85.50",
            "passed": True,
            "breakdown": breakdown,
        }
        response = self._post(payload)

        self.assertEqual(response.status_code, 201)
        from cohort.models import Assessment
        a = Assessment.objects.get(participant=self.participant)
        self.assertEqual(a.breakdown, breakdown)
        mock_passed.assert_called_once()
        self.assertEqual(mock_passed.call_args.kwargs.get("breakdown"), breakdown)

    @patch("cohort.views.send_assessment_failed_email")
    def test_fail_creates_assessment_and_sends_failed_email(self, mock_failed):
        payload = {"email": "john@example.com", "score": "40.00", "passed": False}
        response = self._post(payload)

        self.assertEqual(response.status_code, 201)
        from cohort.models import Assessment
        self.assertTrue(Assessment.objects.filter(participant=self.participant, passed=False).exists())
        mock_failed.assert_called_once()

    @patch("cohort.views.send_assessment_passed_email")
    def test_duplicate_assessment_same_cohort_is_blocked(self, mock_passed):
        payload = {"email": "john@example.com", "score": "85.50", "passed": True}
        self._post(payload)
        response = self._post(payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("already submitted", response.json()["message"].lower())

    @patch("cohort.views.send_assessment_passed_email")
    def test_missing_api_key_returns_401(self, mock_passed):
        payload = {"email": "john@example.com", "score": "85.50", "passed": True}
        response = self._post_no_key(payload)

        self.assertEqual(response.status_code, 401)
        mock_passed.assert_not_called()

    @patch("cohort.views.send_assessment_passed_email")
    def test_wrong_api_key_returns_401(self, mock_passed):
        payload = {"email": "john@example.com", "score": "85.50", "passed": True}
        response = self._post(payload, api_key="wrong-key")

        self.assertEqual(response.status_code, 401)
        mock_passed.assert_not_called()

    @patch("cohort.views.send_assessment_passed_email")
    def test_unknown_email_returns_404(self, mock_passed):
        payload = {"email": "nobody@example.com", "score": "85.50", "passed": True}
        response = self._post(payload)

        self.assertEqual(response.status_code, 404)
        mock_passed.assert_not_called()

    @patch("cohort.views.send_assessment_passed_email")
    def test_invalid_score_returns_400(self, mock_passed):
        payload = {"email": "john@example.com", "score": "not-a-number", "passed": True}
        response = self._post(payload)

        self.assertEqual(response.status_code, 400)
        mock_passed.assert_not_called()

    @patch("cohort.views.send_assessment_passed_email")
    def test_participant_id_email_mismatch_returns_400(self, mock_passed):
        payload = {
            "email": "wrong@example.com",
            "participant_id": self.participant.id,
            "score": "85.50",
            "passed": True,
        }
        response = self._post(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("mismatch", response.json()["message"].lower())
        mock_passed.assert_not_called()

    @patch("cohort.views.send_assessment_passed_email")
    def test_participant_id_targets_specific_row_when_email_duplicated(self, mock_passed):
        """Same email on two registrations: optional participant_id picks the row explicitly."""
        from cohort.models import Assessment, Course, Participant, Registration

        reg2 = Registration.objects.create(
            name="ZK Cohort XV", cohort="Cohort-XV", is_open=True
        )
        course2 = Course.objects.create(
            name="ZK Track",
            description="ZK",
            extra_info="Extra",
            registration=reg2,
        )
        newer = Participant.objects.create(
            name="John Doe",
            email="john@example.com",
            wallet_address="0xbbb",
            registration=reg2,
            course=course2,
            cohort="Cohort-XV",
            venue="online",
        )

        # No participant_id: latest by created_at is `newer`
        r1 = self._post(
            {"email": "john@example.com", "score": "90.00", "passed": True}
        )
        self.assertEqual(r1.status_code, 201)
        self.assertTrue(Assessment.objects.filter(participant=newer).exists())

        # Explicit older participant (self.participant)
        r2 = self._post(
            {
                "email": "john@example.com",
                "participant_id": self.participant.id,
                "score": "55.00",
                "passed": True,
            }
        )
        self.assertEqual(r2.status_code, 201)
        a_old = Assessment.objects.get(participant=self.participant)
        self.assertEqual(str(a_old.score), "55.00")


class PaymentActivationEmailTests(SimpleTestCase):
    """
    ``send_registration_success_mail`` may include an activation URL when passed explicitly.
    ``handle_payment_success`` sends only one mail, with no portal activation URL.
    """

    @patch("cohort.helpers.model.base.render_to_string")
    @patch("cohort.helpers.model.base.EmailMessage")
    def test_activation_url_passed_to_email_for_web3_course(
        self, mock_email_cls, mock_render
    ):
        mock_render.return_value = "<html></html>"
        mock_email_cls.return_value = MagicMock()

        with patch("cohort.models.Course") as mock_course_cls:
            mock_course = MagicMock()
            mock_course.name = "Web3 Development"
            mock_course_cls.objects.get.return_value = mock_course

            from cohort.helpers.model.base import send_registration_success_mail
            send_registration_success_mail(
                "student@example.com", 1, "John Doe",
                activation_url="https://portal.web3bridge.com/activate/onboard?token=abc"
            )

        call_kwargs = mock_render.call_args
        self.assertEqual(call_kwargs[0][0], "cohort/web3_registration_email.html")
        context = call_kwargs[0][1]
        self.assertEqual(
            context.get("activation_url"),
            "https://portal.web3bridge.com/activate/onboard?token=abc",
        )
        self.assertEqual(context.get("name"), "John Doe")

    @patch("cohort.helpers.model.base.render_to_string")
    @patch("cohort.helpers.model.base.EmailMessage")
    def test_activation_url_is_none_for_zk_course(self, mock_email_cls, mock_render):
        mock_render.return_value = "<html></html>"
        mock_email_cls.return_value = MagicMock()

        with patch("cohort.models.Course") as mock_course_cls:
            mock_course = MagicMock()
            mock_course.name = "ZK Cohort XIV"
            mock_course_cls.objects.get.return_value = mock_course

            from cohort.helpers.model.base import send_registration_success_mail
            send_registration_success_mail(
                "zk@example.com", 1, "ZK Student",
                activation_url="https://portal.web3bridge.com/activate/onboard?token=zk"
            )

        call_kwargs = mock_render.call_args
        self.assertEqual(call_kwargs[0][0], "cohort/zk_registration_email.html")
        context = call_kwargs[0][1]
        self.assertIsNone(context.get("activation_url"))
        self.assertEqual(context.get("name"), "ZK Student")

    @patch("cohort.views.send_registration_success_mail")
    def test_handle_payment_success_sends_one_mail_without_portal_activation(
        self, mock_mail
    ):
        from cohort.views import handle_payment_success

        participant = MagicMock()
        participant.course_id = 1
        serialized = {
            "email": "student@example.com",
            "name": "John Doe",
            "course": {"id": 1},
        }
        serializer_class = MagicMock()

        handle_payment_success(participant, serialized, serializer_class)

        mock_mail.assert_called_once_with(
            "student@example.com",
            1,
            "John Doe",
            activation_url=None,
        )


class SubmitAssessmentTemplateTests(SimpleTestCase):
    """Verify pass/fail email templates render correctly."""

    def test_passed_template_renders_welcome_and_links(self):
        rendered = render_to_string("cohort/assessment_passed_email.html", {
            "name": "John Doe",
        })
        self.assertIn("Welcome to Web3Bridge", rendered)
        self.assertIn("successfully passed the assessment", rendered.lower())
        self.assertIn("student portal", rendered.lower())
        self.assertIn("https://t.me/web3bridge", rendered)

    def test_passed_template_renders_without_cohort(self):
        rendered = render_to_string("cohort/assessment_passed_email.html", {
            "name": "John Doe",
        })
        self.assertIn("successfully passed the assessment", rendered.lower())

    def test_failed_template_renders_name_score_and_encouragement(self):
        rendered = render_to_string("cohort/assessment_failed_email.html", {
            "name": "John Doe",
            "cohort": "Web3 Cohort XIV",
            "score": "40.00",
            "breakdown_display": None,
        })
        self.assertIn("John Doe", rendered)
        self.assertIn("40.00", rendered)
        self.assertIn("next cohort", rendered.lower())

    def test_failed_template_renders_breakdown_when_present(self):
        rendered = render_to_string("cohort/assessment_failed_email.html", {
            "name": "John Doe",
            "cohort": "Web3 Cohort XIV",
            "score": "40.00",
            "breakdown_display": "Section A: 10 / 30",
        })
        self.assertIn("Score breakdown", rendered)
        self.assertIn("Section A: 10 / 30", rendered)

    def test_assessment_breakdown_suppresses_metadata_only_dict(self):
        from cohort.helpers.model.base import _format_assessment_breakdown

        self.assertIsNone(
            _format_assessment_breakdown(
                {"email": "a@b.com", "score": 29.5, "passed": False}
            )
        )

    def test_assessment_breakdown_formats_real_sections(self):
        from cohort.helpers.model.base import _format_assessment_breakdown

        out = _format_assessment_breakdown({"logic": 40, "solidity": 45})
        self.assertIn("Logic:", out)
        self.assertIn("Solidity:", out)
