from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Testimonial image storage location
def testimonial_image_location(instance, filename):
    full_name_proceesed= instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Testimonial/{full_name_proceesed}/{filename}"

def send_registration_success_mail(email, course_id, participant):
    from cohort.models import Course
    try:
        course = Course.objects.get(pk=course_id)
        if course.id in [2, 3]:
            subject = 'Web2 Registration Success'
            template_name = 'cohort/web2_registration_email.html'
        elif course.id == 4:
            subject = 'Web3 Registration Success'
            template_name = 'cohort/web3_registration_email.html'
        else:
            subject = 'Other Registration Success'
            template_name = 'other_registration_email.html' 

        context = {'name': participant}
        message = render_to_string(template_name, context)

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, '', from_email, recipient_list, html_message=message, fail_silently=False)
    except Course.DoesNotExist:
        # Handle case where course with provided ID does not exist
        pass


def send_participant_details(email, course_id, participant):
    from cohort.models import Course

    try:
        course = Course.objects.get(pk=course_id)
        name= participant.get('name')
        email= participant.get('email')
        gender= participant.get('gender')
        github= participant.get('github')
        number= participant.get('number')
        wallet_address= participant.get('wallet_address')
        city= participant.get('city')
        state= participant.get('state')
        country= participant.get('country')
        duration= participant.get('duration')
        motivation= participant.get('motivation')
        achievement= participant.get('achievement')

        context = {'name': name, 'email': email, 'number': number, 'gender': gender, 'github': github,
                    'city': city, 'country': country, 'wallet': wallet_address, 'course_name': course.name,
                    'duration': duration, 'motivation': motivation, 'achievement': achievement,
                }
        message = render_to_string('cohort/participant_email.html', context)

        subject = 'Web3Bridge Registration Details'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, '', from_email, recipient_list, html_message=message, fail_silently=False)
    except Course.DoesNotExist:
        # Handle case where course with provided ID does not exist
        pass