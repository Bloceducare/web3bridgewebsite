from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Testimonial image storage location


def testimonial_image_location(instance, filename):
    full_name_processed = instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Testimonial/{full_name_processed}/{filename}"


def send_registration_success_mail(email, course_id, participant):
    from cohort.models import Course
    try:
        course = Course.objects.get(pk=course_id)
        print('course...', course)
        if "web2" in course.name.lower():
            subject = 'Web2 Registration Success'
            template_name = 'cohort/web2_registration_email.html'
        elif "web3" in course.name.lower():
            subject = 'Web3 Registration Success'
            template_name = 'cohort/web3_registration_email.html'
        elif "rust" in course.name.lower():
            subject = 'Rust Masterclass Registration Success'
            template_name = 'cohort/rust_registration_email.html'
        else:
            subject = f'{course.name} Registration Success'
            template_name = 'other_registration_email.html'

        context = {'name': participant}
        message = render_to_string(template_name, context)

        from_email = 'support@web3bridge.com'
        recipient_list = [email]

        send_mail(subject, '', from_email, recipient_list,
                  html_message=message, fail_silently=True)
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
        from_email = 'support@web3bridge.com'
        recipient_list = [email]

        send_mail(subject, '', from_email, recipient_list,
                  html_message=message, fail_silently=False)
    except Course.DoesNotExist:
        # Handle case where course with provided ID does not exist
        pass
