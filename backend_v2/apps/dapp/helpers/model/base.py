from django.conf import settings

# dapp image storage location
def dapp_image_location(instance, filename):
    return f"{settings.ENVIROMENT}/dapp/{instance.name}/{filename}"