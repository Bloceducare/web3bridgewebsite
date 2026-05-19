"""
Send payment reminder emails to Solidity (Web3) applicants who passed the assessment
but have not paid.

Criteria:
- Enrolled on a Solidity course (course name contains "solidity", or --course-id)
- Latest assessment for that participant is passed
- payment_status is False
- Not evicted
"""

import csv
import os
import smtplib
import time
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.core.management.base import BaseCommand
from django.db.models import Prefetch, Q
from django.template.loader import render_to_string

from cohort.models import Assessment, Course, Participant


DEFAULT_SUBJECT = "Complete your Web3Bridge registration – payment required"
PAYMENT_LINK = "https://payment.web3bridgeafrica.com"

DETAIL_FIELDNAMES = [
    "participant_id",
    "name",
    "email",
    "cohort",
    "course_id",
    "course_name",
    "registration_id",
    "registration_name",
    "payment_status",
    "assessment_id",
    "assessment_score",
    "assessment_passed",
    "assessment_date_taken",
    "status",
    "attempts",
    "timestamp",
    "error",
]


def _is_solidity_course_name(course_name: str | None) -> bool:
    return "solidity" in (course_name or "").lower()


def _latest_assessment(participant: Participant) -> Assessment | None:
    assessments = list(participant.assessments.all())
    if not assessments:
        return None
    assessments.sort(key=lambda a: (a.date_taken, a.id), reverse=True)
    return assessments[0]


def _latest_assessment_passed(participant: Participant) -> bool:
    latest = _latest_assessment(participant)
    return latest is not None and bool(latest.passed)


def _matches_cohort_filter(participant: Participant, cohort_filter: str) -> bool:
    if not cohort_filter:
        return True
    needle = cohort_filter.lower()
    haystacks = [
        participant.cohort or "",
        getattr(participant.registration, "name", "") or "",
        getattr(participant.registration, "cohort", "") or "",
        getattr(participant.course, "name", "") or "",
    ]
    return any(needle in value.lower() for value in haystacks)


def _participant_detail_row(
    participant: Participant,
    *,
    status: str,
    attempts: int = 0,
    error: str = "",
) -> dict:
    latest = _latest_assessment(participant)
    return {
        "participant_id": participant.id,
        "name": participant.name,
        "email": participant.email,
        "cohort": participant.cohort or "",
        "course_id": participant.course_id or "",
        "course_name": getattr(participant.course, "name", "") or "",
        "registration_id": participant.registration_id or "",
        "registration_name": getattr(participant.registration, "name", "") or "",
        "payment_status": participant.payment_status,
        "assessment_id": latest.id if latest else "",
        "assessment_score": latest.score if latest else "",
        "assessment_passed": latest.passed if latest else "",
        "assessment_date_taken": latest.date_taken.isoformat() if latest and latest.date_taken else "",
        "status": status,
        "attempts": attempts,
        "timestamp": datetime.utcnow().isoformat(),
        "error": error,
    }


class Command(BaseCommand):
    help = (
        "Email Solidity-track applicants who passed the assessment but have not paid "
        "(payment_status=False)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Export full recipient list to CSV; do not send",
        )
        parser.add_argument(
            "--dry-run-csv",
            type=str,
            default="web3_payment_reminder_dry_run.csv",
            help="CSV path for --dry-run export (default: web3_payment_reminder_dry_run.csv)",
        )
        parser.add_argument(
            "--test-emails",
            type=str,
            default="",
            help="Comma-separated emails to send to (must still match filters unless --force-test)",
        )
        parser.add_argument(
            "--force-test",
            action="store_true",
            help="With --test-emails, skip Solidity/assessment filters for those addresses",
        )
        parser.add_argument(
            "--course-id",
            type=int,
            default=None,
            help="Solidity course id (if omitted, all courses with 'solidity' in the name)",
        )
        parser.add_argument(
            "--cohort-filter",
            type=str,
            default="",
            help='Optional substring filter, e.g. "cohort xv"',
        )
        parser.add_argument(
            "--subject",
            type=str,
            default=DEFAULT_SUBJECT,
            help=f"Email subject (default: {DEFAULT_SUBJECT})",
        )
        parser.add_argument(
            "--delay-between-emails",
            type=float,
            default=1.5,
            help="Seconds between sends (default: 1.5)",
        )
        parser.add_argument(
            "--max-retries",
            type=int,
            default=3,
            help="Retries per recipient (default: 3)",
        )
        parser.add_argument(
            "--log-file",
            type=str,
            default="web3_payment_reminder_log.csv",
            help="CSV path when sending (default: web3_payment_reminder_log.csv)",
        )
        parser.add_argument(
            "--resume-from-log",
            type=str,
            default="",
            help="Skip emails already marked SUCCESS in this log file",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        dry_run_csv = options["dry_run_csv"]
        cohort_filter = (options["cohort_filter"] or "").strip()
        course_id = options["course_id"]
        subject = options["subject"]
        delay_between_emails = max(0.0, float(options["delay_between_emails"]))
        max_retries = max(1, int(options["max_retries"]))
        log_file = options["log_file"]
        resume_from_log = options["resume_from_log"]
        force_test = options["force_test"]
        test_emails = self._parse_test_emails(options["test_emails"])

        solidity_course_ids = self._resolve_solidity_course_ids(course_id)
        if not solidity_course_ids:
            self.stdout.write(
                self.style.ERROR(
                    "No Solidity course found. Pass --course-id or ensure a course "
                    "with 'solidity' in the name exists."
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Solidity course id(s): {', '.join(str(cid) for cid in solidity_course_ids)}"
            )
        )
        for cid in solidity_course_ids:
            course = Course.objects.filter(pk=cid).only("name").first()
            if course:
                self.stdout.write(f"  - {cid}: {course.name}")

        if test_emails:
            participants = self._participants_for_test(
                test_emails,
                solidity_course_ids=solidity_course_ids,
                force_test=force_test,
            )
        else:
            participants = self._eligible_participants(
                solidity_course_ids=solidity_course_ids,
                cohort_filter=cohort_filter,
            )

        if resume_from_log and not dry_run:
            sent_before = self._read_successful_emails(resume_from_log)
            if sent_before:
                before = len(participants)
                participants = [p for p in participants if p.email.lower() not in sent_before]
                self.stdout.write(
                    self.style.WARNING(
                        f"Resume: skipped {before - len(participants)} already sent"
                    )
                )

        self.stdout.write(self.style.SUCCESS(f"\nEligible recipients: {len(participants)}"))
        if not participants:
            self.stdout.write(self.style.WARNING("No matching participants. Exiting."))
            return

        detail_rows = [
            _participant_detail_row(participant, status="DRY_RUN" if dry_run else "PENDING")
            for participant in participants
        ]

        if dry_run:
            self._write_csv(dry_run_csv, detail_rows, mode="w")
            self.stdout.write(self.style.SUCCESS("\n=== Dry run — full recipient list ==="))
            for index, row in enumerate(detail_rows, start=1):
                self.stdout.write(
                    f"{index}. {row['name']} <{row['email']}> | "
                    f"participant_id={row['participant_id']} | "
                    f"course_id={row['course_id']} ({row['course_name']}) | "
                    f"cohort={row['cohort']} | "
                    f"assessment_id={row['assessment_id']} | "
                    f"score={row['assessment_score']} | passed={row['assessment_passed']} | "
                    f"paid={row['payment_status']}"
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nDry run complete. {len(detail_rows)} row(s) written to "
                    f"{os.path.abspath(dry_run_csv)}"
                )
            )
            return

        self.stdout.write(
            self.style.WARNING(f'\nAbout to send {len(participants)} email(s). Type "yes":')
        )
        if input().strip().lower() != "yes":
            self.stdout.write(self.style.ERROR("Cancelled."))
            return

        sent_count = 0
        failed_count = 0
        smtp_connection = None

        try:
            for index, participant in enumerate(participants, start=1):
                status = "FAILED"
                error_message = ""
                attempts_used = 0

                for attempt in range(1, max_retries + 1):
                    attempts_used = attempt
                    try:
                        if smtp_connection is None:
                            smtp_connection = self._build_smtp_connection()
                        self._send_email(participant, subject, smtp_connection)
                        status = "SUCCESS"
                        sent_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"[{index}/{len(participants)}] Sent to {participant.email}"
                            )
                        )
                        break
                    except Exception as exc:  # noqa: BLE001
                        error_message = str(exc)
                        if attempt < max_retries:
                            if isinstance(exc, smtplib.SMTPServerDisconnected) or (
                                "connection unexpectedly closed" in error_message.lower()
                            ):
                                self._close_smtp(smtp_connection)
                                smtp_connection = self._build_smtp_connection()
                            time.sleep(attempt * 2)
                        else:
                            failed_count += 1
                            self.stdout.write(
                                self.style.ERROR(
                                    f"[{index}/{len(participants)}] Failed {participant.email}: "
                                    f"{error_message}"
                                )
                            )

                row = _participant_detail_row(
                    participant,
                    status=status,
                    attempts=attempts_used,
                    error=error_message,
                )
                self._append_log(log_file, row)

                if index < len(participants) and delay_between_emails > 0:
                    time.sleep(delay_between_emails)
        finally:
            self._close_smtp(smtp_connection)

        self.stdout.write(self.style.SUCCESS("\n=== Summary ==="))
        self.stdout.write(self.style.SUCCESS(f"Sent: {sent_count}"))
        self.stdout.write(
            self.style.ERROR(f"Failed: {failed_count}")
            if failed_count
            else self.style.SUCCESS("Failed: 0")
        )
        self.stdout.write(self.style.SUCCESS(f"Log: {os.path.abspath(log_file)}"))

    def _resolve_solidity_course_ids(self, course_id: int | None) -> list[int]:
        if course_id is not None:
            course = Course.objects.filter(pk=course_id).only("id", "name").first()
            if course is None:
                return []
            if not _is_solidity_course_name(course.name):
                self.stdout.write(
                    self.style.WARNING(
                        f"Course id={course_id} name does not contain 'solidity': {course.name}"
                    )
                )
            return [course.id]
        return list(
            Course.objects.filter(name__icontains="solidity")
            .order_by("-id")
            .values_list("id", flat=True)
        )

    def _eligible_participants(
        self,
        *,
        solidity_course_ids: list[int],
        cohort_filter: str,
    ) -> list[Participant]:
        assessment_prefetch = Prefetch(
            "assessments",
            queryset=Assessment.objects.order_by("-date_taken", "-id"),
        )
        qs = (
            Participant.objects.filter(
                payment_status=False,
                is_evicted=False,
                course_id__in=solidity_course_ids,
            )
            .exclude(Q(email="") | Q(email__isnull=True))
            .select_related("course", "registration")
            .prefetch_related(assessment_prefetch)
            .order_by("-created_at", "-id")
        )

        by_email: dict[str, Participant] = {}
        for participant in qs:
            if not _matches_cohort_filter(participant, cohort_filter):
                continue
            if not _latest_assessment_passed(participant):
                continue
            key = participant.email.strip().lower()
            if key not in by_email:
                by_email[key] = participant
        return list(by_email.values())

    def _participants_for_test(
        self,
        test_emails: list[str],
        *,
        solidity_course_ids: list[int],
        force_test: bool,
    ) -> list[Participant]:
        assessment_prefetch = Prefetch(
            "assessments",
            queryset=Assessment.objects.order_by("-date_taken", "-id"),
        )
        participants: list[Participant] = []
        for email in test_emails:
            row = (
                Participant.objects.filter(email__iexact=email)
                .select_related("course", "registration")
                .prefetch_related(assessment_prefetch)
                .order_by("-created_at", "-id")
                .first()
            )
            if row is None:
                self.stdout.write(self.style.WARNING(f"No participant for {email}, skipped"))
                continue
            if not force_test:
                if row.course_id not in solidity_course_ids:
                    self.stdout.write(
                        self.style.WARNING(
                            f"{email}: course_id={row.course_id} is not a Solidity course, skipped"
                        )
                    )
                    continue
                if not _latest_assessment_passed(row):
                    self.stdout.write(
                        self.style.WARNING(f"{email}: no passed assessment, skipped")
                    )
                    continue
                if row.payment_status:
                    self.stdout.write(self.style.WARNING(f"{email}: already paid, skipped"))
                    continue
            participants.append(row)
        return participants

    def _send_email(self, participant: Participant, subject: str, smtp_connection) -> None:
        context = {
            "name": participant.name,
            "payment_link": PAYMENT_LINK,
        }
        html_body = render_to_string("cohort/web3_payment_reminder_email.html", context)
        from_email = getattr(
            settings, "ADMISSION_EMAIL_HOST_USER", settings.DEFAULT_FROM_EMAIL
        )
        email_msg = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=from_email,
            to=[participant.email],
        )
        email_msg.content_subtype = "html"
        email_msg.connection = smtp_connection
        email_msg.send(fail_silently=False)

    @staticmethod
    def _parse_test_emails(value: str) -> list[str]:
        if not value:
            return []
        seen: set[str] = set()
        emails: list[str] = []
        for raw in value.split(","):
            candidate = raw.strip().lower()
            if not candidate or candidate in seen:
                continue
            seen.add(candidate)
            emails.append(candidate)
        return emails

    @staticmethod
    def _read_successful_emails(log_path: str) -> set[str]:
        if not os.path.exists(log_path):
            return set()
        successful: set[str] = set()
        with open(log_path, "r", encoding="utf-8", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                if (row.get("status") or "").upper() == "SUCCESS":
                    email = (row.get("email") or "").strip().lower()
                    if email:
                        successful.add(email)
        return successful

    @staticmethod
    def _build_smtp_connection():
        return get_connection(
            host=getattr(settings, "ADMISSION_EMAIL_HOST", settings.EMAIL_HOST),
            port=getattr(settings, "ADMISSION_EMAIL_PORT", settings.EMAIL_PORT),
            username=getattr(settings, "ADMISSION_EMAIL_HOST_USER"),
            password=getattr(settings, "ADMISSION_EMAIL_HOST_PASSWORD"),
            use_tls=getattr(settings, "ADMISSION_EMAIL_USE_TLS", settings.EMAIL_USE_TLS),
        )

    @staticmethod
    def _close_smtp(connection) -> None:
        if not connection:
            return
        try:
            connection.close()
        except Exception:  # noqa: BLE001
            return

    @staticmethod
    def _write_csv(path: str, rows: list[dict], *, mode: str = "w") -> None:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, mode, encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=DETAIL_FIELDNAMES)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: row.get(key, "") for key in DETAIL_FIELDNAMES})

    @staticmethod
    def _append_log(log_file: str, row: dict) -> None:
        directory = os.path.dirname(log_file)
        if directory:
            os.makedirs(directory, exist_ok=True)
        write_header = not os.path.exists(log_file) or os.path.getsize(log_file) == 0
        with open(log_file, "a", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=DETAIL_FIELDNAMES)
            if write_header:
                writer.writeheader()
            writer.writerow({key: row.get(key, "") for key in DETAIL_FIELDNAMES})
