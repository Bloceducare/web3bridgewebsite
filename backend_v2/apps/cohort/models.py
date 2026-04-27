from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from utils.helpers.models import BaseModelBaseMixin, CloudinaryDeleteMixin
from utils.models import Image
from utils.enums.models import RegistrationStatus
from .helpers.model import testimonial_image_location


# Model
# Course model
class Course(BaseModelBaseMixin, models.Model):
    name = models.CharField(_("course name"), max_length=1000, blank=False, null=False)
    description = models.TextField(_("description"), blank=False, null=False)
    venue = models.JSONField(
        _("venue"), null=False, blank=False, default=list, editable=True
    )
    extra_info = models.TextField(_("extra_info"), blank=False, null=False)
    images = models.ManyToManyField(Image, related_name="related_images")
    status = models.BooleanField(default=True)
    duration = models.CharField(
        _("duration"), max_length=100, blank=False, default="3 months"
    )
    # One to Many relationship with Registration
    registration = models.ForeignKey(
        "Registration", related_name="courses", on_delete=models.SET_NULL, null=True
    )
    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"


# Registration openings model
class Registration(BaseModelBaseMixin, models.Model):
    name = models.CharField(
        _("registration name"), max_length=1000, blank=False, null=False
    )
    is_open = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    cohort = models.CharField(
        _("cohort name"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Optional label (e.g. Web3, Web2). Set on each programme in admin."),
    )
    registrationFee = models.CharField(
        _("registration fee"), max_length=50, blank=True, null=True
    )

    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"< {type(self).__name__}({self.name} {self.start_date}-{self.end_date}) >"
        )


# Participant model
class Participant(BaseModelBaseMixin, models.Model):
    name = models.CharField(
        _("full name"), max_length=255, blank=False, null=False, default=""
    )
    wallet_address = models.CharField(
        _("wallet address"), max_length=255, blank=False, null=False
    )
    email = models.EmailField(
        _("participant email"), max_length=255, blank=False, null=False
    )
    registration = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_(
            "Programme (Registration) for payments and reporting; copied from "
            "Course.registration on save when missing."
        ),
    )
    status = models.CharField(
        max_length=20,
        choices=RegistrationStatus.choices(),
        default=RegistrationStatus.PENDING.value,
    )
    motivation = models.TextField(_("motivation"), blank=False, null=True)
    achievement = models.TextField(_("achievement"), blank=False, null=True)
    city = models.CharField(_("city name"), max_length=50, blank=False, null=True)
    state = models.CharField(_("state name"), max_length=50, blank=False, null=True)
    country = models.CharField(_("country name"), max_length=50, blank=False, null=True)
    gender = models.CharField(
        _("gender"),
        max_length=20,
        blank=False,
        null=True,
        help_text="Collected on the registration form (e.g. male, female, other); exposed via Participant create API.",
    )
    github = models.URLField(_("github url"), max_length=250, blank=True, default="")
    number = models.CharField(
        _("phone number"),
        max_length=64,
        blank=False,
        null=True,
        help_text="International formats allowed; validated loosely in the API.",
    )
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    cohort = models.CharField(
        _("cohort name"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Set from the course’s programme on enroll; may be null for legacy rows."),
    )
    payment_status = models.BooleanField(default=False)
    venue = models.CharField(
        _("venue"), max_length=30, blank=False, null=False, default="online"
    )
    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Always persist ``registration_id`` when the course has a programme link.
        Prevents null programme FKs that break payment matching and reporting.
        """
        if self.registration_id is None and self.course_id:
            try:
                rid = (
                    Course.objects.only("registration_id")
                    .get(pk=self.course_id)
                    .registration_id
                )
            except Course.DoesNotExist:
                rid = None
            if rid:
                self.registration_id = rid

        # Keep participant.cohort aligned with programme label when missing.
        if (self.cohort or "").strip() == "" and self.registration_id:
            try:
                registration_obj = Registration.objects.only("cohort", "name").get(
                    pk=self.registration_id
                )
            except Registration.DoesNotExist:
                registration_obj = None
            if registration_obj is not None:
                label = (
                    # registration_obj.cohort
                    registration_obj.name
                    
                ).strip()
                if label:
                    max_len = self._meta.get_field("cohort").max_length
                    self.cohort = label[:max_len]
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email", "registration", "course"],
                name="cohort_participant_email_registration_course_uniq",
            ),
        ]
        indexes = [
            models.Index(fields=["-created_at"], name="participant_created_at_idx"),
            models.Index(fields=["email"], name="participant_email_idx"),
            models.Index(fields=["registration"], name="participant_registration_idx"),
            models.Index(fields=["course"], name="participant_course_idx"),
            models.Index(fields=["status"], name="participant_status_idx"),
        ]

    def __str__(self):
        return f"< {type(self).__name__}({self.name}) >"


# Testimonial model
class Testimonial(BaseModelBaseMixin, CloudinaryDeleteMixin, models.Model):
    headline = models.CharField(_("headline"), max_length=1000, blank=True, null=True)
    full_name = models.CharField(
        _("last name"), max_length=255, blank=False, null=False
    )
    testimony = models.TextField(_("testimony"), blank=False, null=False)
    picture_link = models.URLField(
        _("picture link"), max_length=250, blank=True, default=""
    )
    # picture= models.ImageField(upload_to=testimonial_image_location, blank=False, null=False)
    # brief= models.CharField(_('author brief'), max_length=255, blank=False, null=False)

    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name_processed = self.full_name.replace(" ", "_")
        return f"< {type(self).__name__}({full_name_processed})>"


# Approved Web3 Participant model
class ApprovedWeb3Participant(BaseModelBaseMixin, models.Model):
    """Table to track approved Web3 Cohort XIV participants"""

    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="approved_web3_status",
        null=True,
        blank=True,
        help_text="Reference to the participant (optional if participant doesn't exist yet)",
    )
    email = models.EmailField(
        _("email address"),
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        help_text="Email for lookup (required even if participant exists)",
    )
    notes = models.TextField(
        _("notes"),
        blank=True,
        null=True,
        help_text="Any additional notes about this approval",
    )

    # New timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Approved Web3 Participant"
        verbose_name_plural = "Approved Web3 Participants"
        indexes = [
            models.Index(fields=["email"], name="approved_web3_email_idx"),
            models.Index(fields=["-created_at"], name="approved_web3_created_at_idx"),
        ]

    @property
    def name(self):
        """Get name from participant if available, otherwise None"""
        return self.participant.name if self.participant else None

    @property
    def cohort(self):
        """Get cohort from participant if available, otherwise None"""
        return self.participant.cohort if self.participant else None

    def __str__(self):
        name = self.participant.name if self.participant else self.email
        return f"< {type(self).__name__}({name}) >"


class AssessmentReschedule(models.Model):
    """
    Tracks reschedule requests: at most one per Participant row.
    Tied to Participant (CASCADE) so deleting a participant clears reschedule state;
    re-registration with the same email gets a new Participant and may reschedule again.
    """
    participant = models.OneToOneField(
        Participant,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="assessment_reschedule",
    )
    email = models.EmailField(
        _("email"),
        max_length=255,
        help_text="Denormalized copy of participant email for reporting.",
    )
    cohort = models.CharField(_("cohort"), max_length=255)
    rescheduled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["email"], name="reschedule_email_idx"),
        ]

    def __str__(self):
        return f"< {type(self).__name__}({self.email}) >"


class Assessment(models.Model):
    """Stores assessment results for a participant per cohort."""
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='assessments',
    )
    score = models.DecimalField(_('score'), max_digits=5, decimal_places=2)
    breakdown = models.JSONField(_('breakdown'), blank=True, null=True)
    date_taken = models.DateTimeField(_('date taken'))
    passed = models.BooleanField(_('passed'), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['participant'], name='assessment_participant_idx'),
        ]

    def __str__(self):
        return f"< {type(self).__name__}({self.participant.name} - {self.score}) >"
