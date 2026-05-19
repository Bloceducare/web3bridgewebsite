from django.db import IntegrityError
from rest_framework import serializers
from . import models
from .helpers.cohort_label import fit_participant_cohort, resolve_active_cohort_label
from utils.serializers import ImageSerializer
from utils.models import Image
from .literals import (
    COURSE_REF_NAME,
    REGISTRATION_REF_NAME,
    PARTICIPANT_REF_NAME,
    TESTIMONIAL_REF_NAME,
)


class BlankStringAsNullPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """``""`` / whitespace-only strings are treated like a missing value (null)."""

    def to_internal_value(self, data):
        if data is None:
            return None
        if isinstance(data, str) and data.strip() == "":
            return None
        return super().to_internal_value(data)


def _validate_loose_phone_number(value: str | None) -> str:
    """
    Very loose international phone check: trim, length cap, any numeric digit (Unicode).

    Allows +, spaces, dashes, parentheses, dots, slashes, etc. No country-specific rules.
    """
    value = (value or "").strip()
    if not value:
        return ""
    if len(value) < 2:
        raise serializers.ValidationError("Phone number is too short.")
    if len(value) > 64:
        raise serializers.ValidationError("Phone number is too long.")
    if not any(ch.isdigit() for ch in value):
        raise serializers.ValidationError(
            "Phone number must include at least one digit."
        )
    return value


def _merge_registration_and_program_ids(attrs: dict) -> dict:
    """
    Accept ``registrationId`` and/or ``program`` (alias) as the Registration (programme) FK.

    When both are sent they must agree. Exposes ``registration_id`` on validated data.
    """
    reg_id = attrs.get("registrationId")
    prog_id = attrs.get("program")
    if reg_id is not None and prog_id is not None and reg_id != prog_id:
        raise serializers.ValidationError(
            {"program": "Must match registrationId when both are provided."}
        )
    attrs["registration_id"] = reg_id if reg_id is not None else prog_id
    return attrs


# Serializer
# Course Serializer
class CourseSerializer:
    class Create(serializers.ModelSerializer):
        images = serializers.ListField(child=serializers.ImageField())

        class Meta:
            model = models.Course
            fields = [
                "name",
                "description",
                "venue",
                "extra_info",
                "images",
                "registration",
                "duration",
            ]
            extra_kwargs = {"venue": {"required": True}}
            ref_name = COURSE_REF_NAME

        def create(self, validated_data):
            images_data = validated_data.pop("images", [])
            course_obj = models.Course.objects.create(**validated_data)

            for image_data in images_data:
                image_object = Image.objects.create(picture=image_data)
                image_object.save()
                course_obj.images.add(image_object)

            course_obj.save()
            return course_obj

    class List(serializers.ModelSerializer):
        images = ImageSerializer(many=True, read_only=True)

        class Meta:
            model = models.Course
            fields = [
                "id",
                "name",
                "description",
                "venue",
                "extra_info",
                "images",
                "status",
                "registration",
                "duration",
            ]

    class Retrieve(serializers.ModelSerializer):
        images = ImageSerializer(many=True, read_only=True)

        class Meta:
            model = models.Course
            fields = [
                "id",
                "name",
                "description",
                "venue",
                "extra_info",
                "images",
                "status",
                "registration",
                "duration",
            ]

    class Update(serializers.ModelSerializer):
        images = serializers.ListField(child=serializers.ImageField(), required=False)

        class Meta:
            ref_name = "courses"
            model = models.Course
            fields = [
                "id",
                "name",
                "description",
                "venue",
                "extra_info",
                "images",
                "status",
                "registration",
                "duration",
            ]
            extra_kwargs = {field: {"required": False} for field in fields}

        def update(self, instance, validated_data):
            images_data = validated_data.pop("images", [])
            uploaded_images = []

            for image_data in images_data:
                image_object = Image.objects.create(picture=image_data)
                image_object.save()
                uploaded_images.append(image_object)

            if len(uploaded_images) > 0:
                instance.images.clear()
                instance.images.set(uploaded_images)

            instance.name = validated_data.get("name", instance.name)
            instance.status = validated_data.get("status", instance.status)
            instance.description = validated_data.get(
                "description", instance.description
            )
            instance.venue = validated_data.get("venue", instance.venue)
            instance.extra_info = validated_data.get("extra_info", instance.extra_info)
            instance.registration = validated_data.get(
                "registration", instance.registration
            )
            instance.duration = validated_data.get("duration", instance.duration)
            instance.save()
            return instance


# Registration Serializer
class RegistrationSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = [
                "id",
                "name",
                "start_date",
                "end_date",
                "registrationFee",
                "cohort",
            ]
            ref_name = REGISTRATION_REF_NAME

        def create(self, validated_data):
            registration_obj = models.Registration.objects.create(**validated_data)
            registration_obj.save()
            return registration_obj

    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = [
                "id",
                "name",
                "is_open",
                "start_date",
                "end_date",
                "registrationFee",
                "courses",
                "cohort",
            ]
            ref_name = REGISTRATION_REF_NAME

    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = [
                "id",
                "name",
                "is_open",
                "start_date",
                "end_date",
                "registrationFee",
                "courses",
                "cohort",
            ]
            ref_name = REGISTRATION_REF_NAME

    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = [
                "id",
                "name",
                "is_open",
                "start_date",
                "end_date",
                "registrationFee",
                "cohort",
            ]
            ref_name = REGISTRATION_REF_NAME
            extra_kwargs = {field: {"required": False} for field in fields}

        def update(self, instance, validated_data):
            instance.name = validated_data.get("name", instance.name)
            instance.is_open = validated_data.get("is_open", instance.is_open)
            instance.start_date = validated_data.get("start_date", instance.start_date)
            instance.end_date = validated_data.get("end_date", instance.end_date)
            instance.registrationFee = validated_data.get(
                "registrationFee", instance.registrationFee
            )
            instance.cohort = validated_data.get("cohort", instance.cohort)
            instance.save()
            return instance


# Participant Serializer
class ParticipantSerializer:
    class Create(serializers.ModelSerializer):
        name = serializers.CharField(required=True)
        wallet_address = serializers.CharField(required=True)
        course = serializers.PrimaryKeyRelatedField(
            queryset=models.Course.objects.select_related("registration"),
            required=True,
        )
        registration = BlankStringAsNullPrimaryKeyRelatedField(
            queryset=models.Registration.objects.all(),
            required=False,
            allow_null=True,
        )
        email = serializers.EmailField(required=True)
        motivation = serializers.CharField(required=False, allow_blank=True, default="")
        achievement = serializers.CharField(
            required=False, allow_blank=True, default=""
        )
        city = serializers.CharField(required=True)
        state = serializers.CharField(required=False, allow_blank=True, default="")
        country = serializers.CharField(required=True)
        # Stored on Participant.gender (max_length=20). Collected on the public registration form (frontend_v2).
        gender = serializers.CharField(
            required=True,
            help_text="Required for new registrations; values such as male, female, or other from the registration UI.",
        )
        github = serializers.URLField(required=False)
        number = serializers.CharField(
            required=False,
            allow_blank=True,
            default="",
            max_length=64,
        )
        venue = serializers.CharField(required=True)

        class Meta:
            model = models.Participant
            exclude = ["status", "payment_status", "cohort"]
            validators = []
            ref_name = PARTICIPANT_REF_NAME

        def validate_number(self, value):
            return _validate_loose_phone_number(value)

        def validate(self, attrs):
            course = attrs.get("course")
            if not course:
                return attrs
            linked = getattr(course, "registration", None)
            if linked is None:
                raise serializers.ValidationError(
                    {
                        "course": (
                            "This course has no programme linked. In admin, set "
                            "Course → registration to your programme."
                        )
                    }
                )
            if not linked.is_open:
                raise serializers.ValidationError(
                    {
                        "registration": (
                            "This course’s programme is not open for registration."
                        )
                    }
                )
            email = (attrs.get("email") or "").strip()
            cohort_value = fit_participant_cohort(
                resolve_active_cohort_label(registration=linked, course=course)
            )
            existing_participant = models.Participant.objects.filter(
                email__iexact=email,
                cohort=cohort_value,
            ).first()
            if existing_participant:
                if existing_participant.payment_status:
                    raise serializers.ValidationError(
                        {
                            "email": (
                                "Participant already registered and paid for this cohort"
                            )
                        }
                    )
                raise serializers.ValidationError(
                    {
                        "email": {
                            "already_registered_unpaid": True,
                            "message": (
                                "You are already registered for this cohort "
                                "but haven't completed payment. Please proceed to payment "
                                "to secure your spot."
                            ),
                            "payment_link": "https://payment.web3bridgeafrica.com",
                            "participant_id": existing_participant.id,
                        }
                    }
                )
            attrs["registration"] = linked
            return attrs

        def create(self, validated_data):
            course = validated_data["course"]
            linked = getattr(course, "registration", None)
            if linked is None:
                raise serializers.ValidationError(
                    {
                        "course": (
                            "This course has no programme linked. In admin, set "
                            "Course -> registration to your programme."
                        )
                    }
                )
            validated_data["registration"] = linked
            validated_data["cohort"] = fit_participant_cohort(
                resolve_active_cohort_label(registration=linked, course=course)
            )
            try:
                return models.Participant.objects.create(**validated_data)
            except IntegrityError:
                # Handle race conditions where duplicate rows slip between validate and create.
                email = (validated_data.get("email") or "").strip()
                cohort_value = validated_data.get("cohort")
                existing_participant = models.Participant.objects.filter(
                    email__iexact=email,
                    cohort=cohort_value,
                ).first()
                if existing_participant:
                    if existing_participant.payment_status:
                        raise serializers.ValidationError(
                            {
                                "email": (
                                    "Participant already registered and paid for this cohort"
                                )
                            }
                        )
                    raise serializers.ValidationError(
                        {
                            "email": {
                                "already_registered_unpaid": True,
                                "message": (
                                    "You are already registered for this cohort "
                                    "but haven't completed payment. Please proceed to payment "
                                    "to secure your spot."
                                ),
                                "payment_link": "https://payment.web3bridgeafrica.com",
                                "participant_id": existing_participant.id,
                            }
                        }
                    )
                raise

    class List(serializers.ModelSerializer):
        course = CourseSerializer.Retrieve(read_only=True)
        registration = RegistrationSerializer.Retrieve(read_only=True)

        class Meta:
            model = models.Participant
            fields = "__all__"
            ref_name = PARTICIPANT_REF_NAME

    class Retrieve(serializers.ModelSerializer):
        course = CourseSerializer.Retrieve(read_only=True)
        registration = RegistrationSerializer.Retrieve(read_only=True)

        class Meta:
            model = models.Participant
            fields = "__all__"
            ref_name = PARTICIPANT_REF_NAME

    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Participant
            fields = [
                "id",
                "name",
                "wallet_address",
                "email",
                "registration",
                "status",
                "motivation",
                "achievement",
                "city",
                "state",
                "country",
                "gender",
                "github",
                "number",
                "course",
                "cohort",
                "venue",
            ]
            extra_kwargs = {field: {"required": False} for field in fields}
            ref_name = PARTICIPANT_REF_NAME

        def validate_number(self, value):
            return _validate_loose_phone_number(value)

        def update(self, instance, validated_data):
            instance.name = validated_data.get("name", instance.name)
            instance.wallet_address = validated_data.get(
                "wallet_address", instance.wallet_address
            )
            instance.email = validated_data.get("email", instance.email)
            instance.registration = validated_data.get(
                "registration", instance.registration
            )
            instance.status = validated_data.get("status", instance.status)
            instance.motivation = validated_data.get("motivation", instance.motivation)
            instance.achievement = validated_data.get(
                "achievement", instance.achievement
            )
            instance.city = validated_data.get("city", instance.city)
            instance.state = validated_data.get("state", instance.state)
            instance.country = validated_data.get("country", instance.country)
            # instance.duration= validated_data.get("duration", instance.duration)
            instance.gender = validated_data.get("gender", instance.gender)
            instance.github = validated_data.get("github", instance.github)
            instance.number = validated_data.get("number", instance.number)
            instance.course = validated_data.get("course", instance.course)
            instance.cohort = validated_data.get("cohort", instance.cohort)
            instance.venue = validated_data.get("venue", instance.venue)
            instance.payment_status = validated_data.get(
                "payment_status", instance.payment_status
            )

            instance.save()
            return instance


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SendConfirmationEmailSerializer(serializers.Serializer):
    """Resend confirmation: optional disambiguators when one email has multiple registrations."""

    email = serializers.EmailField()
    participantId = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Participant primary key (preferred when provided by the client).",
    )
    course = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Course id for the registration to confirm (alternative to participantId).",
    )
    registrationId = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Registration (programme) id; alias field ``program``. Scopes payment to one intake.",
    )
    program = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Alias for registrationId (FK to Registration / programme including cohort).",
    )

    def validate(self, attrs):
        return _merge_registration_and_program_ids(attrs)


class VerifyPaymentByEmailSerializer(serializers.Serializer):
    """Payload from payment service when marking a participant paid on the main server."""

    email = serializers.EmailField()
    paymentId = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
        help_text="Opaque payment reference from the payment backend (stored for tracing only).",
    )
    status = serializers.BooleanField(required=False, default=True)
    participantId = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Disambiguate when the email has multiple cohort registrations.",
    )
    course = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Course id for this payment (alternative to participantId).",
    )
    registrationId = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Registration (programme) id; alias ``program``. Use with course for correct row.",
    )
    program = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Alias for registrationId (Registration / programme intake, includes cohort).",
    )

    def validate(self, attrs):
        return _merge_registration_and_program_ids(attrs)


class RescheduleAssessmentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    cohort = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
        help_text=(
            "Optional. Cohort is taken from the latest participant row for this email "
            "(by registration time), not from this field."
        ),
    )
    assessment_link = serializers.URLField()


class SubmitAssessmentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    participant_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text=(
            "Optional. When set, must match the participant row and the email must match that "
            "participant. Use when multiple registrations share an email."
        ),
    )
    score = serializers.DecimalField(max_digits=5, decimal_places=2)
    passed = serializers.BooleanField()
    breakdown = serializers.JSONField(required=False, allow_null=True)


class CutoffReconcileParticipantItemSerializer(serializers.Serializer):
    email = serializers.EmailField()
    participant_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text=(
            "Optional. When set, must match the participant row and the email must match that "
            "participant. Use when multiple registrations share an email."
        ),
    )


class ReconcileAssessmentCutoffSerializer(serializers.Serializer):
    """
    Bulk reconcile participants who failed under a previous cutoff: mark assessment passed,
    send cutoff-reconciliation email. Same participant resolution rules as submit-assessment.
    """

    items = serializers.ListField(
        child=CutoffReconcileParticipantItemSerializer(),
        min_length=1,
    )
    min_score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
        help_text=(
            "When set, each participant's stored assessment score must be greater than or equal "
            "to this value or the item is skipped."
        ),
    )
    qualifying_threshold_percent = serializers.IntegerField(
        required=False,
        default=50,
        min_value=0,
        max_value=100,
        help_text="Inserted into the email copy (e.g. 50 → '50% and above').",
    )


# Testimonial Serializer
class TestimonialSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = [
                "id",
                "full_name",
                "testimony",
                "picture_link",
                "created_at",
                "updated_at",
            ]
            ref_name = TESTIMONIAL_REF_NAME

        def create(self, validated_data):
            registration_obj = models.Testimonial.objects.create(**validated_data)
            registration_obj.save()
            return registration_obj

    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = [
                "id",
                "full_name",
                "testimony",
                "picture_link",
                "created_at",
                "updated_at",
            ]
            ref_name = TESTIMONIAL_REF_NAME

    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = [
                "id",
                "full_name",
                "testimony",
                "picture_link",
                "created_at",
                "updated_at",
            ]
            ref_name = TESTIMONIAL_REF_NAME

    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = ["id", "full_name", "testimony", "picture_link"]
            ref_name = TESTIMONIAL_REF_NAME
            extra_kwargs = {field: {"required": False} for field in fields}

        def update(self, instance, validated_data):
            instance.headline = validated_data.get("headline", instance.headline)
            instance.full_name = validated_data.get("full_name", instance.full_name)
            instance.testimony = validated_data.get("testimony", instance.testimony)
            instance.picture_link = validated_data.get("picture_link", instance.picture)
            instance.save()
            return instance


class BulkEmailSerializer(serializers.Serializer):
    recipients = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of participant IDs to send the email to",
    )
    subject = serializers.CharField(max_length=200, help_text="Email subject line")
    body = serializers.CharField(help_text="Email body content")

    class Meta:
        fields = ["recipients", "subject", "body"]

    def validate_recipients(self, value):
        if not value:
            raise serializers.ValidationError("At least one recipient is required")

        # Validate all IDs exist in a single bulk query instead of individual queries
        if not isinstance(value, list):
            raise serializers.ValidationError("Recipients must be a list")

        # Convert to integers and remove duplicates
        try:
            recipient_ids = [int(id) for id in value]
            unique_ids = list(set(recipient_ids))
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "All recipient IDs must be valid integers"
            )

        # Bulk check existence
        existing_ids = set(
            models.Participant.objects.filter(id__in=unique_ids).values_list(
                "id", flat=True
            )
        )
        missing_ids = set(unique_ids) - existing_ids

        if missing_ids:
            raise serializers.ValidationError(
                f"Invalid participant IDs: {list(missing_ids)}"
            )

        return unique_ids


class PortalInviteSerializer(serializers.Serializer):
    participant_id = serializers.IntegerField(
        help_text="Participant ID to send the portal onboarding invite to",
    )

    def validate_participant_id(self, value):
        if not models.Participant.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Invalid participant ID: {value}")
        return value


class BulkPortalInviteSerializer(serializers.Serializer):
    participants = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of participant IDs to send portal onboarding invites to",
    )

    def validate_participants(self, value):
        if not value:
            raise serializers.ValidationError("At least one participant is required")

        try:
            participant_ids = [int(pid) for pid in value]
            unique_ids = list(dict.fromkeys(participant_ids))
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                "All participant IDs must be valid integers"
            )

        existing_ids = set(
            models.Participant.objects.filter(id__in=unique_ids).values_list(
                "id", flat=True
            )
        )
        missing_ids = set(unique_ids) - existing_ids
        if missing_ids:
            raise serializers.ValidationError(
                f"Invalid participant IDs: {sorted(missing_ids)}"
            )

        return unique_ids
