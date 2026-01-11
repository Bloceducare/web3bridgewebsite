"""
Django management command to send Discord access emails to paid Web2 participants.

This script:
1. Finds all paid Web2 participants (payment_status=True, cohort contains 'web2', excludes 'web3')
2. Sends personalized email with their wallet address
3. Only sends to participants with valid email and wallet address
4. Tracks sent/failed emails and saves to CSV
"""

import time
import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings
from cohort.models import Participant


class Command(BaseCommand):
    help = 'Send Discord access emails to all paid Web2 participants'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=20,
            help='Number of emails to send per batch (default: 20, optimized for Gmail)'
        )
        parser.add_argument(
            '--delay-between-emails',
            type=float,
            default=2.0,
            help='Delay in seconds between individual emails (default: 2.0 for Gmail rate limits)'
        )
        parser.add_argument(
            '--delay-between-batches',
            type=float,
            default=10.0,
            help='Delay in seconds between batches (default: 10.0 for Gmail rate limits)'
        )
        parser.add_argument(
            '--max-retries',
            type=int,
            default=3,
            help='Maximum number of retries for failed emails (default: 3)'
        )
        parser.add_argument(
            '--cohort-filter',
            type=str,
            default='cohort xiv',
            help='Cohort filter (default: cohort xiv)'
        )
        parser.add_argument(
            '--test-emails',
            type=str,
            default=None,
            help='Comma-separated list of test email addresses to send to (e.g., "email1@example.com,email2@example.com")'
        )
        parser.add_argument(
            '--log-file',
            type=str,
            default='web2_discord_email_log.csv',
            help='CSV file to log sent/failed emails (default: web2_discord_email_log.csv)'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        batch_size = options['batch_size']
        test_emails = options['test_emails']
        log_file = options['log_file']
        delay_between_emails = options['delay_between_emails']
        delay_between_batches = options['delay_between_batches']
        max_retries = options['max_retries']
        
        # Resolve log file path
        if not os.path.isabs(log_file):
            log_file = os.path.abspath(log_file)

        # If test emails provided, use those instead
        if test_emails:
            test_email_list = [email.strip() for email in test_emails.split(',') if email.strip()]
            self.stdout.write(self.style.SUCCESS(f'Test mode: Sending to {len(test_email_list)} specific emails'))
            self.stdout.write(self.style.SUCCESS(f'Test emails: {", ".join(test_email_list)}'))
            
            # STRICT: Only find paid Web2 Cohort XIV participants
            web2_participants = Participant.objects.filter(
                email__in=test_email_list,
                payment_status=True,  # MUST BE PAID
                wallet_address__isnull=False,
            ).exclude(
                wallet_address=''
            ).filter(
                # Must contain 'web2' AND 'cohort xiv' (case-insensitive)
                Q(cohort__icontains='web2') & Q(cohort__icontains='cohort xiv')
            ).exclude(
                # Explicitly exclude web3 variations
                Q(cohort__icontains='web3')
            ).exclude(
                # Exclude other cohorts
                Q(cohort__icontains='master') |
                Q(cohort__icontains='Master') |
                Q(cohort__icontains='rust') |
                Q(cohort__icontains='Rust') |
                Q(cohort__icontains='zk') |
                Q(cohort__icontains='ZK') |
                Q(cohort__icontains='zero knowledge')
            )
            
            # Check which emails have participants
            found_emails = set(web2_participants.values_list('email', flat=True))
            missing_emails = set(test_email_list) - found_emails
            
            # Create temp participant objects for missing emails
            participants_list = list(web2_participants)
            if missing_emails:
                self.stdout.write(self.style.WARNING(f'Note: {len(missing_emails)} emails not found in database, will use placeholder wallet'))
                
                class TempParticipant:
                    def __init__(self, email, wallet, name):
                        self.email = email
                        self.wallet_address = wallet
                        self.name = name
                
                for email in missing_emails:
                    # Try to find any participant with this email to get wallet
                    any_participant = Participant.objects.filter(email__iexact=email).first()
                    if any_participant and any_participant.wallet_address:
                        wallet = any_participant.wallet_address
                        name = any_participant.name
                    else:
                        wallet = '0x0000000000000000000000000000000000000000'  # Placeholder
                        name = email.split('@')[0]  # Use email prefix as name
                    
                    participants_list.append(TempParticipant(email, wallet, name))
            
            total_participants = len(participants_list)
        else:
            # Find all paid Web2 Cohort XIV participants ONLY
            # Must be EXACTLY "web2 cohort xiv" variations, nothing else
            self.stdout.write(self.style.SUCCESS('Finding paid Web2 Cohort XIV participants ONLY...'))
            
            web2_participants = Participant.objects.filter(
                payment_status=True,
                email__isnull=False,
                wallet_address__isnull=False,
            ).exclude(
                email=''
            ).exclude(
                wallet_address=''
            ).filter(
                # Must contain 'web2' AND 'cohort xiv' (case-insensitive)
                Q(cohort__icontains='web2') & Q(cohort__icontains='cohort xiv')
            ).exclude(
                # Explicitly exclude web3 variations
                Q(cohort__icontains='web3')
            ).exclude(
                # Exclude other cohorts that might match
                Q(cohort__icontains='master') |
                Q(cohort__icontains='Master') |
                Q(cohort__icontains='rust') |
                Q(cohort__icontains='Rust') |
                Q(cohort__icontains='zk') |
                Q(cohort__icontains='ZK') |
                Q(cohort__icontains='zero knowledge')
            )

            total_participants = web2_participants.count()
            participants_list = list(web2_participants)

        self.stdout.write(self.style.SUCCESS(f'Found {total_participants} participants'))

        if total_participants == 0:
            self.stdout.write(self.style.WARNING('No participants found. Exiting.'))
            return

        # Show preview
        self.stdout.write(self.style.SUCCESS('\n=== Preview ==='))
        for idx, participant in enumerate(participants_list[:10], 1):
            self.stdout.write(f'{idx}. {participant.name} ({participant.email})')
            self.stdout.write(f'   Wallet: {participant.wallet_address}')
            if hasattr(participant, 'cohort'):
                self.stdout.write(f'   Cohort: {participant.cohort}')
        
        if total_participants > 10:
            self.stdout.write(f'... and {total_participants - 10} more')

        if dry_run:
            self.stdout.write(self.style.WARNING('\n=== DRY RUN MODE - No emails will be sent ==='))
            self.stdout.write(self.style.SUCCESS(f'Would send {total_participants} emails'))
            return

        # Confirmation
        self.stdout.write(self.style.WARNING(f'\n⚠️  About to send {total_participants} emails'))
        confirm = input('Type "yes" to proceed: ')
        if confirm.lower() != 'yes':
            self.stdout.write(self.style.ERROR('Operation cancelled.'))
            return

        # Send emails in batches with tracking
        self.stdout.write(self.style.SUCCESS(f'\nSending emails in batches of {batch_size}...'))
        self.stdout.write(self.style.SUCCESS(f'Delays: {delay_between_emails}s between emails, {delay_between_batches}s between batches'))
        self.stdout.write(self.style.SUCCESS(f'Max retries: {max_retries}'))
        
        # Tracking lists
        sent_participants = []
        failed_participants = []
        
        total_batches = (len(participants_list) + batch_size - 1) // batch_size
        
        for i in range(0, len(participants_list), batch_size):
            batch = participants_list[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            self.stdout.write(f'\n{"="*80}')
            self.stdout.write(f'Processing batch {batch_num}/{total_batches} ({len(batch)} participants)...')
            self.stdout.write(f'{"="*80}')
            
            for idx, participant in enumerate(batch, 1):
                email_sent = False
                last_error = None
                
                # Retry logic
                for attempt in range(1, max_retries + 1):
                    try:
                        success = self.send_email_to_participant(participant)
                        if success:
                            sent_participants.append({
                                'email': participant.email,
                                'name': getattr(participant, 'name', 'N/A'),
                                'wallet': participant.wallet_address,
                                'status': 'SUCCESS',
                                'attempt': attempt,
                                'timestamp': datetime.now().isoformat(),
                                'error': None
                            })
                            self.stdout.write(self.style.SUCCESS(f'  [{idx}/{len(batch)}] ✓ Sent to: {participant.email} (attempt {attempt})'))
                            email_sent = True
                            break
                        else:
                            last_error = "Email send returned False"
                    except Exception as e:
                        last_error = str(e)
                        if attempt < max_retries:
                            wait_time = attempt * 2  # Exponential backoff
                            self.stdout.write(self.style.WARNING(f'  [{idx}/{len(batch)}] ⚠ Retry {attempt}/{max_retries} for {participant.email} after {wait_time}s...'))
                            time.sleep(wait_time)
                        else:
                            self.stdout.write(self.style.ERROR(f'  [{idx}/{len(batch)}] ✗ Failed after {max_retries} attempts: {participant.email}'))
                
                if not email_sent:
                    failed_participants.append({
                        'email': participant.email,
                        'name': getattr(participant, 'name', 'N/A'),
                        'wallet': participant.wallet_address,
                        'status': 'FAILED',
                        'attempts': max_retries,
                        'timestamp': datetime.now().isoformat(),
                        'error': last_error
                    })
                
                # Delay between emails (Gmail rate limit: ~20-50 emails per minute)
                if idx < len(batch):  # Don't delay after last email in batch
                    time.sleep(delay_between_emails)
            
            # Delay between batches (important for Gmail)
            if i + batch_size < len(participants_list):
                self.stdout.write(self.style.SUCCESS(f'\nBatch {batch_num} completed. Waiting {delay_between_batches}s before next batch...'))
                time.sleep(delay_between_batches)

        # Save results to CSV
        self.save_results_to_csv(log_file, sent_participants, failed_participants)
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n{"="*80}'))
        self.stdout.write(self.style.SUCCESS(f'✓ SUMMARY'))
        self.stdout.write(self.style.SUCCESS(f'{"="*80}'))
        self.stdout.write(self.style.SUCCESS(f'  - Total participants: {len(participants_list)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Emails sent successfully: {len(sent_participants)}'))
        if failed_participants:
            self.stdout.write(self.style.ERROR(f'  - Failed: {len(failed_participants)}'))
            self.stdout.write(self.style.WARNING(f'\nFailed emails:'))
            for failed in failed_participants:
                self.stdout.write(self.style.ERROR(f'    - {failed["email"]}: {failed["error"]}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'  - Failed: 0 (100% success rate!)'))
        self.stdout.write(self.style.SUCCESS(f'\n✓ Results saved to: {log_file}'))
        self.stdout.write(self.style.SUCCESS('✓ Operation completed!'))

    def send_email_to_participant(self, participant):
        """Send personalized Discord access email to a participant"""
        try:
            # Get name - handle both regular participants and temp participants
            name = getattr(participant, 'name', None) or participant.email.split('@')[0]
            
            # Prepare context
            context = {
                'name': name,
                'wallet_address': participant.wallet_address,
            }

            # Render email template
            html_content = render_to_string('cohort/web2_discord_access_email.html', context)

            # Email settings
            subject = 'Discord Access - Web3Bridge Web2 Cohort'
            from_email = getattr(settings, 'ADMISSION_EMAIL_HOST_USER', 'admission@web3bridge.com')
            
            # Create email message
            email_msg = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=from_email,
                to=[participant.email],
            )
            email_msg.content_subtype = 'html'

            # Use admission SMTP settings if available
            if hasattr(settings, 'ADMISSION_EMAIL_HOST_USER') and hasattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'):
                connection = get_connection(
                    host=getattr(settings, 'ADMISSION_EMAIL_HOST', settings.EMAIL_HOST),
                    port=getattr(settings, 'ADMISSION_EMAIL_PORT', settings.EMAIL_PORT),
                    username=getattr(settings, 'ADMISSION_EMAIL_HOST_USER'),
                    password=getattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'),
                    use_tls=getattr(settings, 'ADMISSION_EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
                )
                email_msg.connection = connection

            # Send email
            email_msg.send(fail_silently=False)
            return True

        except Exception as e:
            # Don't print here, let the caller handle it
            raise e

    def save_results_to_csv(self, log_file, sent_participants, failed_participants):
        """Save email sending results to CSV file"""
        all_results = sent_participants + failed_participants
        
        if not all_results:
            return
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else '.', exist_ok=True)
        
        # Write to CSV
        with open(log_file, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['email', 'name', 'wallet', 'status', 'attempts', 'timestamp', 'error']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in all_results:
                writer.writerow({
                    'email': result['email'],
                    'name': result['name'],
                    'wallet': result['wallet'],
                    'status': result['status'],
                    'attempts': result.get('attempt', result.get('attempts', 1)),
                    'timestamp': result['timestamp'],
                    'error': result.get('error', '')
                })

