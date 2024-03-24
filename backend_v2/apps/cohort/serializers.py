from rest_framework import serializers
from cohort import models

# Serializer 
# Course Serializer
class CourseSerializer:
    class List(serializers.ModelSerializer):
        pass
    
    class Retrieve(serializers.ModelSerializer):
        pass
    
    class Update(serializers.ModelSerializer):
        pass

# Registration Serializer
class RegistrationSerializer:
    class List(serializers.ModelSerializer):
        pass
    
    class Retrieve(serializers.ModelSerializer):
        pass
    
    class Update(serializers.ModelSerializer):
        pass

# Participant Serializer
class ParticipantSerializer:
    class List(serializers.ModelSerializer):
        pass
    
    class Retrieve(serializers.ModelSerializer):
        pass
    
    class Update(serializers.ModelSerializer):
        pass

# Testimonial Serializer
class TestimonialSerializer:
    class List(serializers.ModelSerializer):
        pass
    
    class Retrieve(serializers.ModelSerializer):
        pass
    
    class Update(serializers.ModelSerializer):
        pass