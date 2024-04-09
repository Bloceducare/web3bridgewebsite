
def cloudinary_image_delete_signal_handlers(sender, instance, **kwargs):
    instance.delete_cloudinary_image()