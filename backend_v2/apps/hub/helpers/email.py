from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_hub_registration_email(registration):
    """Send email when hub registration is received"""
    try:
        context = {
            'name': registration.name,
            'email': registration.email,
            'role': registration.role,
        }
        message = render_to_string('hub/registration_email.html', context)
        
        subject = 'Lagos Ethereum Community Hub - Registration Received'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [registration.email]
        
        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=True)
    except Exception as e:
        print(f"Error sending hub registration email: {str(e)}")
        pass


def send_hub_approval_email(registration):
    """Send email when hub registration is approved"""
    try:
        context = {
            'name': registration.name,
        }
        message = render_to_string('hub/approval_email.html', context)
        
        subject = 'Lagos Ethereum Community Hub - Registration Approved'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [registration.email]
        
        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=True)
    except Exception as e:
        print(f"Error sending hub approval email: {str(e)}")
        pass


def send_hub_rejection_email(registration):
    """Send email when hub registration is rejected"""
    try:
        context = {
            'name': registration.name,
            'notes': registration.notes,
        }
        message = render_to_string('hub/rejection_email.html', context)
        
        subject = 'Lagos Ethereum Community Hub - Registration Update'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [registration.email]
        
        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=True)
    except Exception as e:
        print(f"Error sending hub rejection email: {str(e)}")
        pass

