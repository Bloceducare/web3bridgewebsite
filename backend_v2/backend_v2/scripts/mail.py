import time
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from cohort.models import Participant


def send_bulk_email(subject, body, recipient_ids, from_admission=False):
    """
    Sends a single email to multiple recipients.
    
    Args:
        subject (str): Subject of the email
        body (str): General HTML content/message (no personalization)
        recipient_ids (list): List of participant IDs
        from_admission (bool): If True, sends from admission@web3bridge.com
    """
    # Choose email address based on parameter
    if from_admission:
        from_email = getattr(settings, 'ADMISSION_EMAIL_HOST_USER', 'admission@web3bridge.com')
    else:
        from_email = settings.EMAIL_HOST_USER

    # Fetch emails from participant IDs
    participants = Participant.objects.filter(id__in=recipient_ids).select_related('registration')
    recipient_emails = [p.email for p in participants]

    # General context (non-personalized)
    context = {
        'message_content': body,
        'subject': subject
    }

    # Render HTML once for all recipients
    html_content = render_to_string('cohort/custommail.html', context)

    # Construct email
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=from_email,
        to=[],  # No need to specify 'to' since we're using BCC
        bcc=recipient_emails,
    )
    email.content_subtype = 'html'  # Important! Tells Django to treat it as HTML

    # Use custom connection for admission emails if needed
    if from_admission and hasattr(settings, 'ADMISSION_EMAIL_HOST_USER') and hasattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'):
        from django.core.mail import get_connection
        connection = get_connection(
            host=getattr(settings, 'ADMISSION_EMAIL_HOST', settings.EMAIL_HOST),
            port=getattr(settings, 'ADMISSION_EMAIL_PORT', settings.EMAIL_PORT),
            username=getattr(settings, 'ADMISSION_EMAIL_HOST_USER'),
            password=getattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'),
            use_tls=getattr(settings, 'ADMISSION_EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
        )
        email.connection = connection

    # Send the email
    email.send(fail_silently=False)

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
    
    
