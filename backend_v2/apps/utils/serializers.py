from .models import Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None, allow_empty_file=False)
    
    class Meta:
        model = Image
        fields = ['id', 'picture']
        