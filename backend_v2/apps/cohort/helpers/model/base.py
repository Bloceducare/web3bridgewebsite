from django.conf import settings

# Testimonial image storage location
def testimonial_image_location(instance, filename):
    full_name_proceesed= instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Testimonial/{full_name_proceesed}/{filename}"