from rest_framework import serializers
from cohort import models

# Serializer 
# Course Serializer
class CourseSerializer:
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Course
            fields = "__all__"
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Course
            fields = "__all__"
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Course
            fields = "__all__"

# Registration Serializer
class RegistrationSerializer:
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = "__all__"
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = "__all__"
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = "__all__"

# Participant Serializer
class ParticipantSerializer:
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Participant
            fields = "__all__"
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Participant
            fields = "__all__"
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Participant
            fields = "__all__"

# Testimonial Serializer
class TestimonialSerializer:
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = "__all__"
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = "__all__"
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = "__all__"