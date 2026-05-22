"""
Send (or resend) student portal onboarding invites for paid participants in a cohort.

Progress is printed line-by-line for terminal monitoring. Writes a CSV log for resume.

Portal backend resends activation email when the account is still ``invited`` or
onboarding is ``pending`` / ``invited`` (not yet completed). Already-activated
accounts are reported as skipped.
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
    portal_invite_selection_breakdown,
    resolve_paid_participant_ids,
    send_portal_invite_for_participant,
)
from cohort.models import Participant

LOG_FIELDNAMES = [
    "participant_id",
    "email",
    "name",
    "cohort",
    "course_name",
    "payment_status",
    "participant_status",
    "sent",
    "skipped",
    "reason",
    "error",
    "timestamp",
]


def _log_row(participant: Participant, result: dict) -> dict:
    return {
        "participant_id": participant.id,
        "email": participant.email,
        "name": participant.name,
        "cohort": participant.cohort or "",
        "course_name": getattr(participant.course, "name", "") or "",
        "payment_status": participant.payment_status,
        "participant_status": participant.status or "",
        "sent": result.get("sent"),
        "skipped": result.get("skipped"),
        "reason": result.get("reason") or "",
        "error": result.get("error") or "",
        "timestamp": datetime.utcnow().isoformat(),
    }


class Command(BaseCommand):
    help = (
        "Send or resend portal onboarding invites for paid students registered on/after "
        "2026-04-17 (participant.created_at). Re-sends if portal account not activated."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--registered-from",
            type=str,
            default="2026-04-17",
            help=(
                "Include paid participants registered on/after this date "
                "(participant.created_at, ISO YYYY-MM-DD). Default: 2026-04-17."
            ),
        )
        parser.add_argument(
            "--registered-to",
            type=str,
            default="",
            help="Optional upper date (inclusive) for participant.created_at.",
        )
        parser.add_argument(
            "--cohort",
            type=str,
            default="",
            help="Optional extra filter on participant.cohort text (fuzzy).",
        )
        parser.add_argument(
            "--all-paid",
            action="store_true",
            help="Include every paid, non-evicted, non-rejected participant (ignore cohort/intake)",
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
            help="Process at most N participants (0 = no limit)",
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
                "With --email: portal payload from this participant id; activation mail goes to --email."
            ),
        )
        parser.add_argument(
            "--force-test",
            action="store_true",
            help="With --email: skip paid/ZK validation (for template tests only).",
        )

    def handle(self, *args, **options):
        cohort_arg = (options["cohort"] or "").strip()
        registered_from = (options["registered_from"] or "").strip()
        registered_to = (options["registered_to"] or "").strip() or None
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
            selection_meta = {"cohort_filter": cohort_arg or None}
        else:
            participant_ids, selection_mode, selection_meta = resolve_paid_participant_ids(
                queryset,
                cohort=cohort_arg or None,
                all_paid=all_paid,
                registered_from=registered_from or None,
                registered_to=registered_to,
            )

        breakdown = portal_invite_selection_breakdown(
            queryset,
            registered_from=registered_from or None,
            registered_to=registered_to,
        )

        if limit:
            participant_ids = participant_ids[:limit]

        participants = list(
            queryset.filter(id__in=participant_ids).order_by("-created_at", "-id")
        )
        id_order = {pid: index for index, pid in enumerate(participant_ids)}
        participants.sort(key=lambda p: id_order.get(p.id, 10**9))

        resumed_ids = self._read_sent_participant_ids(resume_log) if resume_log else set()
        if resumed_ids:
            before = len(participants)
            participants = [p for p in participants if p.id not in resumed_ids]
            self.stdout.write(
                self.style.WARNING(
                    f"Resume: skipping {before - len(participants)} already-sent "
                    f"from {resume_log}"
                )
            )

        total = len(participants)
        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Cohort portal invites ==="))
        self.stdout.write(f"Selection mode: {selection_mode}")
        self.stdout.write(
            f"Registration window: {breakdown['registered_from']}"
            + (
                f" → {breakdown['registered_to']} (inclusive)"
                if breakdown.get("registered_to")
                else " → now"
            )
            + f" ({breakdown['registration_field']})"
        )
        if selection_meta.get("cohort_filter"):
            self.stdout.write(f"Cohort text filter: {selection_meta['cohort_filter']}")
        self.stdout.write(f"Total paid (all time): {breakdown['total_paid']}")
        self.stdout.write(
            f"Paid in registration window: {breakdown['registered_since_count']}"
        )
        self.stdout.write(f"Eligible for this run: {total}")
        self.stdout.write(f"Dry run: {dry_run}")
        self.stdout.write(
            f"Portal URL: {getattr(settings, 'PORTAL_ONBOARDING_URL', '')}\n"
        )

        if total == 0:
            self.stdout.write(self.style.WARNING("Nothing to do."))
            return

        if dry_run:
            for index, participant in enumerate(participants, start=1):
                self._print_progress(
                    index,
                    total,
                    participant,
                    {"sent": False, "skipped": True, "reason": "dry_run"},
                )
            self.stdout.write(
                self.style.SUCCESS(f"\nDry run complete ({total} row(s)).")
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

        for index, participant in enumerate(participants, start=1):
            result = send_portal_invite_for_participant(participant)
            row = _log_row(participant, result)
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

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Single portal invite ==="))
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
        )
        self._ensure_log_header(log_file)
        self._append_log(log_file, _log_row(participant, result))
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
