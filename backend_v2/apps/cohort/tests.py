from unittest.mock import MagicMock, Mock, patch

import requests
from django.db import IntegrityError
from django.test import SimpleTestCase, TestCase, override_settings
from django.template.loader import render_to_string
from django.utils import timezone
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

    def test_verify_payment_serializer_merges_program_into_registration_id(self):
        from cohort.serializers import VerifyPaymentByEmailSerializer

        s = VerifyPaymentByEmailSerializer(
            data={"email": "user@example.com", "program": 12, "course": 3}
        )
        self.assertTrue(s.is_valid(), s.errors)
        self.assertEqual(s.validated_data["registration_id"], 12)

    def test_verify_payment_serializer_rejects_conflicting_program(self):
        from cohort.serializers import VerifyPaymentByEmailSerializer

        s = VerifyPaymentByEmailSerializer(
            data={
                "email": "user@example.com",
                "registrationId": 1,
                "program": 2,
                "course": 3,
            }
        )
        self.assertFalse(s.is_valid())


@override_settings(
    SECURE_SSL_REDIRECT=False,
    PORTAL_ONBOARDING_URL="",
    PORTAL_INTERNAL_API_KEY="",
)
class ParticipantCreateRegistrationPersistenceTests(TestCase):
    """
    Participant.registration follows the course’s linked programme (Course.registration),
    not an arbitrary id from the client.
    """

    CREATE_URL = "/api/v2/cohort/participant/"

    def setUp(self):
        self.client = APIClient()
        from cohort.models import Course, Registration

        self.reg = Registration.objects.create(
            name="Open intake",
            cohort="Cohort-TEST",
            is_open=True,
        )
        self.other_reg = Registration.objects.create(
            name="Other programme",
            cohort="OTHER",
            is_open=True,
        )
        self.course_unlinked = Course.objects.create(
            name="Course without programme FK",
            description="d",
            extra_info="e",
        )
        self.assertIsNone(self.course_unlinked.registration_id)
        self.course_linked = Course.objects.create(
            name="Course with programme FK",
            description="d",
            extra_info="e",
            registration=self.reg,
        )

    def _base_payload(self, **overrides):
        payload = {
            "name": "Test User",
            "wallet_address": "0x1234567890123456789012345678901234567890",
            "email": "participant_create@example.com",
            "course": self.course_linked.pk,
            "registration": self.reg.pk,
            "city": "Lagos",
            "country": "NG",
            "gender": "male",
            "venue": "online",
        }
        payload.update(overrides)
        return payload

    def test_create_uses_course_programme_not_client_registration_id(self):
        from cohort.models import Participant

        r = self.client.post(
            self.CREATE_URL,
            self._base_payload(
                email="uses_course_prog@example.com",
                registration=self.other_reg.pk,
            ),
            format="json",
        )
        self.assertEqual(r.status_code, 201, r.content)
        p = Participant.objects.get(email="uses_course_prog@example.com")
        self.assertEqual(p.registration_id, self.reg.pk)
        self.assertEqual(p.cohort, self.reg.cohort)

    def test_create_uses_active_cohort_and_normalizes_roman_token(self):
        from cohort.models import Course, Participant, Registration

        stale_reg = Registration.objects.create(
            name="Web3 Cohort XIV",
            cohort="xiv",
            is_open=True,
        )
        Registration.objects.create(
            name="Web3 Cohort XV",
            cohort="xv",
            is_open=True,
        )
        stale_course = Course.objects.create(
            name="Solidity (Web3 Development)",
            description="d",
            extra_info="e",
            registration=stale_reg,
        )
        r = self.client.post(
            self.CREATE_URL,
            self._base_payload(
                email="active_cohort@example.com",
                course=stale_course.pk,
                registration=stale_reg.pk,
            ),
            format="json",
        )
        self.assertEqual(r.status_code, 201, r.content)

        p = Participant.objects.get(email="active_cohort@example.com")
        self.assertEqual(p.registration_id, stale_reg.pk)
        self.assertEqual(p.cohort, "Cohort XV")

    def test_create_resolves_open_registration_when_omitted(self):
        from cohort.models import Participant

        r = self.client.post(
            self.CREATE_URL,
            self._base_payload(
                email="resolved_reg@example.com",
                course=self.course_linked.pk,
                registration=None,
            ),
            format="json",
        )
        self.assertEqual(r.status_code, 201, r.content)
        p = Participant.objects.get(email="resolved_reg@example.com")
        self.assertEqual(p.registration_id, self.reg.pk)

    def test_create_empty_string_registration_same_as_omitted(self):
        from cohort.models import Participant

        r = self.client.post(
            self.CREATE_URL,
            self._base_payload(
                email="empty_str_reg@example.com",
                registration="",
            ),
            format="json",
        )
        self.assertEqual(r.status_code, 201, r.content)
        p = Participant.objects.get(email="empty_str_reg@example.com")
        self.assertEqual(p.registration_id, self.reg.pk)

    def test_create_whitespace_registration_same_as_omitted(self):
        from cohort.models import Participant

        r = self.client.post(
            self.CREATE_URL,
            self._base_payload(
                email="ws_reg@example.com",
                registration="   \t  ",
            ),
            format="json",
        )
        self.assertEqual(r.status_code, 201, r.content)
        p = Participant.objects.get(email="ws_reg@example.com")
        self.assertEqual(p.registration_id, self.reg.pk)

    def test_create_returns_400_when_no_registration_and_course_unlinked(self):
        r = self.client.post(
            self.CREATE_URL,
            self._base_payload(
                email="no_reg@example.com",
                registration=None,
            ),
            format="json",
        )
        self.assertEqual(r.status_code, 400)

    def test_create_rejects_closed_registration(self):
        from cohort.models import Course, Registration

        closed = Registration.objects.create(
            name="Closed intake",
            cohort="Cohort-CLOSED",
            is_open=False,
        )
        course_closed = Course.objects.create(
            name="Linked to closed programme",
            description="d",
            extra_info="e",
            registration=closed,
        )
        r = self.client.post(
            self.CREATE_URL,
            self._base_payload(
                email="closed_prog@example.com",
                course=course_closed.pk,
                registration=None,
            ),
            format="json",
        )
        self.assertEqual(r.status_code, 400)


class ParticipantSaveFillsRegistrationFromCourseTests(TestCase):
    """Model save() must copy course.registration_id when participant FK is unset."""

    def test_save_sets_registration_id_from_course(self):
        from cohort.models import Course, Participant, Registration

        reg = Registration.objects.create(
            name="Prog", cohort="WEB3", is_open=True
        )
        course = Course.objects.create(
            name="C1",
            description="d",
            extra_info="e",
            registration=reg,
        )
        p = Participant.objects.create(
            name="N",
            email="save_fill@example.com",
            wallet_address="0x1",
            course=course,
            venue="online",
        )
        self.assertEqual(p.registration_id, reg.pk)


@override_settings(
    SECURE_SSL_REDIRECT=False,
    PORTAL_ONBOARDING_URL="",
    PORTAL_INTERNAL_API_KEY="",
)
class ParticipantReadAutoCorrectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        from cohort.models import Course, Participant, Registration

        self.reg = Registration.objects.create(
            name="Web3 Cohort XV", cohort="Cohort-XV", is_open=True
        )
        self.course = Course.objects.create(
            name="Solidity",
            description="d",
            extra_info="e",
            registration=self.reg,
        )
        self.participant = Participant.objects.create(
            name="Legacy User",
            email="legacy.fix@example.com",
            wallet_address="0x1111111111111111111111111111111111111111",
            course=self.course,
            registration=None,
            cohort=None,
            venue="online",
        )

    def test_retrieve_autofills_registration_and_cohort(self):
        url = f"/api/v2/cohort/participant/{self.participant.pk}/"
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200, r.content)

        self.participant.refresh_from_db()
        self.assertEqual(self.participant.registration_id, self.reg.pk)
        self.assertEqual(self.participant.cohort, self.reg.cohort)


class CourseListRegistrationSerializationTests(TestCase):
    def test_course_list_includes_registration_pk_when_programme_closed(self):
        from cohort.models import Course, Registration
        from cohort.serializers import CourseSerializer

        closed = Registration.objects.create(
            name="Past", cohort="Cohort-PAST", is_open=False
        )
        course = Course.objects.create(
            name="With closed programme",
            description="d",
            extra_info="e",
            registration=closed,
        )
        data = CourseSerializer.List(course).data
        self.assertEqual(data["registration"], closed.pk)


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

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    def test_verify_payment_returns_404_when_registration_mismatches_course(self):
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()

        response = self._verify_post(
            {
                "email": "dup@example.com",
                "course": self.course_old.id,
                "registrationId": self.reg_new.id,
            }
        )

        self.assertEqual(response.status_code, 404)

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_accepts_matching_registration_id(self, mock_handle):
        mock_handle.side_effect = (
            lambda participant, serialized, serializer_class: serializer_class.Retrieve(
                participant
            ).data
        )
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()

        response = self._verify_post(
            {
                "email": "dup@example.com",
                "course": self.course_old.id,
                "registrationId": self.reg_old.id,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.participant_unpaid.refresh_from_db()
        self.assertTrue(self.participant_unpaid.payment_status)
        mock_handle.assert_called_once()

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_registration_id_retry_does_not_mark_other_rows(self, mock_handle):
        """
        Retries with the same registration-only payload must stay on one row and not
        progressively mark other unpaid rows in that registration as paid.
        """
        from cohort.models import Course, Participant

        mock_handle.side_effect = (
            lambda participant, serialized, serializer_class: serializer_class.Retrieve(
                participant
            ).data
        )

        second_course_same_registration = Course.objects.create(
            name="Web3 Cohort XIV - Track 2",
            description="Desc",
            extra_info="Extra",
            registration=self.reg_old,
        )
        second_row_same_registration = Participant.objects.create(
            name="Jane",
            email="dup@example.com",
            wallet_address="0xbbb",
            registration=self.reg_old,
            course=second_course_same_registration,
            cohort="Cohort-XIV",
            venue="online",
            payment_status=False,
        )
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()

        payload = {
            "email": "dup@example.com",
            "registrationId": self.reg_old.id,
        }
        first_response = self._verify_post(payload)
        second_response = self._verify_post(payload)

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        self.participant_unpaid.refresh_from_db()
        second_row_same_registration.refresh_from_db()

        # Latest row in the registration is selected consistently across retries.
        self.assertFalse(self.participant_unpaid.payment_status)
        self.assertTrue(second_row_same_registration.payment_status)
        self.assertEqual(mock_handle.call_count, 1)

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_email_only_ignores_unpaid_on_closed_registration(
        self, mock_handle
    ):
        """Payment portal must not resolve to unpaid rows for intakes that are no longer open."""
        mock_handle.side_effect = (
            lambda participant, serialized, serializer_class: serializer_class.Retrieve(
                participant
            ).data
        )
        self.reg_old.is_open = False
        self.reg_old.save()
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()

        response = self._verify_post({"email": "dup@example.com"})

        self.assertEqual(response.status_code, 200)
        self.participant_unpaid.refresh_from_db()
        self.assertFalse(self.participant_unpaid.payment_status)
        self.participant_paid_newer.refresh_from_db()
        self.assertTrue(self.participant_paid_newer.payment_status)
        mock_handle.assert_not_called()

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_email_only_prefers_open_unpaid_over_closed_unpaid(
        self, mock_handle
    ):
        mock_handle.side_effect = (
            lambda participant, serialized, serializer_class: serializer_class.Retrieve(
                participant
            ).data
        )
        self.reg_old.is_open = False
        self.reg_old.save()
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()
        self.participant_paid_newer.payment_status = False
        self.participant_paid_newer.save()

        response = self._verify_post({"email": "dup@example.com"})

        self.assertEqual(response.status_code, 200)
        self.participant_unpaid.refresh_from_db()
        self.assertFalse(self.participant_unpaid.payment_status)
        self.participant_paid_newer.refresh_from_db()
        self.assertTrue(self.participant_paid_newer.payment_status)
        mock_handle.assert_called_once()

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_with_participant_id_still_marks_closed_registration_row(
        self, mock_handle
    ):
        """Explicit participantId must still resolve when the programme is closed."""
        mock_handle.side_effect = (
            lambda participant, serialized, serializer_class: serializer_class.Retrieve(
                participant
            ).data
        )
        self.reg_old.is_open = False
        self.reg_old.save()
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()

        response = self._verify_post(
            {
                "email": "dup@example.com",
                "participantId": self.participant_unpaid.id,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.participant_unpaid.refresh_from_db()
        self.assertTrue(self.participant_unpaid.payment_status)
        mock_handle.assert_called_once()

    @patch.object(cohort_views, "API_KEY", "test-verify-payment-key")
    @patch("cohort.views.handle_payment_success")
    def test_verify_payment_autocorrects_null_registration_from_course(
        self, mock_handle
    ):
        mock_handle.side_effect = (
            lambda participant, serialized, serializer_class: serializer_class.Retrieve(
                participant
            ).data
        )
        self.participant_unpaid.registration = None
        self.participant_unpaid.cohort = None
        self.participant_unpaid.payment_status = False
        self.participant_unpaid.save()

        response = self._verify_post(
            {
                "email": "dup@example.com",
                "course": self.course_old.id,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.participant_unpaid.refresh_from_db()
        self.assertEqual(self.participant_unpaid.registration_id, self.reg_old.id)
        self.assertEqual(self.participant_unpaid.cohort, self.reg_old.cohort)
        self.assertTrue(self.participant_unpaid.payment_status)
        mock_handle.assert_called_once()

    def test_same_email_same_cohort_across_registrations_not_allowed(self):
        """DB blocks duplicate rows per email+cohort even if registrations differ."""
        from cohort.models import Course, Participant, Registration

        reg_first = Registration.objects.create(
            name="Intake A", cohort="Cohort-TEST", is_open=True
        )
        reg_second = Registration.objects.create(
            name="Intake B", cohort="Cohort-TEST", is_open=True
        )
        c1 = Course.objects.create(
            name="Track A",
            description="d",
            extra_info="e",
            registration=reg_first,
        )
        c2 = Course.objects.create(
            name="Track B",
            description="d",
            extra_info="e",
            registration=reg_second,
        )
        Participant.objects.create(
            name="Multi",
            email="multi_course@example.com",
            wallet_address="0x111",
            registration=reg_first,
            course=c1,
            cohort=reg_first.cohort,
            venue="online",
            payment_status=False,
        )
        with self.assertRaises(IntegrityError):
            Participant.objects.create(
                name="Multi",
                email="multi_course@example.com",
                wallet_address="0x222",
                registration=reg_second,
                course=c2,
                cohort=reg_second.cohort,
                venue="online",
                payment_status=False,
            )


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

    def test_rust_template_does_not_render_portal_activation_link(self):
        rendered = render_to_string(
            "cohort/rust_registration_email.html",
            {
                "name": "Student Example",
                "activation_url": "https://portal.example.com/activate?token=abc",
            },
        )

        self.assertIn("Student Portal Access:", rendered)
        self.assertIn("will be sent within the next 14 days", rendered)
        self.assertNotIn("Activate your student portal account", rendered)

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


@override_settings(SECURE_SSL_REDIRECT=False)
class ReconcileAssessmentCutoffEndpointTests(TestCase):
    """Tests for POST /api/v2/cohort/participant/reconcile-assessment-cutoff/"""

    ENDPOINT = "/api/v2/cohort/participant/reconcile-assessment-cutoff/"
    API_KEY = "EY63JDFEE9GKNJDBDJ"

    def setUp(self):
        self.client = APIClient()
        from cohort.models import Assessment, Registration, Course, Participant

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
        self.assessment = Assessment.objects.create(
            participant=self.participant,
            score="45.00",
            passed=False,
            breakdown=None,
            date_taken=timezone.now(),
        )

    def _post(self, payload, api_key=None):
        key = api_key if api_key is not None else self.API_KEY
        return self.client.post(
            self.ENDPOINT, payload, format="json", headers={"API-Key": key}
        )

    @patch("cohort.views.send_assessment_cutoff_reconciliation_email")
    def test_reconciles_failed_assessment_and_sends_email(self, mock_send):
        payload = {"items": [{"email": "john@example.com"}]}
        response = self._post(payload)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["data"]["summary"]["reconciled"], 1)
        self.assertEqual(body["data"]["results"][0]["status"], "reconciled")
        self.assessment.refresh_from_db()
        self.assertTrue(self.assessment.passed)
        mock_send.assert_called_once()

    @patch("cohort.views.send_assessment_cutoff_reconciliation_email")
    def test_min_score_skips_when_below(self, mock_send):
        payload = {
            "items": [{"email": "john@example.com"}],
            "min_score": "60.00",
        }
        response = self._post(payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["summary"]["reconciled"], 0)
        self.assertIn("below min_score", response.json()["data"]["results"][0]["detail"])
        self.assessment.refresh_from_db()
        self.assertFalse(self.assessment.passed)
        mock_send.assert_not_called()

    @patch("cohort.views.send_assessment_cutoff_reconciliation_email")
    def test_already_passed_skipped(self, mock_send):
        self.assessment.passed = True
        self.assessment.save()
        response = self._post({"items": [{"email": "john@example.com"}]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["summary"]["reconciled"], 0)
        self.assertIn("already marked as passed", response.json()["data"]["results"][0]["detail"])
        mock_send.assert_not_called()

    @patch("cohort.views.send_assessment_cutoff_reconciliation_email")
    def test_missing_api_key_returns_401(self, mock_send):
        response = self.client.post(
            self.ENDPOINT,
            {"items": [{"email": "john@example.com"}]},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        mock_send.assert_not_called()

    def test_cutoff_reconciliation_template_renders(self):
        rendered = render_to_string(
            "cohort/assessment_cutoff_reconciliation_email.html",
            {
                "cohort": "Web3 Cohort XV",
                "payment_link": "https://payment.web3bridgeafrica.com",
                "qualifying_threshold_percent": 50,
            },
        )
        self.assertIn("downward review", rendered.lower())
        self.assertIn("50", rendered)
        self.assertIn("https://payment.web3bridgeafrica.com", rendered)
        self.assertIn("https://t.me/web3bridge", rendered)


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


class RegistrationWelcomeEmailRetryTests(SimpleTestCase):
    """Post-payment welcome mail retries SMTP failures and alerts operations."""

    @override_settings(
        OPERATIONS_ALERT_EMAILS=["ops@example.com"],
        REGISTRATION_WELCOME_EMAIL_MAX_RETRIES=3,
        REGISTRATION_WELCOME_EMAIL_RETRY_BACKOFF_SECONDS=0,
    )
    @patch("cohort.helpers.model.base.time.sleep")
    @patch("cohort.helpers.model.base.send_mail")
    @patch("cohort.helpers.model.base._build_registration_success_email_message")
    def test_retries_send_until_success(self, mock_build, mock_send_mail, _mock_sleep):
        mock_msg = MagicMock()
        mock_msg.send.side_effect = [ConnectionError("smtp down"), ConnectionError("again"), 1]
        mock_build.return_value = mock_msg

        from cohort.helpers.model.base import send_registration_success_mail

        send_registration_success_mail("stu@example.com", 5, "Sam", activation_url=None)

        self.assertEqual(mock_msg.send.call_count, 3)
        mock_send_mail.assert_not_called()

    @override_settings(
        OPERATIONS_ALERT_EMAILS=["ops@example.com"],
        REGISTRATION_WELCOME_EMAIL_MAX_RETRIES=2,
        REGISTRATION_WELCOME_EMAIL_RETRY_BACKOFF_SECONDS=0,
    )
    @patch("cohort.helpers.model.base.time.sleep")
    @patch("cohort.helpers.model.base.send_mail")
    @patch("cohort.helpers.model.base._build_registration_success_email_message")
    def test_alerts_ops_after_all_retries_fail(self, mock_build, mock_send_mail, _mock_sleep):
        mock_msg = MagicMock()
        mock_msg.send.side_effect = ConnectionError("smtp")
        mock_build.return_value = mock_msg

        from cohort.helpers.model.base import send_registration_success_mail

        send_registration_success_mail("stu@example.com", 5, "Sam", activation_url=None)

        self.assertEqual(mock_msg.send.call_count, 2)
        mock_send_mail.assert_called_once()
        kwargs = mock_send_mail.call_args[1]
        self.assertEqual(kwargs["recipient_list"], ["ops@example.com"])
        self.assertIn("Registration welcome email (post-payment) failed", kwargs["subject"])


class SubmitAssessmentTemplateTests(SimpleTestCase):
    """Verify pass/fail email templates render correctly."""

    def test_passed_template_renders_welcome_and_links(self):
        rendered = render_to_string("cohort/assessment_passed_email.html", {
            "name": "John Doe",
            "payment_link": "https://payment.web3bridgeafrica.com",
        })
        self.assertIn("Welcome to Web3Bridge", rendered)
        self.assertIn("successfully passed the assessment", rendered.lower())
        self.assertIn("student portal", rendered.lower())
        self.assertIn("14 days after payment confirmation", rendered.lower())
        self.assertIn("https://payment.web3bridgeafrica.com", rendered)
        self.assertIn("https://t.me/web3bridge", rendered)

    def test_passed_template_renders_without_cohort(self):
        rendered = render_to_string("cohort/assessment_passed_email.html", {
            "name": "John Doe",
            "payment_link": "https://payment.web3bridgeafrica.com",
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
