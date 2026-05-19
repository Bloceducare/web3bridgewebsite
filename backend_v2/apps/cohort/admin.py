from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .helpers.portal import execute_portal_invite_bulk, send_portal_invite_for_participant
from .models import (
    ApprovedWeb3Participant,
    Course,
    Participant,
    Registration,
    Testimonial,
)


@admin.action(description="Send portal invite email (paid, non-ZK)")
def send_portal_invite_bulk_action(modeladmin, request, queryset):
    """Django admin list action: bulk portal onboarding invites."""
    participant_ids = list(queryset.values_list("id", flat=True))
    if not participant_ids:
        modeladmin.message_user(request, "No participants selected.", level=messages.WARNING)
        return

    summary = execute_portal_invite_bulk(
        participant_ids=participant_ids,
        queryset=queryset,
    )
    modeladmin.message_user(
        request,
        (
            f"Portal invites finished: {summary['sent_count']} sent, "
            f"{summary['skipped_count']} skipped, {summary['failed_count']} failed "
            f"(of {summary['total']})."
        ),
        level=messages.SUCCESS if summary["failed_count"] == 0 else messages.WARNING,
    )


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "cohort",
        "status",
        "payment_status",
        "is_evicted",
        "course",
        "created_at",
    )
    list_filter = ("payment_status", "status", "is_evicted", "course")
    search_fields = ("name", "email", "cohort")
    readonly_fields = ("created_at", "updated_at", "portal_invite_actions")
    actions = [send_portal_invite_bulk_action]
    ordering = ["-created_at"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "number",
                    "course",
                    "registration",
                    "cohort",
                    "status",
                    "payment_status",
                    "is_evicted",
                    "evicted_at",
                    "eviction_reason",
                )
            },
        ),
        (
            "Portal invite",
            {"fields": ("portal_invite_actions",)},
        ),
        (
            "Other",
            {
                "fields": (
                    "wallet_address",
                    "motivation",
                    "achievement",
                    "city",
                    "state",
                    "country",
                    "gender",
                    "github",
                    "venue",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<path:object_id>/send-portal-invite/",
                self.admin_site.admin_view(self.send_portal_invite_view),
                name="cohort_participant_send_portal_invite",
            ),
        ]
        return custom + urls

    @admin.display(description="Portal invite")
    def portal_invite_actions(self, obj):
        if not obj or not obj.pk:
            return "Save the participant first."
        url = reverse("admin:cohort_participant_send_portal_invite", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">Send portal invite email</a>',
            url,
        )

    def send_portal_invite_view(self, request, object_id):
        participant = self.get_object(request, object_id)
        if participant is None:
            self.message_user(request, "Participant not found.", level=messages.ERROR)
            return redirect("admin:cohort_participant_changelist")

        result = send_portal_invite_for_participant(participant)
        if result.get("sent"):
            self.message_user(
                request,
                f"Portal invite sent to {result.get('email')} ({result.get('reason')}).",
                level=messages.SUCCESS,
            )
        elif result.get("skipped"):
            self.message_user(
                request,
                f"Portal invite skipped for {result.get('email')}: {result.get('reason')}.",
                level=messages.WARNING,
            )
        else:
            self.message_user(
                request,
                f"Portal invite failed for {result.get('email')}: {result.get('error')}.",
                level=messages.ERROR,
            )
        return redirect("admin:cohort_participant_change", object_id)


admin.site.register(Course)
admin.site.register(Registration)
admin.site.register(Testimonial)


@admin.register(ApprovedWeb3Participant)
class ApprovedWeb3ParticipantAdmin(admin.ModelAdmin):
    list_display = ("email", "get_name", "get_cohort", "participant", "created_at")
    list_filter = ("created_at",)
    search_fields = ("email", "participant__name", "participant__email")
    readonly_fields = ("created_at", "updated_at", "get_name", "get_cohort")
    ordering = ["-created_at"]
    fields = (
        "participant",
        "email",
        "notes",
        "get_name",
        "get_cohort",
        "created_at",
        "updated_at",
    )

    def get_name(self, obj):
        return obj.name or "N/A"

    get_name.short_description = "Name"

    def get_cohort(self, obj):
        return obj.cohort or "N/A"

    get_cohort.short_description = "Cohort"
