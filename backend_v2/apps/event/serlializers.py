from django.db.models import fields
from rest_framework import serializers
from .models import Event

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('title', 'description', 'start_datetime', 'end_datetime', 'location')