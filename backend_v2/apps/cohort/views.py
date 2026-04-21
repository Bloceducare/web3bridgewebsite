import json
import logging
import threading

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.forms import ValidationError
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, pagination, status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from . import models, serializers
from .helpers.model import (
    send_approval_email,
    send_assessment_failed_email,
    send_assessment_passed_email,
    send_registration_success_mail,
    send_reschedule_assessment_email,
)
from backend_v2.scripts.mail import send_bulk_email
from payment.models import DiscountCode, Payment
from utils.enums.models import RegistrationStatus
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin
from utils.helpers.requests import Utils as requestUtils

logger = logging.getLogger(__name__)


def invalidate_participant_cache():
    """Helper function to invalidate participant cache"""
    try:
        # Try to use delete_pattern if available (django-redis)
        if hasattr(cache, "delete_pattern"):
            cache.delete_pattern("participants_all_page_*")
        else:
            # Fallback: clear all cache or use a different approach
            # For now, we'll just clear the entire cache namespace
            # In production, you might want to track cache keys
            cache.clear()
    except Exception:
        # If cache operations fail, continue without cache invalidation
        pass


def resolve_participant_for_payment_email(
    base_queryset,
    *,
    email: str,
    participant_id: int | None = None,
    course_id: int | None = None,
    registration_id: int | None = None,
):
    """
    Resolve which Participant row to mark paid or resend confirmation for.

    Programme = ``Registration`` (includes ``cohort``). Prefer ``participantId``;
    otherwise ``course`` plus optional ``registrationId`` / ``program`` so the
    correct intake row is chosen when the same email has several programmes.

    When resolving without ``participantId``, rows tied to a **closed** programme
    (``Registration.is_open`` is false) are ignored so the payment portal only
    surfaces current (open) intakes. Explicit ``participantId`` still resolves
    the row for completion callbacks.
    """
    email = (email or "").strip()
    if not email:
        return None
    qs = base_queryset.filter(email__iexact=email)
    if participant_id is None:
        qs = qs.filter(Q(registration__isnull=True) | Q(registration__is_open=True))
    if participant_id is not None:
        row = qs.filter(pk=participant_id).first()
        if row is None:
            return None
        if registration_id is not None and row.registration_id != registration_id:
            return None
        if course_id is not None and row.course_id != course_id:
            return None
        return row

    if course_id is not None:
        try:
            course = models.Course.objects.get(pk=course_id)
        except models.Course.DoesNotExist:
            return None
        q = qs.filter(course_id=course_id)
        if registration_id is not None:
            if (
                course.registration_id is not None
                and registration_id != course.registration_id
            ):
                return None
            q = q.filter(registration_id=registration_id)
        elif course.registration_id is not None:
            q = q.filter(registration_id=course.registration_id)
        return q.first()

    if registration_id is not None:
        unpaid = (
            qs.filter(registration_id=registration_id, payment_status=False)
            .order_by("-created_at", "-id")
            .first()
        )
        if unpaid is not None:
            return unpaid
        return (
            qs.filter(registration_id=registration_id)
            .order_by("-created_at", "-id")
            .first()
        )

    unpaid = (
        qs.filter(payment_status=False).order_by("-created_at", "-id").first()
    )
    if unpaid is not None:
        return unpaid
    return qs.order_by("-created_at", "-id").first()


API_KEY = config("PAYMENT_API_KEY")


def handle_payment_success(
    participant_object, serialized_participant_obj, serializer_class
):
    """
    Send one standard registration success email after payment.

    Portal activation emails are not sent here: the student portal is not live yet, and
    course templates already explain portal access timelines (e.g. within 14 days).
    """
    email = serialized_participant_obj.get("email")
    participant_name = serialized_participant_obj.get("name")
    course_id = getattr(participant_object, "course_id", None)
    course_data = serialized_participant_obj.get("course")
    if course_id is None and isinstance(course_data, dict):
        course_id = course_data.get("id")
    if not course_id:
        logger.warning(
            "Payment flow for %s: participant id=%s has no course; skipping welcome email",
            email,
            getattr(participant_object, "id", None),
        )
        return serializer_class.Retrieve(participant_object).data

    try:
        send_registration_success_mail(
            email, course_id, participant_name, activation_url=None
        )
    except Exception:
        logger.exception(
            "send_registration_success_mail failed for %s (course_id=%s)",
            email,
            course_id,
        )

    return serializer_class.Retrieve(participant_object).data


class CoursesViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Course.objects.select_related("registration")
    serializer_class = serializers.CourseSerializer
    admin_actions = ["create", "update", "destroy", "open_course", "close_course"]

    @swagger_auto_schema(request_body=serializers.CourseSerializer.Create)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class.Create(data=request.data)

        if serializer.is_valid():
            course_obj = serializer.save()
            serialized_course_obj = self.serializer_class.Retrieve(course_obj).data
            return requestUtils.success_response(
                data=serialized_course_obj, http_status=status.HTTP_201_CREATED
            )

        return requestUtils.error_response(
            "Error Creating Course",
            serializer.errors,
            http_status=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, pk, *args, **kwargs):
        course_object = self.queryset.get(pk=pk)
        serialized_course_obj = self.serializer_class.Retrieve(course_object).data
        return requestUtils.success_response(
            data=serialized_course_obj, http_status=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=serializers.CourseSerializer.Update())
    def update(self, request, pk, *args, **kwargs):
        course_object = self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(course_object, data=request.data)

        if serializer.is_valid():
            registration_obj = serializer.save()
            serialized_registration_obj = self.serializer_class.Retrieve(
                registration_obj
            ).data
            return requestUtils.success_response(
                data=serialized_registration_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Updating Registration",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk, *args, **kwargs):
        course_object = self.queryset.get(pk=pk)
        course_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(
            data=serializer.data, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=False, methods=["get"])
    def all_opened(self, request):
        query_set = self.queryset.filter(status=True)
        serializer = self.serializer_class.List(query_set, many=True)
        return requestUtils.success_response(
            data=serializer.data, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=True, methods=["put"])
    def open_course(self, request, pk):
        course_object = self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(course_object, data={"status": True})

        if serializer.is_valid():
            course_obj = serializer.save()
            serialized_course_obj = self.serializer_class.Retrieve(course_obj).data
            return requestUtils.success_response(
                data=serialized_course_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Opening Course",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

    @decorators.action(detail=True, methods=["put"])
    def close_course(self, request, pk):
        course_object = self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(course_object, data={"status": False})

        if serializer.is_valid():
            course_obj = serializer.save()
            serialized_course_obj = self.serializer_class.Retrieve(course_obj).data
            return requestUtils.success_response(
                data=serialized_course_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Opening Course",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )


class RegistrationViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Registration.objects
    serializer_class = serializers.RegistrationSerializer
    admin_actions = [
        "create",
        "update",
        "destroy",
        "close_registration",
        "open_registration",
    ]

    @swagger_auto_schema(request_body=serializers.RegistrationSerializer.Create)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class.Create(data=request.data)

        if serializer.is_valid():
            registration_obj = serializer.save()
            serialized_registration_obj = self.serializer_class.Retrieve(
                registration_obj
            ).data
            return requestUtils.success_response(
                data=serialized_registration_obj, http_status=status.HTTP_201_CREATED
            )

        return requestUtils.error_response(
            "Error Creating Registration",
            serializer.errors,
            http_status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(request_body=serializers.RegistrationSerializer.Update())
    def update(self, request, pk, *args, **kwargs):
        registration_object = self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(
            registration_object, data=request.data
        )

        if serializer.is_valid():
            registration_obj = serializer.save()
            serialized_registration_obj = self.serializer_class.Retrieve(
                registration_obj
            ).data
            return requestUtils.success_response(
                data=serialized_registration_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Updating Registration",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk, *args, **kwargs):
        registration_object = self.queryset.get(pk=pk)
        serialized_registration_obj = self.serializer_class.Retrieve(
            registration_object
        ).data
        return requestUtils.success_response(
            data=serialized_registration_obj, http_status=status.HTTP_200_OK
        )

    def destroy(self, request, pk, *args, **kwargs):
        registration_object = self.queryset.get(pk=pk)
        registration_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(
            data=serializer.data, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=False, methods=["get"])
    def all_opened(self, request):
        query_set = self.queryset.filter(is_open=True)
        serializer = self.serializer_class.List(query_set, many=True)
        return requestUtils.success_response(
            data=serializer.data, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=True, methods=["put"])
    def close_registration(self, request, pk=None):
        registration_object = self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(
            registration_object, data={"is_open": False}
        )

        if serializer.is_valid():
            registration_obj = serializer.save()
            serialized_registration_obj = self.serializer_class.Retrieve(
                registration_obj
            ).data
            return requestUtils.success_response(
                data=serialized_registration_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Closing Registration",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

    @decorators.action(detail=True, methods=["put"])
    def open_registration(self, request, pk=None):
        registration_object = self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(
            registration_object, data={"is_open": True}
        )

        if serializer.is_valid():
            registration_obj = serializer.save()
            serialized_registration_obj = self.serializer_class.Retrieve(
                registration_obj
            ).data
            return requestUtils.success_response(
                data=serialized_registration_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Opening Registration",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )


class ParticipantViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    serializer_class = serializers.ParticipantSerializer
    admin_actions = [
        "update",
        "destroy",
        "send_confirmation_email",
        "approve",
        "paid_per_cohort",
    ]

    def get_queryset(self):
        """
        Optimized queryset with select_related, prefetch_related, and ordering.
        This prevents N+1 queries and ensures data is ordered by newest first.
        """
        return (
            models.Participant.objects.select_related(
                "course", "registration", "course__registration"
            )
            .prefetch_related("course__images")
            .order_by("-created_at")
        )

    @property
    def queryset(self):
        """Property to maintain backward compatibility"""
        return self.get_queryset()

    def check_api_key(self, request):
        api_key = request.headers.get("API-Key")
        if not api_key or api_key != API_KEY:
            return False
        return True

    @swagger_auto_schema(request_body=serializers.ParticipantSerializer.Create())
    def create(self, request, *args, **kwargs):
        request_data = (
            request.data.copy()
            if hasattr(request.data, "copy")
            else dict(request.data)
        )

        if request_data.get("registration") in (None, "") and request_data.get(
            "course"
        ):
            course = models.Course.objects.filter(pk=request_data["course"]).first()
            if course:
                resolved = serializers.resolve_open_registration_for_course(course)
                if resolved:
                    request_data["registration"] = resolved.pk

        registration_id = request_data.get("registration")
        if registration_id in (None, ""):
            return requestUtils.error_response(
                "Missing registration",
                {
                    "registration": (
                        "Registration is required, or no open registration was "
                        "found for this course."
                    )
                },
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            registration_obj = models.Registration.objects.get(pk=registration_id)
            if not registration_obj.is_open:
                return requestUtils.error_response(
                    "Registration is closed",
                    {},
                    http_status=status.HTTP_400_BAD_REQUEST,
                )
        except models.Registration.DoesNotExist:
            return requestUtils.error_response(
                "Invalid registration ID", {}, http_status=status.HTTP_400_BAD_REQUEST
            )

        # Handle request data and discount code
        discount_code = request_data.pop("discount", None)

        # Validate discount code if provided
        if discount_code:
            discount_obj = DiscountCode.objects.filter(code=discount_code).first()
            if not discount_obj:
                return requestUtils.error_response(
                    "Invalid discount code", {}, http_status=status.HTTP_400_BAD_REQUEST
                )

            # Use the new validation logic
            user_email = request_data.get("email")
            if user_email:
                can_use, message = discount_obj.can_be_used_by(user_email)
                if not can_use:
                    return requestUtils.error_response(
                        message, {}, http_status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Fallback for legacy validation
                if discount_obj.is_used:
                    return requestUtils.error_response(
                        "Discount code has already been used",
                        {},
                        http_status=status.HTTP_400_BAD_REQUEST,
                    )

        # Serialize and save participant only after successful discount validation
        serializer = self.serializer_class.Create(
            data=request_data, context={"request": request}
        )

        if serializer.is_valid():
            try:
                participant_obj = serializer.save()
                # Invalidate cache when new participant is created
                invalidate_participant_cache()
            except Exception as e:
                return requestUtils.error_response(
                    "Error Creating Participant",
                    str(e),
                    http_status=status.HTTP_400_BAD_REQUEST,
                )
            serialized_participant_obj = self.serializer_class.Retrieve(
                participant_obj
            ).data

            # If a valid discount code was provided, mark it as used
            if discount_code:
                user_email = serialized_participant_obj.get("email")
                participant_id = participant_obj.id

                # Use the new mark_usage method
                discount_obj.mark_usage(user_email, participant_id)

                # For legacy single-use codes, also update claimant
                if discount_obj.offset == 1:
                    discount_obj.claimant = user_email
                    discount_obj.save()

                participant_obj.payment_status = True
                participant_obj.save()
                serialized_participant_obj = self.serializer_class.Retrieve(
                    participant_obj
                ).data
                serialized_participant_obj = handle_payment_success(
                    participant_obj,
                    serialized_participant_obj,
                    self.serializer_class,
                )

            # Return success response
            return requestUtils.success_response(
                data=serialized_participant_obj, http_status=status.HTTP_201_CREATED
            )

        # Check for special case: user already registered but unpaid
        if serializer.errors and "email" in serializer.errors:
            email_errors = serializer.errors["email"]
            if any("payment pending" in str(error) for error in email_errors):
                # Find the existing participant
                email = request_data.get("email")
                course_id = request_data.get("course")
                try:
                    course = models.Course.objects.get(id=course_id)
                    pfilter = {"email__iexact": (email or "").strip(), "course": course}
                    if course.registration_id is not None:
                        pfilter["registration_id"] = course.registration_id
                    participant = models.Participant.objects.filter(**pfilter).first()

                    if participant and not participant.payment_status:
                        return requestUtils.error_response(
                            "Already Registered - Payment Pending",
                            {
                                "already_registered_unpaid": True,
                                "message": "You are already registered for this course but haven't completed payment. Please proceed to payment to secure your spot.",
                                "payment_link": "https://payment.web3bridgeafrica.com",
                                "participant_id": participant.id,
                            },
                            http_status=status.HTTP_400_BAD_REQUEST,
                        )
                except models.Course.DoesNotExist:
                    pass

        # Return error response if serializer is invalid
        return requestUtils.error_response(
            "Error Creating Participant",
            serializer.errors,
            http_status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(request_body=serializers.VerifyPaymentByEmailSerializer)
    @decorators.action(
        detail=False, methods=["post"], url_path="verify-payment-by-email"
    )
    def verify_payment_by_email(self, request, *args, **kwargs):
        if not self.check_api_key(request):
            return Response(
                {"error": "Invalid or missing API key"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        body = serializers.VerifyPaymentByEmailSerializer(data=request.data)
        if not body.is_valid():
            return requestUtils.error_response(
                "Invalid request",
                body.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        email = body.validated_data["email"]
        participant_id = body.validated_data.get("participantId")
        course_id = body.validated_data.get("course")
        registration_id = body.validated_data.get("registration_id")
        mark_paid = body.validated_data.get("status", True)

        participant_object = resolve_participant_for_payment_email(
            self.get_queryset(),
            email=email,
            participant_id=participant_id,
            course_id=course_id,
            registration_id=registration_id,
        )
        if not participant_object:
            return requestUtils.error_response(
                "Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND
            )

        serialized_participant_obj = self.serializer_class.Retrieve(
            participant_object
        ).data
        if not mark_paid:
            return requestUtils.success_response(
                data=serialized_participant_obj, http_status=status.HTTP_200_OK
            )

        if participant_object.payment_status:
            return requestUtils.success_response(
                data=serialized_participant_obj, http_status=status.HTTP_200_OK
            )

        participant_object.payment_status = True
        participant_object.save()
        # Invalidate cache when payment status changes
        invalidate_participant_cache()

        serialized_participant_obj = handle_payment_success(
            participant_object,
            serialized_participant_obj,
            self.serializer_class,
        )
        return requestUtils.success_response(
            data=serialized_participant_obj, http_status=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=serializers.EmailSerializer)
    @decorators.action(
        detail=False, methods=["post"], url_path="check-registration-status"
    )
    def check_registration_status(self, request, *args, **kwargs):
        """Check if a user is already registered and their payment status"""
        email = request.data.get("email")
        course_id = request.data.get("course")

        if not email or not course_id:
            return requestUtils.error_response(
                "Email and course ID are required",
                {},
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            course = models.Course.objects.get(id=course_id)

            # Programme (registration) + course scopes the row (same as payment verify).
            participant_filter = {
                "email__iexact": (email or "").strip(),
                "course": course,
            }
            if course.registration_id is not None:
                participant_filter["registration_id"] = course.registration_id
            participant = models.Participant.objects.filter(**participant_filter).first()

            if not participant:
                return requestUtils.success_response(
                    {
                        "registered": False,
                        "message": "No registration found for this email and course",
                    },
                    http_status=status.HTTP_200_OK,
                )

            if (
                participant.registration_id is not None
                and not participant.registration.is_open
            ):
                return requestUtils.success_response(
                    {
                        "registered": False,
                        "message": "No open registration for this email and course",
                    },
                    http_status=status.HTTP_200_OK,
                )

            return requestUtils.success_response(
                {
                    "registered": True,
                    "payment_status": participant.payment_status,
                    "participant_id": participant.id,
                    "message": "Already paid"
                    if participant.payment_status
                    else "Registered but payment pending",
                    "payment_link": "https://payment.web3bridgeafrica.com"
                    if not participant.payment_status
                    else None,
                },
                http_status=status.HTTP_200_OK,
            )

        except models.Course.DoesNotExist:
            return requestUtils.error_response(
                "Course not found", {}, http_status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(request_body=serializers.SendConfirmationEmailSerializer)
    @decorators.action(
        detail=False, methods=["post"], url_path="send-confirmation-email"
    )
    def send_confirmation_email(self, request, *args, **kwargs):
        """
        Mark the participant paid (if not already) and resend the standard course welcome email.

        Same single welcome email as after payment: no portal activation link (templates already
        describe portal timing where applicable).
        """
        body = serializers.SendConfirmationEmailSerializer(data=request.data)
        if not body.is_valid():
            return requestUtils.error_response(
                "Invalid request",
                body.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )
        email = body.validated_data["email"]
        participant_id = body.validated_data.get("participantId")
        course_id = body.validated_data.get("course")
        registration_id = body.validated_data.get("registration_id")

        participant_object = resolve_participant_for_payment_email(
            self.get_queryset(),
            email=email,
            participant_id=participant_id,
            course_id=course_id,
            registration_id=registration_id,
        )
        if not participant_object:
            return requestUtils.error_response(
                "Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND
            )

        serialized_participant_obj = self.serializer_class.Retrieve(
            participant_object
        ).data
        if not participant_object.payment_status:
            participant_object.payment_status = True
            participant_object.save()
            invalidate_participant_cache()

        course_data = serialized_participant_obj.get("course") or {}
        resolved_course_id = course_data.get("id") or participant_object.course_id
        participant_name = serialized_participant_obj.get("name")

        try:
            send_registration_success_mail(
                participant_object.email,
                resolved_course_id,
                participant_name,
                activation_url=None,
            )
        except Exception:
            logger.exception(
                "send_registration_success_mail failed for confirmation resend (email=%s course_id=%s)",
                participant_object.email,
                resolved_course_id,
            )

        serialized_participant_obj = self.serializer_class.Retrieve(
            participant_object
        ).data
        return requestUtils.success_response(
            data=serialized_participant_obj, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None, *args, **kwargs):
        """
        Approve a participant: sets status to ACCEPTED and sends course-based email.
        For ZK courses, includes a payment link in the email.
        """
        try:
            participant_object = self.get_queryset().get(pk=pk)
        except models.Participant.DoesNotExist:
            return requestUtils.error_response(
                "Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND
            )

        # Update status to ACCEPTED
        participant_object.status = RegistrationStatus.ACCEPTED.value
        participant_object.save()
        # Invalidate cache when participant is updated
        invalidate_participant_cache()

        # Send course-based approval email (ZK includes payment link)
        payment_link = "https://payment.web3bridgeafrica.com"
        send_approval_email(participant_object, payment_link=payment_link)

        serialized_participant_obj = self.serializer_class.Retrieve(
            participant_object
        ).data
        return requestUtils.success_response(
            data=serialized_participant_obj, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=False, methods=["get"], url_path="paid")
    def paid_per_cohort(self, request, *args, **kwargs):
        """
        Fetch all participants that have paid, filtered by cohort.
        Requires admin auth token.
        Query param: ?cohort=Web3 Cohort XIV
        """
        cohort = request.query_params.get("cohort")
        if not cohort:
            return requestUtils.error_response(
                "cohort query parameter is required",
                {},
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(cohort=cohort, payment_status=True)
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.RescheduleAssessmentSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="reschedule")
    def reschedule(self, request, *args, **kwargs):
        """
        Notify a student that their assessment has been rescheduled.
        Sends an email with a CTA button linking to the new assessment and a 3-day deadline notice.

        The participant is resolved as the **latest** row for the given email (newest
        ``created_at``), so re-registrations and multiple cohort rows do not bind to an
        older registration. Cohort in the email and stored record comes from that row.
        """
        serializer = serializers.RescheduleAssessmentSerializer(data=request.data)
        if not serializer.is_valid():
            return requestUtils.error_response(
                "Invalid request data",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        name = serializer.validated_data["name"]
        assessment_link = serializer.validated_data["assessment_link"]

        # Latest registration for this email (same person may appear in multiple cohort rows).
        participant = (
            models.Participant.objects.filter(email__iexact=email)
            .order_by("-created_at", "-id")
            .first()
        )
        if not participant:
            return requestUtils.error_response(
                "Participant not found",
                {
                    "detail": "No participant found with this email. They must be registered first.",
                },
                http_status=status.HTTP_404_NOT_FOUND,
            )

        cohort_label = participant.cohort

        if models.AssessmentReschedule.objects.filter(participant=participant).exists():
            return requestUtils.error_response(
                "Assessment already rescheduled",
                {"detail": "This participant has already rescheduled their assessment once. No further reschedules are allowed."},
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        send_reschedule_assessment_email(email, name, cohort_label, assessment_link)
        models.AssessmentReschedule.objects.create(
            participant=participant, email=email, cohort=cohort_label
        )

        return requestUtils.success_response(
            data={"message": f"Reschedule assessment email sent to {email}"},
            http_status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=serializers.SubmitAssessmentSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="submit-assessment")
    def submit_assessment(self, request, *args, **kwargs):
        """
        Submit an assessment result for a participant.
        Creates an Assessment record and sends a pass or fail email.
        Requires a valid API-Key header.

        If the same email exists on multiple participant rows, pass optional
        ``participant_id`` to target the correct registration; otherwise the
        most recently created participant with that email is used.
        """
        if not self.check_api_key(request):
            return Response(
                {"error": "Invalid or missing API key"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = serializers.SubmitAssessmentSerializer(data=request.data)
        if not serializer.is_valid():
            return requestUtils.error_response(
                "Invalid request data", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]
        score = serializer.validated_data["score"]
        passed = serializer.validated_data["passed"]
        breakdown = serializer.validated_data.get("breakdown")
        participant_id = serializer.validated_data.get("participant_id")

        if participant_id is not None:
            participant = models.Participant.objects.filter(pk=participant_id).first()
            if not participant:
                return requestUtils.error_response(
                    "Participant not found",
                    {"detail": f"No participant with id={participant_id}."},
                    http_status=status.HTTP_404_NOT_FOUND,
                )
            if participant.email.strip().lower() != email.strip().lower():
                return requestUtils.error_response(
                    "Participant email mismatch",
                    {
                        "detail": "participant_id does not match the given email for this participant.",
                    },
                    http_status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Prefer the latest registration if the same email exists on multiple participants
            # (e.g. different cohorts / re-registration after deletion).
            participant = (
                models.Participant.objects.filter(email__iexact=email)
                .order_by("-created_at")
                .first()
            )
            if not participant:
                return requestUtils.error_response(
                    "Participant not found",
                    {"detail": "No participant found with this email. Please register first."},
                    http_status=status.HTTP_404_NOT_FOUND,
                )

        # Block duplicate assessment for the same cohort
        already_exists = models.Assessment.objects.filter(
            participant=participant,
            participant__registration=participant.registration,
        ).exists()
        if already_exists:
            return requestUtils.error_response(
                "Assessment already submitted",
                {"detail": "An assessment record already exists for this participant in this cohort."},
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        # Create assessment record
        from django.utils import timezone
        models.Assessment.objects.create(
            participant=participant,
            score=score,
            breakdown=breakdown,
            passed=passed,
            date_taken=timezone.now(),
        )

        # Send appropriate email (pass vs fail templates from submit-assessment)
        if passed:
            send_assessment_passed_email(
                email, participant.name, participant.cohort, score, breakdown=breakdown
            )
        else:
            send_assessment_failed_email(
                email, participant.name, participant.cohort, score, breakdown=breakdown
            )

        return requestUtils.success_response(
            data={"message": f"Assessment submitted and email sent to {email}"},
            http_status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(request_body=serializers.ParticipantSerializer.Update())
    def update(self, request, pk, *args, **kwargs):
        participant_object = self.get_queryset().get(pk=pk)
        serializer = self.serializer_class.Update(participant_object, data=request.data)

        if serializer.is_valid():
            participant_obj = serializer.save()
            # Invalidate cache when participant is updated
            invalidate_participant_cache()
            serialized_participant_obj = self.serializer_class.Retrieve(
                participant_obj
            ).data
            return requestUtils.success_response(
                data=serialized_participant_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Updating Participant",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk, *args, **kwargs):
        participant_object = self.get_queryset().get(pk=pk)
        serialized_participant_obj = self.serializer_class.Retrieve(
            participant_object
        ).data
        return requestUtils.success_response(
            data=serialized_participant_obj, http_status=status.HTTP_200_OK
        )

    def destroy(self, request, pk, *args, **kwargs):
        participant_object = self.get_queryset().get(pk=pk)

        # Nullify the DB-level FK in payment table before deleting.
        # payment.registration_id references cohort_participant.id but is not
        # managed by Django, so raw SQL is required to preserve payment records.
        #
        # Participant deletion CASCADE-removes related Assessment and AssessmentReschedule
        # (and other FKs with CASCADE). Payment rows are kept with registration_id nulled.
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE payment SET registration_id = NULL WHERE registration_id = %s",
                [participant_object.pk],
            )

        participant_object.delete()
        invalidate_participant_cache()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        """
        Optimized participant listing endpoint with:
        - Redis caching
        - Optimized pagination (no expensive count query)
        - Query optimization (select_related/prefetch_related)
        - Ordering by newest first
        """
        # Get pagination parameters
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 50))

        # Ensure limit doesn't exceed 200 for performance
        limit = min(limit, 200)

        # Calculate offset
        offset = (page - 1) * limit

        # Create cache key based on page and limit
        cache_key = f"participants_all_page_{page}_limit_{limit}"

        # Try to get from cache first (never 500 if Redis is down or misconfigured)
        cached_data = None
        try:
            cached_data = cache.get(cache_key)
        except Exception:
            logger.warning(
                "Participant list cache read failed for %s", cache_key, exc_info=True
            )
        if cached_data:
            return requestUtils.success_response(
                data=cached_data, http_status=status.HTTP_200_OK
            )

        # Get optimized queryset
        queryset = self.get_queryset()

        # Get one extra item to check if there's a next page (without expensive count)
        paginated_queryset = queryset[offset : offset + limit + 1]

        # Check if there's a next page
        has_next = len(paginated_queryset) > limit
        if has_next:
            paginated_queryset = paginated_queryset[:limit]  # Remove the extra item

        # Serialize the data
        serializer = self.serializer_class.List(paginated_queryset, many=True)

        # Calculate pagination info without expensive count query
        has_previous = page > 1

        response_data = {
            "results": serializer.data,
            "pagination": {
                "current_page": page,
                "limit": limit,
                "has_next": has_next,
                "has_previous": has_previous,
                "next_page": page + 1 if has_next else None,
                "previous_page": page - 1 if has_previous else None,
                # Don't include total_count or total_pages to avoid expensive queries
            },
        }

        # Cache the response (configurable TTL); ignore Redis failures
        cache_timeout = getattr(settings, "PARTICIPANT_CACHE_TIMEOUT", 600)
        try:
            cache.set(cache_key, response_data, cache_timeout)
        except Exception:
            logger.warning(
                "Participant list cache write failed for %s", cache_key, exc_info=True
            )

        return requestUtils.success_response(
            data=response_data, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=True, methods=["get"])
    def registration(self, request, pk):
        """
        Get participants by registration ID with optimization
        """
        queryset = self.get_queryset().filter(registration=pk)
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(
            data=serializer.data, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=False, methods=["get"], url_path="stream")
    def stream(self, request):
        """
        Streaming endpoint for large datasets.
        Returns data in chunks using Server-Sent Events (SSE) or JSON streaming.
        This is optimized for fetching thousands of participants without timeout.
        """
        from django.http import StreamingHttpResponse

        # Get parameters
        chunk_size = int(request.GET.get("chunk_size", 100))
        registration_id = request.GET.get("registration", None)
        course_id = request.GET.get("course", None)

        # Build optimized queryset
        queryset = self.get_queryset()

        if registration_id:
            queryset = queryset.filter(registration_id=registration_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        def generate():
            """Generator function that yields JSON chunks"""
            # Send initial metadata
            yield '{"status": "started", "chunk_size": ' + str(chunk_size) + "}\n"

            # Process in chunks
            offset = 0
            total_sent = 0

            while True:
                # Get chunk
                chunk = queryset[offset : offset + chunk_size]
                chunk_list = list(chunk)

                if not chunk_list:
                    break

                # Serialize chunk
                serializer = self.serializer_class.List(chunk_list, many=True)
                chunk_data = serializer.data

                # Yield chunk as JSON
                yield (
                    json.dumps(
                        {
                            "chunk": chunk_data,
                            "offset": offset,
                            "count": len(chunk_data),
                            "total_sent": total_sent + len(chunk_data),
                        }
                    )
                    + "\n"
                )

                offset += chunk_size
                total_sent += len(chunk_data)

                # If we got fewer items than chunk_size, we're done
                if len(chunk_list) < chunk_size:
                    break

            # Send completion message
            yield json.dumps({"status": "completed", "total_sent": total_sent}) + "\n"

        response = StreamingHttpResponse(
            generate(),
            content_type="application/x-ndjson",  # Newline-delimited JSON
        )
        response["X-Accel-Buffering"] = "no"  # Disable buffering in nginx
        return response


class TestimonialViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Testimonial.objects.all()
    serializer_class = serializers.TestimonialSerializer
    admin_actions = ["create", "update", "destroy"]

    @swagger_auto_schema(request_body=serializers.TestimonialSerializer.Create())
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class.Create(data=request.data)

        if serializer.is_valid():
            testimonial_obj = serializer.save()
            serialized_testimonial_obj = self.serializer_class.Retrieve(
                testimonial_obj
            ).data
            return requestUtils.success_response(
                data=serialized_testimonial_obj, http_status=status.HTTP_201_CREATED
            )

        return requestUtils.error_response(
            "Error Creating Testimonial",
            serializer.errors,
            http_status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(request_body=serializers.TestimonialSerializer.Update())
    def update(self, request, pk, *args, **kwargs):
        testimonial_object = self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(testimonial_object, data=request.data)

        if serializer.is_valid():
            testimonial_obj = serializer.save()
            serialized_testimonial_obj = self.serializer_class.Retrieve(
                testimonial_obj
            ).data
            return requestUtils.success_response(
                data=serialized_testimonial_obj, http_status=status.HTTP_200_OK
            )
        else:
            return requestUtils.error_response(
                "Error Updating Testimonial",
                serializer.errors,
                http_status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk, *args, **kwargs):
        testimonial_object = self.queryset.get(pk=pk)
        testimonial_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        testimonial_object = self.queryset.get(pk=pk)
        serialized_testimonial_obj = self.serializer_class.Retrieve(
            testimonial_object
        ).data
        return requestUtils.success_response(
            data=serialized_testimonial_obj, http_status=status.HTTP_200_OK
        )

    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(
            data=serializer.data, http_status=status.HTTP_200_OK
        )


class BulkEmailViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    @swagger_auto_schema(request_body=serializers.BulkEmailSerializer)
    @decorators.action(detail=False, methods=["post"])
    def send_bulk_email(self, request):
        serializer = serializers.BulkEmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data["subject"]
            html_body = serializer.validated_data["body"]
            recipient_ids = serializer.validated_data[
                "recipients"
            ]  # Already validated as integers
            from_admission = request.data.get("from_admission", False)  # New parameter

            if not recipient_ids:
                return Response(
                    {"message": "No recipients provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            logger.info(
                "Bulk email request: subject=%s, recipients=%d, from_admission=%s",
                subject,
                len(recipient_ids),
                from_admission,
            )

            thread = threading.Thread(
                target=send_bulk_email,
                args=(subject, html_body, recipient_ids, from_admission),
                daemon=True,
            )
            thread.start()

            # Return immediately
            return Response(
                {
                    "message": "Email sending initiated",
                    "recipient_count": len(recipient_ids),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.BulkEmailSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="send-admission-email")
    def send_admission_bulk_email(self, request):
        """Send bulk emails from admission@web3bridge.com"""
        serializer = serializers.BulkEmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data["subject"]
            html_body = serializer.validated_data["body"]
            recipient_ids = serializer.validated_data[
                "recipients"
            ]  # Already validated as integers

            if not recipient_ids:
                return Response(
                    {"message": "No recipients provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            logger.info(
                "Admission bulk email request: subject=%s, recipients=%d",
                subject,
                len(recipient_ids),
            )

            thread = threading.Thread(
                target=send_bulk_email,
                args=(subject, html_body, recipient_ids, True),
                daemon=True,
            )
            thread.start()

            # Return immediately
            return Response(
                {
                    "message": "Admission email sending initiated",
                    "recipient_count": len(recipient_ids),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
