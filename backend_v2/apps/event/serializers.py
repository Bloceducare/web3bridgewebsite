from .models import Event
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Create(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ["id", "title", "description", "date", "time", "time_zone", "location", "image"]
        
        def create(self, validated_data):
            event_obj = Event.objects.create(**validated_data)
            event_obj.save()
            return event_obj
    
    class List(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ["id", "title", "description", "date", "time", "time_zone", "location", "image"]

    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ["id", "title", "description", "date", "time", "time_zone", "location", "image"]
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ["id", "title", "description", "date", "time", "time_zone", "location", "image"]
            extra_kwargs= { field: {'required': False} for field in fields}
            
        def update(self, instance, validated_data):
            instance.title= validated_data.get('title', instance.title)
            instance.description= validated_data.get('description', instance.description)
            instance.date= validated_data.get('date', instance.date)
            instance.time= validated_data.get('time', instance.time)
            instance.time_zone= validated_data.get('time_zone', instance.time_zone)
            instance.location= validated_data.get('location', instance.location)
            instance.image= validated_data.get('image', instance.image)
            instance.save()
            return instance
        
    class Delete(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ["id", "title", "description", "date", "time", "time_zone", "location", "image"]
        
        def delete(self, instance):
            instance.delete()
            return instance
        
    
