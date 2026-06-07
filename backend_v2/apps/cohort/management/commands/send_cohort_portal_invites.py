"""
Send (or resend) student portal onboarding invites for paid Cohort XV participants.

Eligibility: payment_status=True, registered on/after 2026-04-17, cohort match.
Portal filter (portal.users): send/resend unless account_state=active; resend when invited.

Email template (portal_backend): "Welcome to the Web3Bridge Student Portal — Set Up Your Account"
with an activation link. Portal resends when the account is still ``invited`` or onboarding is
``pending`` / ``invited`` (not yet activated). Already-activated accounts are skipped.

Usage:
  # Preview who would receive mail (new invites + pending activation resends)
  python manage.py send_cohort_portal_invites --dry-run

  # Test to your inbox using a real paid student's portal record
  python manage.py send_cohort_portal_invites --email you@example.com --from-participant-id 123

  # Send to all eligible paid Cohort XV students
  python manage.py send_cohort_portal_invites --yes
"""

from __future__ import annotations

import csv
import os
import sys
import time
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from cohort.helpers.portal import (
    DEFAULT_PORTAL_INVITE_REGISTERED_FROM,
    parse_registered_from_date,
    portal_invite_selection_breakdown,
    refine_participants_for_portal_invite,
    resolve_paid_participant_ids,
    send_portal_invite_for_participant,
    summarize_portal_invite_audit,
)
from cohort.models import Participant

DEFAULT_COHORT = "Cohort XV"
DEFAULT_REGISTERED_FROM = DEFAULT_PORTAL_INVITE_REGISTERED_FROM.isoformat()

LOG_FIELDNAMES = [
    "participant_id",
    "email",
    "name",
    "cohort",
    "course_name",
    "payment_status",
    "participant_status",
    "invite_need",
    "sent",
    "skipped",
    "reason",
    "error",
    "timestamp",
]


def _log_row(participant: Participant, result: dict, *, invite_need: str = "") -> dict:
    return {
        "participant_id": participant.id,
        "email": participant.email,
        "name": participant.name,
        "cohort": participant.cohort or "",
        "course_name": getattr(participant.course, "name", "") or "",
        "payment_status": participant.payment_status,
        "participant_status": participant.status or "",
        "invite_need": invite_need,
        "sent": result.get("sent"),
        "skipped": result.get("skipped"),
        "reason": result.get("reason") or "",
        "error": result.get("error") or "",
        "timestamp": datetime.utcnow().isoformat(),
    }


class Command(BaseCommand):
    help = (
        "Send or resend portal onboarding invites for paid Cohort XV students "
        "(registered on/after 2026-04-17). Includes portal users with "
        "account_state=invited who have not activated yet."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--cohort",
            type=str,
            default=DEFAULT_COHORT,
            help=f'Cohort label filter (fuzzy). Default: "{DEFAULT_COHORT}".',
        )
        parser.add_argument(
            "--registered-from",
            type=str,
            default=DEFAULT_REGISTERED_FROM,
            help=(
                "Include paid participants registered on/after this date "
                f"(participant.created_at, ISO YYYY-MM-DD). Default: {DEFAULT_REGISTERED_FROM}."
            ),
        )
        parser.add_argument(
            "--registered-to",
            type=str,
            default="",
            help="Optional upper date (inclusive) for participant.created_at.",
        )
        parser.add_argument(
            "--all-paid",
            action="store_true",
            help="Include every paid participant in cohort/date window (ignore cohort filter)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List eligible participants only; do not call the portal API",
        )
        parser.add_argument(
            "--yes",
            action="store_true",
            help='Skip the "type yes" confirmation prompt',
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=1.0,
            help="Seconds between portal API calls (default: 1.0)",
        )
        parser.add_argument(
            "--log-file",
            type=str,
            default="cohort_portal_invite_log.csv",
            help="CSV log path (default: cohort_portal_invite_log.csv)",
        )
        parser.add_argument(
            "--resume-from-log",
            type=str,
            default="",
            help="Skip participant IDs already marked sent=true in this log",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Process at most N eligible participants (0 = no limit)",
        )
        parser.add_argument(
            "--participant-id",
            type=int,
            action="append",
            default=[],
            help="Only these participant IDs (can repeat flag)",
        )
        parser.add_argument(
            "--email",
            type=str,
            default="",
            help=(
                "Send to one address only. Uses the latest participant row with this email, "
                "or combine with --from-participant-id to deliver using another row's course data."
            ),
        )
        parser.add_argument(
            "--from-participant-id",
            type=int,
            default=None,
            help=(
                "With --email: portal payload from this participant id; "
                "activation mail goes to --email."
            ),
        )
        parser.add_argument(
            "--force-test",
            action="store_true",
            help="With --email: skip paid/approval validation (for template tests only).",
        )

    def handle(self, *args, **options):
        cohort_arg = (options["cohort"] or "").strip()
        registered_from = (options["registered_from"] or DEFAULT_REGISTERED_FROM).strip()
        registered_to = (options["registered_to"] or "").strip() or None
        registered_from_date = parse_registered_from_date(registered_from)
        all_paid = options["all_paid"]
        dry_run = options["dry_run"]
        auto_yes = options["yes"]
        delay = max(0.0, float(options["delay"]))
        log_file = options["log_file"]
        resume_log = (options["resume_from_log"] or "").strip()
        limit = max(0, int(options["limit"] or 0))
        only_ids = options["participant_id"] or []
        single_email = (options["email"] or "").strip().lower()
        from_participant_id = options["from_participant_id"]
        force_test = options["force_test"]

        if not getattr(settings, "PORTAL_ONBOARDING_URL", ""):
            self.stderr.write(
                self.style.ERROR("PORTAL_ONBOARDING_URL is not configured.")
            )
            sys.exit(1)
        if not getattr(settings, "PORTAL_INTERNAL_API_KEY", ""):
            self.stderr.write(
                self.style.ERROR("PORTAL_INTERNAL_API_KEY is not configured.")
            )
            sys.exit(1)

        queryset = Participant.objects.select_related(
            "course", "registration", "course__registration"
        )

        if single_email:
            self._send_single_email_invite(
                queryset=queryset,
                to_email=single_email,
                from_participant_id=from_participant_id,
                dry_run=dry_run,
                force_test=force_test,
                log_file=log_file,
            )
            return

        if only_ids:
            participant_ids = list(dict.fromkeys(only_ids))
            selection_mode = "participant_ids"
            selection_meta = {
                "cohort_filter": cohort_arg or None,
                "registered_from": registered_from_date.isoformat(),
            }
        elif all_paid:
            participant_ids, selection_mode, selection_meta = resolve_paid_participant_ids(
                queryset,
                all_paid=True,
                registered_from=registered_from_date,
                registered_to=registered_to,
            )
        else:
            participant_ids, selection_mode, selection_meta = resolve_paid_participant_ids(
                queryset,
                cohort=cohort_arg or DEFAULT_COHORT,
                registered_from=registered_from_date,
                registered_to=registered_to,
            )

        breakdown = portal_invite_selection_breakdown(
            queryset,
            registered_from=registered_from_date,
            registered_to=registered_to,
        )

        participants = list(
            queryset.filter(id__in=participant_ids).order_by("-created_at", "-id")
        )
        id_order = {pid: index for index, pid in enumerate(participant_ids)}
        participants.sort(key=lambda p: id_order.get(p.id, 10**9))

        eligible_participants, audit_rows = refine_participants_for_portal_invite(
            participants,
            paid_only=True,
        )
        audit_by_id = {
            getattr(row["participant"], "id", None): row for row in audit_rows
        }
        audit_summary = summarize_portal_invite_audit(audit_rows)

        resumed_ids = self._read_sent_participant_ids(resume_log) if resume_log else set()
        if resumed_ids:
            before = len(eligible_participants)
            eligible_participants = [
                p for p in eligible_participants if p.id not in resumed_ids
            ]
            self.stdout.write(
                self.style.WARNING(
                    f"Resume: skipping {before - len(eligible_participants)} already-sent "
                    f"from {resume_log}"
                )
            )

        if limit:
            eligible_participants = eligible_participants[:limit]

        matched_count = len(participants)
        total = len(eligible_participants)
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Cohort portal invites ==="))
        self.stdout.write(
            'Email subject: "Welcome to the Web3Bridge Student Portal — Set Up Your Account"'
        )
        self.stdout.write(f"Selection mode: {selection_mode}")
        if selection_meta.get("cohort_filter"):
            self.stdout.write(f"Cohort filter: {selection_meta['cohort_filter']}")
        self.stdout.write(
            f"Registered on/after: {selection_meta.get('registered_from') or breakdown['registered_from']}"
            + (
                f" → {selection_meta.get('registered_to') or breakdown.get('registered_to')} (inclusive)"
                if selection_meta.get("registered_to") or breakdown.get("registered_to")
                else ""
            )
            + f" ({breakdown['registration_field']})"
        )
        self.stdout.write("Eligibility: payment_status=True only (portal skips active accounts)")
        self.stdout.write(f"Total paid (all time): {breakdown['total_paid']}")
        self.stdout.write(f"Matched selection: {matched_count}")
        self.stdout.write(f"Eligible (send + resend pending): {total}")
        if audit_summary:
            self.stdout.write("Audit:")
            for key, count in sorted(audit_summary.items()):
                self.stdout.write(f"  {key}: {count}")
        self.stdout.write(f"Dry run: {dry_run}")
        self.stdout.write(
            f"Portal URL: {getattr(settings, 'PORTAL_ONBOARDING_URL', '')}\n"
        )

        if matched_count == 0:
            self.stdout.write(self.style.WARNING("No paid participants matched the selection."))
            return

        if total == 0:
            self.stdout.write(
                self.style.WARNING(
                    "No participants need an invite (all activated or filtered out)."
                )
            )
            return

        if dry_run:
            for index, participant in enumerate(eligible_participants, start=1):
                need = (audit_by_id.get(participant.id) or {}).get("reason") or "eligible"
                self._print_progress(
                    index,
                    total,
                    participant,
                    {"sent": False, "skipped": True, "reason": f"dry_run ({need})"},
                )
            skipped = [
                row
                for row in audit_rows
                if not row.get("eligible")
                and getattr(row["participant"], "id", None)
                not in {p.id for p in eligible_participants}
            ]
            if skipped:
                self.stdout.write(self.style.WARNING("\nSkipped (not eligible):"))
                for row in skipped:
                    participant = row["participant"]
                    self.stdout.write(
                        f"  SKIP {participant.email} (id={participant.id}) | {row.get('reason')}"
                    )
            self.stdout.write(
                self.style.SUCCESS(f"\nDry run complete ({total} would be sent).")
            )
            return

        if not auto_yes:
            self.stdout.write(
                self.style.WARNING(
                    f'\nAbout to send/resend {total} portal invite(s). Type "yes":'
                )
            )
            if input().strip().lower() != "yes":
                self.stdout.write(self.style.ERROR("Cancelled."))
                return

        sent_count = 0
        resent_count = 0
        skipped_count = 0
        failed_count = 0

        self._ensure_log_header(log_file)

        for index, participant in enumerate(eligible_participants, start=1):
            invite_need = (audit_by_id.get(participant.id) or {}).get("reason") or ""
            result = send_portal_invite_for_participant(participant, paid_only=True)
            row = _log_row(participant, result, invite_need=invite_need)
            self._append_log(log_file, row)
            self._print_progress(index, total, participant, result)

            reason = result.get("reason") or ""
            if result.get("sent"):
                sent_count += 1
                if reason == "portal_invite_resent":
                    resent_count += 1
            elif result.get("skipped"):
                skipped_count += 1
            else:
                failed_count += 1

            if index < total and delay > 0:
                time.sleep(delay)

        self.stdout.write(self.style.SUCCESS("\n=== Summary ==="))
        self.stdout.write(self.style.SUCCESS(f"Sent (incl. new + resent): {sent_count}"))
        self.stdout.write(self.style.SUCCESS(f"  Resent (not yet activated): {resent_count}"))
        self.stdout.write(self.style.WARNING(f"Skipped (already active, etc.): {skipped_count}"))
        if failed_count:
            self.stdout.write(self.style.ERROR(f"Failed: {failed_count}"))
        else:
            self.stdout.write(self.style.SUCCESS("Failed: 0"))
        self.stdout.write(self.style.SUCCESS(f"Log: {os.path.abspath(log_file)}"))

    def _send_single_email_invite(
        self,
        *,
        queryset,
        to_email: str,
        from_participant_id: int | None,
        dry_run: bool,
        force_test: bool,
        log_file: str,
    ) -> None:
        participant = None
        delivery_override = None

        if from_participant_id is not None:
            participant = queryset.filter(pk=from_participant_id).first()
            if participant is None:
                self.stderr.write(
                    self.style.ERROR(
                        f"No participant with id={from_participant_id}."
                    )
                )
                sys.exit(1)
            if participant.email.lower() != to_email:
                delivery_override = to_email
        else:
            participant = (
                queryset.filter(email__iexact=to_email)
                .order_by("-created_at", "-id")
                .first()
            )
            if participant is None:
                self.stderr.write(
                    self.style.ERROR(
                        f"No participant found for {to_email}. "
                        "Register them first, or pass --from-participant-id <paid_id> "
                        "to send a test using another student's portal record."
                    )
                )
                sys.exit(1)

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Single portal invite (test) ==="))
        self.stdout.write(
            'Email subject: "Welcome to the Web3Bridge Student Portal — Set Up Your Account"'
        )
        self.stdout.write(f"Delivery email: {to_email}")
        self.stdout.write(
            f"Participant id={participant.id} | stored email={participant.email} | "
            f"cohort={participant.cohort or '-'} | paid={participant.payment_status}"
        )
        if delivery_override:
            self.stdout.write(
                self.style.WARNING(
                    f"Using participant {participant.id} data; mail goes to {to_email}"
                )
            )

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Dry run — no API call."))
            return

        result = send_portal_invite_for_participant(
            participant,
            delivery_email=delivery_override,
            skip_validation=force_test,
            paid_only=True,
        )
        self._ensure_log_header(log_file)
        self._append_log(log_file, _log_row(participant, result, invite_need="test"))
        self._print_progress(1, 1, participant, result)

        if result.get("activation_url"):
            self.stdout.write(f"Activation URL: {result['activation_url']}")

        if result.get("sent"):
            self.stdout.write(self.style.SUCCESS("\nInvite email triggered via portal API."))
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"\nFailed: {result.get('error') or result.get('reason')}"
                )
            )
            sys.exit(1)

    def _print_progress(
        self, index: int, total: int, participant: Participant, result: dict
    ) -> None:
        reason = result.get("reason") or result.get("error") or ""
        if result.get("sent"):
            style = self.style.SUCCESS
            label = "SENT"
        elif result.get("skipped"):
            style = self.style.WARNING
            label = "SKIP"
        else:
            style = self.style.ERROR
            label = "FAIL"

        line = (
            f"[{index}/{total}] {label} {participant.email} "
            f"(id={participant.id}, cohort={participant.cohort or '-'}) | {reason}"
        )
        self.stdout.write(style(line))
        self.stdout.flush()

    @staticmethod
    def _ensure_log_header(log_path: str) -> None:
        if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
            return
        with open(log_path, "w", encoding="utf-8", newline="") as fp:
            csv.DictWriter(fp, fieldnames=LOG_FIELDNAMES).writeheader()

    @staticmethod
    def _append_log(log_path: str, row: dict) -> None:
        with open(log_path, "a", encoding="utf-8", newline="") as fp:
            csv.DictWriter(fp, fieldnames=LOG_FIELDNAMES).writerow(row)

    @staticmethod
    def _read_sent_participant_ids(log_path: str) -> set[int]:
        if not os.path.exists(log_path):
            return set()
        sent: set[int] = set()
        with open(log_path, "r", encoding="utf-8", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                if str(row.get("sent")).lower() not in {"true", "1", "yes"}:
                    continue
                try:
                    sent.add(int(row["participant_id"]))
                except (KeyError, TypeError, ValueError):
                    continue
        return sent
