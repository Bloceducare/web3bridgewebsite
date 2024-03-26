from django.conf import settings

# Testimonial image storage location
def testimonial_image_location(instance, filename):
    return f"{settings.ENVIROMENT}/Testimonial/{instance.last_name}_{instance.first_name}/{filename}"