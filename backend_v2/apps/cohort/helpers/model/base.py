# Testimonial image storage location
def testimonial_image_location(instance, filename):
    return f"Testimonial/{instance.last_name}_{instance.first_name}/{filename}"