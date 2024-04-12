from django.conf import settings

# Team image storage location
def team_image_location(instance, filename):
    full_name_proceesed= instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Team/{full_name_proceesed}/{filename}"

# Mentor image storage location
def mentor_image_location(instance, filename):
    full_name_proceesed= instance.full_name.replace(" ", "_")
    return f"{settings.ENVIROMENT}/Team/{full_name_proceesed}/{filename}"