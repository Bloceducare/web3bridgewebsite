from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
import re
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import re

# Testimonial image storage location


def testimonial_image_location(instance, filename):
    full_name_processed = instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Testimonial/{full_name_processed}/{filename}"


def send_registration_success_mail(email, course_id, participant):
    from cohort.models import Course
    try:
        course = Course.objects.get(pk=course_id)
        name_lc = (course.name or "").lower()

        # Prioritize Rust, then Web2/Web3. Explicitly guard ZK from matching others.
        if re.search(r"\brust\b", name_lc):
            subject = 'Rust Masterclass Registration Success'
            template_name = 'cohort/rust_registration_email.html'
        elif re.search(r"\bweb2\b", name_lc):
            subject = 'Web2 Registration Success'
            template_name = 'cohort/web2_registration_email.html'
        elif re.search(r"\bweb3\b", name_lc):
            subject = 'Web3 Registration Success'
            template_name = 'cohort/web3_registration_email.html'
        elif re.search(r"\bzk\b|\bzero[- ]?knowledge\b", name_lc):
            subject = '🎉 Welcome to the Web3Bridge Zero Knowledge Program!'
            template_name = 'cohort/zk_registration_email.html'
        else:
            subject = f'{course.name} Registration Success'
            template_name = 'other_registration_email.html'

        context = {'name': participant}
        message = render_to_string(template_name, context)

        # Use admission email credentials if available, otherwise fall back to default
        from_email = getattr(settings, 'ADMISSION_EMAIL_HOST_USER', 'admission@web3bridge.com')
        recipient_list = [email]

        # Create EmailMessage for more control over SMTP settings
        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )
        email_msg.content_subtype = 'html'
        
        # Use admission SMTP settings if available
        if hasattr(settings, 'ADMISSION_EMAIL_HOST_USER') and hasattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'):
            # Use custom connection for admission emails
            from django.core.mail import get_connection
            connection = get_connection(
                host=getattr(settings, 'ADMISSION_EMAIL_HOST', settings.EMAIL_HOST),
                port=getattr(settings, 'ADMISSION_EMAIL_PORT', settings.EMAIL_PORT),
                username=getattr(settings, 'ADMISSION_EMAIL_HOST_USER'),
                password=getattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'),
                use_tls=getattr(settings, 'ADMISSION_EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
            )
            email_msg.connection = connection
        
        email_msg.send(fail_silently=True)
    except Course.DoesNotExist:
        # Handle case where course with provided ID does not exist
        pass


def send_participant_details(email, course_id, participant):
    from cohort.models import Course

    try:
        course = Course.objects.get(pk=course_id)
        name = participant.get('name')
        email = participant.get('email')
        number = participant.get('number')
        gender = participant.get('gender')
        github = participant.get('github')
        city = participant.get('city')
        state = participant.get('state')
        country = participant.get('country')
        duration = participant.get('duration')
        motivation = participant.get('motivation')
        achievement = participant.get('achievement')
        wallet_address = participant.get('wallet_address')
        venue = participant.get('venue')

        context = {
            'name': name, 'email': email, 'number': number, 'gender': gender,
            'city': city, 'state': state, 'country': country,
            'github': github, 'wallet': wallet_address, 'course_name': course.name,
            'duration': duration, 'motivation': motivation, 'achievement': achievement,
        }
        message = render_to_string('cohort/participant_email.html', context)

        subject = 'Web3Bridge Cohort Registration Details'
        from_email = getattr(settings, 'ADMISSION_EMAIL_HOST_USER', 'admission@web3bridge.com')
        recipient_list = [email]

        # Create EmailMessage for more control over SMTP settings
        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
        )
        email_msg.content_subtype = 'html'
        
        # Use admission SMTP settings if available
        if hasattr(settings, 'ADMISSION_EMAIL_HOST_USER') and hasattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'):
            # Use custom connection for admission emails
            from django.core.mail import get_connection
            connection = get_connection(
                host=getattr(settings, 'ADMISSION_EMAIL_HOST', settings.EMAIL_HOST),
                port=getattr(settings, 'ADMISSION_EMAIL_PORT', settings.EMAIL_PORT),
                username=getattr(settings, 'ADMISSION_EMAIL_HOST_USER'),
                password=getattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'),
                use_tls=getattr(settings, 'ADMISSION_EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
            )
            email_msg.connection = connection
        
        email_msg.send(fail_silently=False)
    except Course.DoesNotExist:
        # Handle case where course with provided ID does not exist
        pass


def send_approval_email(participant, payment_link: str | None = None):
    """
    Send approval emails by course. For ZK courses, include a payment link.
    """
    try:
        course_name = (participant.course.name or "")
        name_lc = course_name.lower()
        recipient_email = participant.email
        participant_name = participant.name

        # Detect ZK
        is_zk = bool(re.search(r"\bzk\b|\bzero[- ]?knowledge\b", name_lc))

        if is_zk:
            subject = "You’re Approved – Proceed to Payment (Web3Bridge ZK Program)"
            template_name = "cohort/zk_approval_email.html"
            link = payment_link or "https://payment.web3bridgeafrica.com"
            context = {"name": participant_name, "payment_link": link, "course_name": course_name}
        else:
            subject = f"You’re Approved for {course_name} – Next Steps"
            template_name = "cohort/approval_email.html"
            context = {"name": participant_name, "course_name": course_name}

        message = render_to_string(template_name, context)

        from_email = getattr(settings, 'ADMISSION_EMAIL_HOST_USER', 'admission@web3bridge.com')
        email_msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[recipient_email],
        )
        email_msg.content_subtype = 'html'

        # Use admission SMTP settings if available
        if hasattr(settings, 'ADMISSION_EMAIL_HOST_USER') and hasattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'):
            from django.core.mail import get_connection
            connection = get_connection(
                host=getattr(settings, 'ADMISSION_EMAIL_HOST', settings.EMAIL_HOST),
                port=getattr(settings, 'ADMISSION_EMAIL_PORT', settings.EMAIL_PORT),
                username=getattr(settings, 'ADMISSION_EMAIL_HOST_USER'),
                password=getattr(settings, 'ADMISSION_EMAIL_HOST_PASSWORD'),
                use_tls=getattr(settings, 'ADMISSION_EMAIL_USE_TLS', settings.EMAIL_USE_TLS),
            )
            email_msg.connection = connection

        email_msg.send(fail_silently=True)
    except Exception:
        pass
