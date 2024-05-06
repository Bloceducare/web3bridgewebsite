from django.conf import settings
from django.core.mail import send_mail

# Testimonial image storage location
def testimonial_image_location(instance, filename):
    full_name_proceesed= instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Testimonial/{full_name_proceesed}/{filename}"




def send_registration_success_mail(email):
    subject = 'Registration Success'
    message = 'Thank you for registering!'
    from_email = settings.EMAIL_HOST_USER  # Use your email settings here
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
