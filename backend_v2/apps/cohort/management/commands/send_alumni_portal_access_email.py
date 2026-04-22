import csv
import os
import re
import smtplib
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DEFAULT_SUBJECT = "Web3bridge Alumni Portal is ready for use"


@dataclass
class RecipientTokenPair:
    email: str
    token: str


class Command(BaseCommand):
    help = (
        "Send alumni portal announcement mail by pairing emails from mails.csv with "
        "available access tokens from access-tokens.csv."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--emails-csv",
            type=str,
            default=str(
                Path(settings.BASE_DIR) / "apps" / "cohort" / "management" / "mails.csv"
            ),
            help="Path to recipient emails CSV (default: apps/cohort/management/mails.csv)",
        )
        parser.add_argument(
            "--tokens-csv",
            type=str,
            default=str(Path(settings.BASE_DIR) / "access-tokens.csv"),
            help="Path to access tokens CSV (default: access-tokens.csv)",
        )
        parser.add_argument(
            "--subject",
            type=str,
            default=DEFAULT_SUBJECT,
            help=f'Email subject line (default: "{DEFAULT_SUBJECT}")',
        )
        parser.add_argument(
            "--from-email",
            type=str,
            default=getattr(settings, "DEFAULT_FROM_EMAIL", "support@web3bridge.com"),
            help="Sender email address (default: DEFAULT_FROM_EMAIL / support@web3bridge.com)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview pairings without sending emails",
        )
        parser.add_argument(
            "--test-emails",
            type=str,
            default="",
            help='Comma-separated test recipients (example: "me@example.com,ayodeji@web3bridge.com")',
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Optional cap on number of emails to send/pair (default: all)",
        )
        parser.add_argument(
            "--max-retries",
            type=int,
            default=3,
            help="Maximum retries per email (default: 3)",
        )
        parser.add_argument(
            "--delay-between-emails",
            type=float,
            default=1.5,
            help="Delay in seconds between emails (default: 1.5)",
        )
        parser.add_argument(
            "--log-file",
            type=str,
            default="alumni_portal_email_log.csv",
            help="CSV path for send logs (default: alumni_portal_email_log.csv)",
        )
        parser.add_argument(
            "--resume-from-log",
            type=str,
            default="",
            help=(
                "Optional existing log file path. Successful recipients in that log "
                "will be excluded from this run."
            ),
        )
        parser.add_argument(
            "--start-from-index",
            type=int,
            default=1,
            help=(
                "1-based position to start from when logs are unavailable "
                "(example: 51 starts from recipient/token #51)."
            ),
        )
        parser.add_argument(
            "--preserve-duplicates",
            action="store_true",
            help=(
                "Preserve duplicate emails from mails.csv (indexing follows raw CSV order). "
                "Default behavior deduplicates addresses."
            ),
        )

    def handle(self, *args, **options):
        emails_csv = options["emails_csv"]
        tokens_csv = options["tokens_csv"]
        subject = options["subject"]
        from_email = options["from_email"]
        dry_run = options["dry_run"]
        test_emails_raw = options["test_emails"]
        limit = max(0, int(options["limit"]))
        max_retries = max(1, int(options["max_retries"]))
        delay_between_emails = max(0.0, float(options["delay_between_emails"]))
        log_file = options["log_file"]
        resume_from_log = options["resume_from_log"]
        start_from_index = max(1, int(options["start_from_index"]))
        preserve_duplicates = options["preserve_duplicates"]

        test_emails = self._parse_test_emails(test_emails_raw)
        if test_emails:
            emails = test_emails
            self.stdout.write(
                self.style.WARNING(
                    f"Test mode enabled: sending only to {len(emails)} email(s)."
                )
            )
        else:
            emails = self._read_recipient_emails(
                emails_csv, preserve_duplicates=preserve_duplicates
            )

        if resume_from_log:
            previously_sent = self._read_successful_emails_from_log(resume_from_log)
            if previously_sent:
                before_count = len(emails)
                emails = [email for email in emails if email not in previously_sent]
                skipped = before_count - len(emails)
                self.stdout.write(
                    self.style.WARNING(
                        f"Resume mode: skipped {skipped} email(s) already marked SUCCESS "
                        f"in {resume_from_log}"
                    )
                )
        tokens = self._read_available_tokens(tokens_csv)

        if start_from_index > 1:
            offset = start_from_index - 1
            self.stdout.write(
                self.style.WARNING(
                    f"Manual start index enabled: starting from #{start_from_index} "
                    f"(skipping first {offset} recipient(s) and token(s))."
                )
            )
            emails = emails[offset:]
            tokens = tokens[offset:]

        if not emails:
            self.stdout.write(self.style.ERROR("No valid recipient emails found. Exiting."))
            return
        if not tokens:
            self.stdout.write(self.style.ERROR("No available access tokens found. Exiting."))
            return

        pairs = self._build_pairs(emails, tokens, limit)
        skipped_due_to_token_shortage = max(0, len(emails) - len(pairs))

        self.stdout.write(self.style.SUCCESS(f"Loaded recipients: {len(emails)}"))
        self.stdout.write(self.style.SUCCESS(f"Loaded available tokens: {len(tokens)}"))
        self.stdout.write(self.style.SUCCESS(f"Prepared email-token pairs: {len(pairs)}"))
        if skipped_due_to_token_shortage:
            self.stdout.write(
                self.style.WARNING(
                    f"Skipped {skipped_due_to_token_shortage} recipient(s) due to token shortage."
                )
            )

        self.stdout.write(self.style.SUCCESS("\n=== Pairing Preview ==="))
        for index, pair in enumerate(pairs[:10], start=1):
            self.stdout.write(f"{index}. {pair.email} -> {pair.token}")
        if len(pairs) > 10:
            self.stdout.write(f"... and {len(pairs) - 10} more")

        if dry_run:
            self.stdout.write(self.style.WARNING("\nDry run complete. No emails sent."))
            return

        self.stdout.write(
            self.style.WARNING(
                f'\nAbout to send {len(pairs)} email(s). Type "yes" to continue:'
            )
        )
        confirm = input().strip().lower()
        if confirm != "yes":
            self.stdout.write(self.style.ERROR("Operation cancelled."))
            return

        sent_rows = []
        failed_rows = []
        smtp_connection = None

        try:
            for index, pair in enumerate(pairs, start=1):
                status = "FAILED"
                error_message = ""
                attempts_used = 0

                for attempt in range(1, max_retries + 1):
                    attempts_used = attempt
                    try:
                        if smtp_connection is None:
                            smtp_connection = self._build_smtp_connection()
                        self._send_email(pair, subject, from_email, smtp_connection)
                        status = "SUCCESS"
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"[{index}/{len(pairs)}] Sent to {pair.email} (attempt {attempt})"
                            )
                        )
                        break
                    except Exception as exc:  # noqa: BLE001
                        error_message = str(exc)
                        if attempt < max_retries:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"[{index}/{len(pairs)}] Retry {attempt}/{max_retries} for "
                                    f"{pair.email}: {error_message}"
                                )
                            )
                            # Gmail often drops long-lived SMTP sessions; reconnect before retry.
                            if isinstance(exc, smtplib.SMTPServerDisconnected) or (
                                "connection unexpectedly closed" in error_message.lower()
                            ):
                                self._close_smtp_connection(smtp_connection)
                                smtp_connection = self._build_smtp_connection()
                            time.sleep(attempt * 2)
                        else:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"[{index}/{len(pairs)}] Failed for {pair.email}: {error_message}"
                                )
                            )

                row = {
                    "email": pair.email,
                    "token": pair.token,
                    "status": status,
                    "attempts": attempts_used,
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": error_message,
                }
                if status == "SUCCESS":
                    sent_rows.append(row)
                else:
                    failed_rows.append(row)
                # Persist progress on each recipient so resume works after crashes/disconnects.
                self._save_results(log_file, [row], [])

                if index < len(pairs) and delay_between_emails > 0:
                    time.sleep(delay_between_emails)
        finally:
            self._close_smtp_connection(smtp_connection)

        self.stdout.write(self.style.SUCCESS("\n=== Summary ==="))
        self.stdout.write(self.style.SUCCESS(f"Total targeted: {len(pairs)}"))
        self.stdout.write(self.style.SUCCESS(f"Sent: {len(sent_rows)}"))
        self.stdout.write(
            self.style.ERROR(f"Failed: {len(failed_rows)}")
            if failed_rows
            else self.style.SUCCESS("Failed: 0")
        )
        self.stdout.write(self.style.SUCCESS(f"Log file: {os.path.abspath(log_file)}"))

    def _read_recipient_emails(
        self, csv_path: str, preserve_duplicates: bool = False
    ) -> list[str]:
        emails: list[str] = []
        seen: set[str] = set()
        with open(csv_path, "r", encoding="utf-8", newline="") as fp:
            for raw_line in fp:
                candidate = raw_line.strip().rstrip(",").lower()
                if not candidate:
                    continue
                if not EMAIL_PATTERN.match(candidate):
                    continue
                if not preserve_duplicates:
                    if candidate in seen:
                        continue
                    seen.add(candidate)
                emails.append(candidate)
        return emails

    def _read_available_tokens(self, csv_path: str) -> list[str]:
        tokens: list[str] = []
        with open(csv_path, "r", encoding="utf-8", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                code = (row.get("code") or "").strip()
                used_value = (row.get("used") or "").strip().lower()
                is_used = used_value in {"1", "true", "yes"}
                if code and not is_used:
                    tokens.append(code)
        return tokens

    def _build_pairs(
        self, emails: list[str], tokens: list[str], limit: int
    ) -> list[RecipientTokenPair]:
        pair_count = min(len(emails), len(tokens))
        if limit > 0:
            pair_count = min(pair_count, limit)
        return [
            RecipientTokenPair(email=emails[index], token=tokens[index])
            for index in range(pair_count)
        ]

    def _parse_test_emails(self, value: str) -> list[str]:
        if not value:
            return []
        emails: list[str] = []
        seen: set[str] = set()
        for raw in value.split(","):
            candidate = raw.strip().rstrip(",").lower()
            if not candidate or not EMAIL_PATTERN.match(candidate):
                continue
            if candidate in seen:
                continue
            seen.add(candidate)
            emails.append(candidate)
        return emails

    def _read_successful_emails_from_log(self, log_path: str) -> set[str]:
        successful_emails: set[str] = set()
        if not os.path.exists(log_path):
            self.stdout.write(
                self.style.WARNING(f"Resume log not found: {log_path}. Continuing without resume.")
            )
            return successful_emails

        with open(log_path, "r", encoding="utf-8", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                status = (row.get("status") or "").strip().upper()
                email = (row.get("email") or "").strip().lower()
                if status == "SUCCESS" and email:
                    successful_emails.add(email)
        return successful_emails

    def _send_email(
        self,
        pair: RecipientTokenPair,
        subject: str,
        from_email: str,
        smtp_connection,
    ) -> None:
        context = {"access_token": pair.token}
        html_body = render_to_string("cohort/alumni_portal_access_email.html", context)

        email_msg = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=from_email,
            to=[pair.email],
        )
        email_msg.content_subtype = "html"
        email_msg.connection = smtp_connection

        email_msg.send(fail_silently=False)

    def _build_smtp_connection(self):
        connection = get_connection(
            host=getattr(settings, "EMAIL_HOST", None),
            port=getattr(settings, "EMAIL_PORT", None),
            username=getattr(settings, "EMAIL_HOST_USER", None),
            password=getattr(settings, "EMAIL_HOST_PASSWORD", None),
            use_tls=getattr(settings, "EMAIL_USE_TLS", True),
        )
        return connection

    def _close_smtp_connection(self, connection) -> None:
        if not connection:
            return
        try:
            connection.close()
        except Exception:  # noqa: BLE001
            return

    def _save_results(self, log_file: str, sent_rows: list[dict], failed_rows: list[dict]) -> None:
        all_rows = sent_rows + failed_rows
        if not all_rows:
            return

        directory = os.path.dirname(log_file)
        if directory:
            os.makedirs(directory, exist_ok=True)

        write_header = not os.path.exists(log_file) or os.path.getsize(log_file) == 0
        with open(log_file, "a", encoding="utf-8", newline="") as fp:
            fieldnames = ["email", "token", "status", "attempts", "timestamp", "error"]
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
