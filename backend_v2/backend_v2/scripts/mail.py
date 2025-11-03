import time
import threading
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, get_connection
from django.template.loader import render_to_string
from cohort.models import Participant


def _send_email_batch(subject, html_content, recipient_emails_batch, from_email, from_admission=False):
    """
    Helper function to send emails to a batch of recipients.
    """
    batch_num = len(recipient_emails_batch)
    print(f"[EMAIL BATCH] Starting to send batch with {batch_num} recipients")
    print(f"[EMAIL BATCH] From: {from_email}, Admission: {from_admission}")
    print(f"[EMAIL BATCH] First 3 recipients: {recipient_emails_batch[:3]}")
    
    try:
        # Construct email
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=[],  # No need to specify 'to' since we're using BCC
            bcc=recipient_emails_batch,
        )
        email.content_subtype = 'html'  # Important! Tells Django to treat it as HTML

        # Use custom connection for admission emails if needed
        if from_admission and hasattr(settings, 'ADMISSION_EMAIL_HOST_USER') and hasattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'):
            print(f"[EMAIL BATCH] Using admission email connection")
            connection = get_connection(
                host=getattr(settings, 'ADMISSION_EMAIL_HOST', settings.EMAIL_HOST),
                port=getattr(settings, 'ADMISSION_EMAIL_PORT', settings.EMAIL_PORT),
                username=getattr(settings, 'ADMISSION_EMAIL_HOST_USER'),
                password=getattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'),
                use_tls=getattr(settings, 'ADMISSION_EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
            )
            email.connection = connection
            print(f"[EMAIL BATCH] Connection configured: host={getattr(settings, 'ADMISSION_EMAIL_HOST', settings.EMAIL_HOST)}, port={getattr(settings, 'ADMISSION_EMAIL_PORT', settings.EMAIL_PORT)}")
        else:
            print(f"[EMAIL BATCH] Using default email connection")

        # Send the email
        print(f"[EMAIL BATCH] Attempting to send email...")
        result = email.send(fail_silently=True)  # Don't raise exceptions to avoid breaking batch
        print(f"[EMAIL BATCH] Email send result: {result}")
        print(f"[EMAIL BATCH] Successfully sent batch to {batch_num} recipients")
    except Exception as e:
        # Log error but don't stop other batches
        print(f"[EMAIL BATCH] ERROR sending email batch: {str(e)}")
        import traceback
        print(f"[EMAIL BATCH] Traceback: {traceback.format_exc()}")


def send_bulk_email(subject, body, recipient_ids, from_admission=False):
    """
    Sends a single email to multiple recipients in batches to avoid timeouts.
    
    Args:
        subject (str): Subject of the email
        body (str): General HTML content/message (no personalization)
        recipient_ids (list): List of participant IDs
        from_admission (bool): If True, sends from admission@web3bridge.com
    """
    print(f"[BULK EMAIL] ========================================")
    print(f"[BULK EMAIL] Starting bulk email send")
    print(f"[BULK EMAIL] Subject: {subject}")
    print(f"[BULK EMAIL] Recipient IDs: {recipient_ids}")
    print(f"[BULK EMAIL] From admission: {from_admission}")
    print(f"[BULK EMAIL] Total recipient IDs: {len(recipient_ids)}")
    
    # Choose email address based on parameter
    if from_admission:
        from_email = getattr(settings, 'ADMISSION_EMAIL_HOST_USER', 'admission@web3bridge.com')
        print(f"[BULK EMAIL] From email (admission): {from_email}")
    else:
        from_email = getattr(settings, 'EMAIL_HOST_USER', 'default@web3bridge.com')
        print(f"[BULK EMAIL] From email (default): {from_email}")

    # Fetch emails from participant IDs - optimize query
    print(f"[BULK EMAIL] Fetching participants from database...")
    participants = Participant.objects.filter(id__in=recipient_ids).only('email', 'id')
    participant_count = participants.count()
    print(f"[BULK EMAIL] Found {participant_count} participants in database")
    
    recipient_emails = [p.email for p in participants if p.email]
    print(f"[BULK EMAIL] Valid emails found: {len(recipient_emails)}")
    print(f"[BULK EMAIL] First 5 emails: {recipient_emails[:5]}")

    if not recipient_emails:
        print("[BULK EMAIL] ERROR: No valid recipient emails found")
        print(f"[BULK EMAIL] Participants queried: {list(participants.values_list('id', 'email'))}")
        return

    # General context (non-personalized)
    context = {
        'message_content': body,
        'subject': subject
    }

    # Render HTML once for all recipients
    print(f"[BULK EMAIL] Rendering email template...")
    html_content = render_to_string('cohort/custommail.html', context)
    print(f"[BULK EMAIL] Template rendered, HTML length: {len(html_content)} characters")

    # Send in batches to avoid timeouts and SMTP limits
    # Most SMTP servers limit BCC recipients per email (typically 50-100)
    BATCH_SIZE = 50
    threads = []
    total_batches = (len(recipient_emails) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"[BULK EMAIL] Creating {total_batches} batches of size {BATCH_SIZE}")

    for i in range(0, len(recipient_emails), BATCH_SIZE):
        batch = recipient_emails[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        print(f"[BULK EMAIL] Creating thread for batch {batch_num}/{total_batches} ({len(batch)} recipients)")
        
        # Send each batch in a separate thread to avoid blocking
        thread = threading.Thread(
            target=_send_email_batch,
            args=(subject, html_content, batch, from_email, from_admission),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        print(f"[BULK EMAIL] Started thread for batch {batch_num}")
        
        # Small delay between batches to avoid overwhelming the SMTP server
        if i + BATCH_SIZE < len(recipient_emails):
            time.sleep(0.5)

    # Wait for all threads to complete (with timeout)
    print(f"[BULK EMAIL] Waiting for {len(threads)} threads to complete...")
    for idx, thread in enumerate(threads, 1):
        print(f"[BULK EMAIL] Waiting for thread {idx}/{len(threads)}...")
        thread.join(timeout=30)  # 30 second timeout per batch
        if thread.is_alive():
            print(f"[BULK EMAIL] WARNING: Thread {idx} timed out after 30 seconds")
        else:
            print(f"[BULK EMAIL] Thread {idx} completed successfully")
    
    print(f"[BULK EMAIL] ========================================")
    print(f"[BULK EMAIL] Bulk email process completed")

    # subject = 'Hello from Web3bridge'
    # context = {
    #     'message_content': """
    #         Hello,

    #         Again, we are thrilled to have received your application and looking forward to having you in the cohort. As we move closer to the closing dates of the application and move towards commencing the selection and onboarding phase of the cohort, we will be hosting a X (Twitter) space today Friday 31st May by 6PM GMT+1, to discuss the plans and journey to cohort XI.

    #         We will be explaining the plans for the cohort and taking all the questions you might have in relations to the cohort.

    #         Looking forward to seeing you on the call, use the link below to join set reminder and join the call. https://x.com/i/spaces/1OwGWYVAalAxQ
    #     """
    # }

    # # Fetch all participants
    # participants = Participant.objects.all()

    # for participant in participants:
    # participant_context = context.copy()
    # participant_contexts = [{'name': participant.name} for participant in participants]
    # Provide the template name and context to render_to_string
    # messages = [render_to_string(
    #     'cohort/custommail.html', context).format(**context) for _ in participants]

    # recipient_list = [participant.email for participant in participants]
    
    

def send_admission_bulk_email(subject, body, recipient_ids):
    """
    Convenience function to send bulk emails from admission@web3bridge.com
    """
    return send_bulk_email(subject, body, recipient_ids, from_admission=True)
    
    
