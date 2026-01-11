"""
Django management command to load approved Web3 or ZK Cohort XIV participants from CSV.

This script:
1. Reads a CSV file with approved participants
2. Creates/updates ApprovedWeb3Participant records (works for both Web3 and ZK)
3. Links them to existing Participant records or creates new ones
4. Handles participants from previous cohorts by creating normalized records
5. Auto-detects cohort type (Web3 or ZK) from cohort name or course name
"""

import csv
import os
from django.core.management.base import BaseCommand
from django.db.models import Q
from cohort.models import ApprovedWeb3Participant, Participant, Registration, Course
from utils.enums.models import RegistrationStatus


class Command(BaseCommand):
    help = 'Load approved Web3 or ZK Cohort XIV participants from CSV into ApprovedWeb3Participant table'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            default='list.csv',
            help='Path to CSV file with approved participants (default: list.csv)'
        )
        parser.add_argument(
            '--cohort-name',
            type=str,
            default=None,
            help='Cohort name (e.g., "web3 cohort XIV" or "zk cohort XIV"). Auto-detected if not provided.'
        )
        parser.add_argument(
            '--cohort-type',
            type=str,
            choices=['web3', 'zk', 'auto'],
            default='auto',
            help='Cohort type: web3, zk, or auto-detect (default: auto)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing approved participants before loading'
        )
        parser.add_argument(
            '--link-participants',
            action='store_true',
            default=True,
            help='Try to link to existing Participant records by email (default: True)'
        )
        parser.add_argument(
            '--create-participants',
            action='store_true',
            help='Create new Participant records for approved participants if they don\'t exist or are from other cohorts'
        )
        parser.add_argument(
            '--course-name',
            type=str,
            default=None,
            help='Course name (auto-detected if not provided: "Solidity (Web3 Development)" for web3, "Zero Knowledge" for zk)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        cohort_name = options['cohort_name']
        cohort_type = options['cohort_type']
        clear_existing = options['clear']
        link_participants = options['link_participants']
        create_participants = options['create_participants']
        course_name = options['course_name']

        # Resolve path
        if not os.path.isabs(csv_file):
            csv_file = os.path.abspath(csv_file)

        # Only setup registration/course if we need to create participants
        registration = None
        course = None
        
        # Set default cohort_name if not provided
        if not cohort_name:
            cohort_name = 'web3 cohort XIV'  # Default, can be overridden
        
        if create_participants:
            # Auto-detect cohort type and name if not provided
            if cohort_type == 'auto' or not cohort_name:
                # Try to detect from CSV or default to web3
                if not cohort_name:
                    # Default based on type or default to web3
                    if cohort_type == 'zk':
                        cohort_name = 'zk cohort XIV'
                    else:
                        cohort_name = 'web3 cohort XIV'
                
                # Auto-detect type from cohort name
                cohort_name_lower = cohort_name.lower()
                if 'zk' in cohort_name_lower or 'zero knowledge' in cohort_name_lower:
                    detected_type = 'zk'
                elif 'web3' in cohort_name_lower:
                    detected_type = 'web3'
                else:
                    detected_type = 'web3'  # Default
            else:
                detected_type = cohort_type if cohort_type != 'auto' else 'web3'

            self.stdout.write(self.style.SUCCESS(f'Detected cohort type: {detected_type.upper()}'))
            self.stdout.write(self.style.SUCCESS(f'Using cohort name: {cohort_name}'))

            # Get or create Registration (only if creating participants)
            registration = Registration.objects.filter(
                Q(name__iexact=cohort_name) | 
                (Q(name__icontains=detected_type) & Q(name__icontains='xiv'))
            ).first()
            
            if not registration:
                registration = Registration.objects.create(
                    name=cohort_name,
                    is_open=False,
                    cohort='Cohort-XIV'
                )
                self.stdout.write(self.style.SUCCESS(f'Created registration: {cohort_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Found registration: {registration.name}'))

            # Get or find Course - auto-detect if not provided
            if course_name:
                course = Course.objects.filter(name__icontains=course_name).first()
            
            if not course:
                # Auto-detect course based on type
                if detected_type == 'zk':
                    # Look for ZK course
                    course = Course.objects.filter(
                        Q(name__icontains='zk') | Q(name__icontains='zero knowledge')
                    ).exclude(
                        Q(name__icontains='rust')
                    ).first()
                    if not course and registration:
                        course = Course.objects.filter(registration=registration).filter(
                            Q(name__icontains='zk') | Q(name__icontains='zero knowledge')
                        ).first()
                else:
                    # Look for Web3 course
                    course = Course.objects.filter(
                        Q(name__icontains='web3') | Q(name__icontains='solidity')
                    ).exclude(
                        Q(name__icontains='web2')
                    ).first()
                    if not course and registration:
                        course = Course.objects.filter(registration=registration).filter(
                            Q(name__icontains='web3') | Q(name__icontains='solidity')
                        ).first()
            
            if course:
                self.stdout.write(self.style.SUCCESS(f'Found course: {course.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Warning: Could not find course. Participant records may be created without course.'))

        # Clear existing if requested
        if clear_existing:
            deleted_count = ApprovedWeb3Participant.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f'Cleared {deleted_count} existing approved participants'))

        # Read CSV
        self.stdout.write(self.style.SUCCESS(f'Reading approved participants from {csv_file}...'))
        approved_data = self.read_csv(csv_file)
        self.stdout.write(self.style.SUCCESS(f'Found {len(approved_data)} approved participants in CSV'))
        self.stdout.write(self.style.SUCCESS(f'\nProcessing participants...\n'))

        # Process each participant
        created_count = 0
        updated_count = 0
        skipped_count = 0
        linked_count = 0
        participant_created_count = 0
        participant_updated_count = 0

        for row in approved_data:
            email = row['email'].lower().strip()
            name = row.get('name', '').strip()
            
            if not email:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'  ⚠ Skipping row - no email found'))
                continue

            # Simply find participant by email (no cohort checking)
            participant = None
            existing_participant = Participant.objects.filter(email__iexact=email).first()
            
            if existing_participant:
                # Use existing participant regardless of cohort
                participant = existing_participant
                linked_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Found existing participant: {email}'))
            elif create_participants:
                # No participant exists - create new one
                participant = self.create_new_participant(
                    email, name, cohort_name, registration, course
                )
                participant_created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created new participant: {email}'))
            else:
                # No participant and not creating - will link later if found
                self.stdout.write(self.style.WARNING(f'  ⚠ No participant found for {email} (use --create-participants to create)'))

            # Create or update ApprovedWeb3Participant (just based on email from list)
            approved_participant, created = ApprovedWeb3Participant.objects.update_or_create(
                email=email,
                defaults={
                    'participant': participant,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created ApprovedWeb3Participant: {email}'))
            else:
                updated_count += 1
                if approved_participant.participant != participant:
                    approved_participant.participant = participant
                    approved_participant.save()
                    participant_updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated ApprovedWeb3Participant: {email}'))

        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n✓ Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  - ApprovedWeb3Participant created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  - ApprovedWeb3Participant updated: {updated_count}'))
        if link_participants:
            self.stdout.write(self.style.SUCCESS(f'  - Linked to existing Participant records: {linked_count}'))
        if create_participants:
            self.stdout.write(self.style.SUCCESS(f'  - New Participant records created: {participant_created_count}'))
            self.stdout.write(self.style.SUCCESS(f'  - Participant links updated: {participant_updated_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'  - Skipped (no email): {skipped_count}'))
        
        total_approved = ApprovedWeb3Participant.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\n✓ Total approved participants in database: {total_approved}'))
        self.stdout.write(self.style.SUCCESS('✓ Operation completed successfully!'))

    def read_csv(self, csv_file):
        """Read approved participants from CSV file - handles multiple column name formats"""
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        approved_data = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Try multiple possible column names for email
                email = (
                    row.get('email', '').strip() or 
                    row.get('Email Address', '').strip() or
                    row.get('Email', '').strip() or
                    row.get('email address', '').strip()
                )
                
                # Try multiple possible column names for name
                name = (
                    row.get('name', '').strip() or
                    row.get('Full Name', '').strip() or
                    row.get('Name', '').strip() or
                    row.get('full name', '').strip()
                )
                
                if email:
                    approved_data.append({
                        'email': email,
                        'name': name,
                        'row': row  # Keep full row for potential future use
                    })

        return approved_data

    def create_normalized_participant(self, old_participant, email, name, cohort_name, registration, course):
        """Create a new participant record normalized for web3 cohort XIV"""
        # Use data from old participant but update cohort/course/registration
        new_participant = Participant.objects.create(
            name=name or old_participant.name,
            email=email,
            wallet_address=old_participant.wallet_address,
            registration=registration,
            status=RegistrationStatus.PENDING.value,  # Will be updated to ACCEPTED later
            motivation=old_participant.motivation or '',
            achievement=old_participant.achievement or '',
            city=old_participant.city,
            state=old_participant.state,
            country=old_participant.country,
            gender=old_participant.gender,
            github=old_participant.github or '',
            number=old_participant.number or '',
            course=course,
            cohort=cohort_name,
            payment_status=old_participant.payment_status,
            venue=old_participant.venue or 'online',
        )
        return new_participant

    def create_new_participant(self, email, name, cohort_name, registration, course):
        """Create a new participant record from scratch"""
        new_participant = Participant.objects.create(
            name=name or '',
            email=email,
            wallet_address='',  # Will need to be filled later
            registration=registration,
            status=RegistrationStatus.PENDING.value,
            motivation='',
            achievement='',
            course=course,
            cohort=cohort_name,
            payment_status=False,
            venue='online',
        )
        return new_participant

