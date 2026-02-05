
from django.core.mail import EmailMessage
from django.conf import settings

def send_hub_registration_email(registration):
    """
    Sends an email to admins whenever a new hub registration occurs.
    """

    # Email subject
    subject = f"New Hub Registration: {registration.name}"

    # Email body
    body = f"""
Hello Admin,

A new hub registration has been submitted. Details:

Name: {registration.name}
Email: {registration.email}
Phone: {registration.phone}
Organization: {getattr(registration, 'organization', 'N/A')}
Role/Position: {getattr(registration, 'role', 'N/A')}
Additional Info: {getattr(registration, 'other_info', 'N/A')}

Registration ID: {registration.id}
Registered At: {registration.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""

    # List of admin emails
    admin_emails = [
        "support@web3bridge.com"
    ]

    # Create and send the email
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=admin_emails,
    )

    try:
        email.send(fail_silently=False)
        print(f"Hub registration email sent to admins for registration ID {registration.id}")
    except Exception as e:
        print(f"Error sending hub registration email: {str(e)}")