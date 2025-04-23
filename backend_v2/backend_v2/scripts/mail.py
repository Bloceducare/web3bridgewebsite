import time
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from cohort.models import Participant

def send_bulk_email(subject, body, recipients):
    from_email = settings.EMAIL_HOST_USER
    participants = Participant.objects.filter(id__in=recipients).select_related('registration')

    for count, participant in enumerate(participants, start=1):
        context = {
            'name': participant.name,
            'email': participant.email,
            'cohort': participant.cohort,
            'registration': participant.registration.name if participant.registration else None,
            'message_content': body,
            'subject': subject
        }

        personalized_html = render_to_string('cohort/custommail.html', context)

        send_mail(
            subject=subject,
            message='',
            html_message=personalized_html,
            from_email=from_email,
            recipient_list=[participant.email],
            fail_silently=False,
        )
        print(f"Email sent to {participant.email}")

        # Throttle: pause after every 50 emails
        if count % 50 == 0:
            time.sleep(60)  # Pause for 60 seconds
