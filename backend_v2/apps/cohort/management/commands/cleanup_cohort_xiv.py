"""
Django management command to cleanup Web3 Cohort XIV participants.

This script:
1. Reads a CSV file with approved participants
2. Finds all participants in "web3 cohort XIV" 
3. Rejects those NOT in the approved list (sets status to REJECTED)
4. Updates status of those IN the list to ACCEPTED
5. Logs rejected participants to a backup CSV file
"""

import csv
import json
import os
from django.core.management.base import BaseCommand
from django.db.models import Q
from cohort.models import Participant
from utils.enums.models import RegistrationStatus


class Command(BaseCommand):
    help = 'Cleanup Web3 Cohort XIV participants - reject those not in approved list and approve those in list'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            default='list.csv',
            help='Path to CSV file with approved participants (default: list.csv)'
        )
        parser.add_argument(
            '--backup-file',
            type=str,
            default='rejected_participants_backup.csv',
            help='Path to backup CSV file for rejected participants (default: rejected_participants_backup.csv)'
        )
        parser.add_argument(
            '--cohort-name',
            type=str,
            default='web3 cohort XIV',
            help='Cohort name to filter by (default: web3 cohort XIV)'
        )
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Skip confirmation and proceed with rejection'
        )
        parser.add_argument(
            '--export-json',
            type=str,
            default=None,
            help='Export full participant objects to JSON file before rejection (optional)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        backup_file = options['backup_file']
        cohort_name = options['cohort_name']
        skip_confirmation = options['yes']
        export_json = options.get('export_json')

        # Resolve paths - if relative, assume they're relative to current working directory
        # (which should be the project root where manage.py is)
        if not os.path.isabs(csv_file):
            csv_file = os.path.abspath(csv_file)
        
        if not os.path.isabs(backup_file):
            backup_file = os.path.abspath(backup_file)

        # Read approved emails from CSV
        self.stdout.write(self.style.SUCCESS(f'Reading approved participants from {csv_file}...'))
        approved_emails = self.read_approved_emails(csv_file)
        self.stdout.write(self.style.SUCCESS(f'Found {len(approved_emails)} approved participants in CSV'))

        # Find all participants in the cohort (case-insensitive)
        # Only match "web3 cohort XIV" variations, NOT "web2 cohort XIV"
        self.stdout.write(self.style.SUCCESS(f'Finding participants in cohort: {cohort_name}...'))
        cohort_participants = Participant.objects.filter(
            # Must contain "web3" (case-insensitive) AND "cohort xiv" (case-insensitive)
            Q(cohort__icontains='web3') & Q(cohort__icontains='cohort xiv')
        ).exclude(
            # Explicitly exclude web2 variations
            Q(cohort__icontains='web2')
        ).select_related('course', 'registration')

        total_cohort = cohort_participants.count()
        self.stdout.write(self.style.SUCCESS(f'Found {total_cohort} total participants in cohort'))

        # Separate participants into: to_approve and to_reject
        to_approve = []
        to_reject = []

        for participant in cohort_participants:
            email_lower = participant.email.lower().strip()
            if email_lower in approved_emails:
                to_approve.append(participant)
            else:
                to_reject.append(participant)

        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(self.style.SUCCESS(f'  - Participants to APPROVE: {len(to_approve)}'))
        self.stdout.write(self.style.WARNING(f'  - Participants to REJECT: {len(to_reject)}'))

        # Show participants to be rejected with full details
        if to_reject:
            self.stdout.write(self.style.WARNING(f'\n{"="*80}'))
            self.stdout.write(self.style.WARNING(f'PARTICIPANTS TO BE REJECTED ({len(to_reject)})'))
            self.stdout.write(self.style.WARNING(f'{"="*80}'))
            for idx, participant in enumerate(to_reject, 1):
                self.stdout.write(f'\n{"-"*80}')
                self.stdout.write(self.style.WARNING(f'{idx}. {participant.name} ({participant.email})'))
                self.stdout.write(f'   ID: {participant.id}')
                self.stdout.write(f'   Cohort: {participant.cohort}')
                self.stdout.write(f'   Status: {participant.status}')
                self.stdout.write(f'   Course: {participant.course.name if participant.course else "N/A"}')
                self.stdout.write(f'   Registration: {participant.registration.name if participant.registration else "N/A"}')
                self.stdout.write(f'   Created: {participant.created_at}')
                self.stdout.write(f'   Updated: {participant.updated_at}')
                self.stdout.write(f'   Wallet Address: {participant.wallet_address}')
                self.stdout.write(f'   City: {participant.city or "N/A"}, State: {participant.state or "N/A"}, Country: {participant.country or "N/A"}')
                self.stdout.write(f'   Phone: {participant.number or "N/A"}')
                self.stdout.write(f'   Gender: {participant.gender or "N/A"}')
                self.stdout.write(f'   GitHub: {participant.github or "N/A"}')
                self.stdout.write(f'   Venue: {participant.venue or "N/A"}')
                self.stdout.write(f'   Payment Status: {participant.payment_status}')
                if participant.motivation:
                    motivation_preview = participant.motivation[:100] + '...' if len(participant.motivation) > 100 else participant.motivation
                    self.stdout.write(f'   Motivation: {motivation_preview}')
                if participant.achievement:
                    achievement_preview = participant.achievement[:100] + '...' if len(participant.achievement) > 100 else participant.achievement
                    self.stdout.write(f'   Achievement: {achievement_preview}')

            # Show participants to be approved
            if to_approve:
                self.stdout.write(self.style.SUCCESS(f'\n=== PARTICIPANTS TO BE APPROVED ({len(to_approve)}) ==='))
                for idx, participant in enumerate(to_approve[:10], 1):  # Show first 10
                    self.stdout.write(f'{idx}. {participant.name} ({participant.email})')
                if len(to_approve) > 10:
                    self.stdout.write(f'... and {len(to_approve) - 10} more')

            # Export to JSON if requested
            if export_json:
                self.export_participants_to_json(to_reject, export_json)
                self.stdout.write(self.style.SUCCESS(f'✓ Full participant data exported to {export_json}'))

            # Confirmation
            if not skip_confirmation:
                self.stdout.write(self.style.WARNING('\n⚠️  WARNING: This will REJECT the participants listed above!'))
                confirm = input('\nType "yes" to proceed with rejection: ')
                if confirm.lower() != 'yes':
                    self.stdout.write(self.style.ERROR('Operation cancelled.'))
                    return

        # Proceed with rejection and approval
        if to_reject:
            self.stdout.write(self.style.WARNING(f'\nRejecting {len(to_reject)} participants...'))
            rejected_data = self.reject_participants(to_reject, backup_file)
            self.stdout.write(self.style.SUCCESS(f'✓ Rejected {len(rejected_data)} participants'))
            self.stdout.write(self.style.SUCCESS(f'✓ Backup saved to {backup_file}'))
        else:
            self.stdout.write(self.style.SUCCESS('No participants to reject.'))

        if to_approve:
            self.stdout.write(self.style.SUCCESS(f'\nApproving {len(to_approve)} participants...'))
            approved_count = self.approve_participants(to_approve)
            self.stdout.write(self.style.SUCCESS(f'✓ Approved {approved_count} participants'))
        else:
            self.stdout.write(self.style.WARNING('No participants to approve.'))

        self.stdout.write(self.style.SUCCESS('\n✓ Operation completed successfully!'))

    def read_approved_emails(self, csv_file):
        """Read approved email addresses from CSV file"""
        approved_emails = set()
        
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get('Email Address', '').strip()
                if email:
                    approved_emails.add(email.lower())

        return approved_emails

    def reject_participants(self, participants, backup_file):
        """Reject participants (set status to REJECTED) and save backup to CSV"""
        rejected_data = []

        # Prepare backup data
        for participant in participants:
            rejected_data.append({
                'id': participant.id,
                'name': participant.name,
                'email': participant.email,
                'cohort': participant.cohort,
                'old_status': participant.status,
                'new_status': RegistrationStatus.REJECTED.value,
                'course': participant.course.name if participant.course else '',
                'registration': participant.registration.name if participant.registration else '',
                'wallet_address': participant.wallet_address,
                'city': participant.city or '',
                'state': participant.state or '',
                'country': participant.country or '',
                'gender': participant.gender or '',
                'github': participant.github or '',
                'number': participant.number or '',
                'venue': participant.venue or '',
                'motivation': participant.motivation or '',
                'achievement': participant.achievement or '',
                'payment_status': participant.payment_status,
                'created_at': participant.created_at.isoformat() if participant.created_at else '',
                'updated_at': participant.updated_at.isoformat() if participant.updated_at else '',
            })

        # Write backup CSV
        if rejected_data:
            os.makedirs(os.path.dirname(backup_file) if os.path.dirname(backup_file) else '.', exist_ok=True)
            with open(backup_file, 'w', encoding='utf-8', newline='') as f:
                if rejected_data:
                    writer = csv.DictWriter(f, fieldnames=rejected_data[0].keys())
                    writer.writeheader()
                    writer.writerows(rejected_data)

        # Update status to REJECTED
        for participant in participants:
            participant.status = RegistrationStatus.REJECTED.value
            participant.save()

        return rejected_data

    def approve_participants(self, participants):
        """Update participant status to ACCEPTED"""
        count = 0
        for participant in participants:
            participant.status = RegistrationStatus.ACCEPTED.value
            participant.save()
            count += 1
        return count

    def export_participants_to_json(self, participants, json_file):
        """Export full participant objects to JSON file"""
        participants_data = []
        for participant in participants:
            participant_dict = {
                'id': participant.id,
                'name': participant.name,
                'email': participant.email,
                'cohort': participant.cohort,
                'status': participant.status,
                'wallet_address': participant.wallet_address,
                'city': participant.city,
                'state': participant.state,
                'country': participant.country,
                'gender': participant.gender,
                'github': participant.github,
                'number': participant.number,
                'venue': participant.venue,
                'motivation': participant.motivation,
                'achievement': participant.achievement,
                'payment_status': participant.payment_status,
                'created_at': participant.created_at.isoformat() if participant.created_at else None,
                'updated_at': participant.updated_at.isoformat() if participant.updated_at else None,
                'course': {
                    'id': participant.course.id if participant.course else None,
                    'name': participant.course.name if participant.course else None,
                } if participant.course else None,
                'registration': {
                    'id': participant.registration.id if participant.registration else None,
                    'name': participant.registration.name if participant.registration else None,
                } if participant.registration else None,
            }
            participants_data.append(participant_dict)

        # Resolve path if relative
        if not os.path.isabs(json_file):
            json_file = os.path.abspath(json_file)

        os.makedirs(os.path.dirname(json_file) if os.path.dirname(json_file) else '.', exist_ok=True)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(participants_data, f, indent=2, ensure_ascii=False)

