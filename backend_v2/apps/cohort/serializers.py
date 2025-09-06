from rest_framework import serializers
from cohort import models
from utils.serializers import ImageSerializer
from utils.models import Image
from .literals import COURSE_REF_NAME, REGISTRATION_REF_NAME, PARTICIPANT_REF_NAME, TESTIMONIAL_REF_NAME

# Serializer 
# Course Serializer
class CourseSerializer:
    class Create(serializers.ModelSerializer):
        images = serializers.ListField(child=serializers.ImageField())
        
        class Meta:
            model = models.Course
            fields = ["name", "description", "venue", "extra_info", "images", "registration", "duration"]
            extra_kwargs= {"venue":{"required": True}}
            ref_name= COURSE_REF_NAME
    
        def create(self, validated_data):
            images_data = validated_data.pop("images", [])
            course_obj = models.Course.objects.create(**validated_data)
            
            for image_data in images_data:
                image_object = Image.objects.create(picture=image_data)
                image_object.save()
                course_obj.images.add(image_object)
                
            course_obj.save()
            return course_obj
        
    class List(serializers.ModelSerializer):
        images = ImageSerializer(many=True, read_only=True)
        
        class Meta:
            model = models.Course
            fields = ["id", "name", "description", "venue", "extra_info", "images", "status", "registration", "duration"]
    
    class Retrieve(serializers.ModelSerializer):
        images = ImageSerializer(many=True, read_only=True)
        
        class Meta:
            model = models.Course
            fields = ["id", "name", "description", "venue", "extra_info", "images", "status", "registration", "duration"]
    
    class Update(serializers.ModelSerializer):
        images = serializers.ListField(child=serializers.ImageField(), required=False)
        
        class Meta:
            ref_name = "courses"
            model = models.Course
            fields = ["id", "name", "description", "venue", "extra_info", "images", "status", "registration", "duration"]
            extra_kwargs= { field: {"required": False} for field in fields}
            
        def update(self, instance, validated_data):
            images_data = validated_data.pop("images", [])
            uploaded_images= []
            
            for image_data in images_data:
                image_object = Image.objects.create(picture=image_data)
                image_object.save()
                uploaded_images.append(image_object)
            
            if len(uploaded_images) > 0:
                instance.images.clear() 
                instance.images.set(uploaded_images)    
                
            instance.name= validated_data.get("name", instance.name)
            instance.status= validated_data.get("status", instance.status)
            instance.description= validated_data.get("description", instance.description)
            instance.venue= validated_data.get("venue", instance.venue)
            instance.extra_info= validated_data.get("extra_info", instance.extra_info)
            instance.registration= validated_data.get("registration", instance.registration)
            instance.duration= validated_data.get("duration", instance.duration)
            instance.save()
            return instance

# Registration Serializer
class RegistrationSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = ["id", "name", "start_date", "end_date", "registrationFee", 'cohort']
            ref_name = REGISTRATION_REF_NAME
        
        def create(self, validated_data):
            registration_obj = models.Registration.objects.create(**validated_data)
            registration_obj.save()
            return registration_obj
        
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = ["id", "name", "is_open", "start_date", "end_date", "registrationFee", "courses", 'cohort']
            ref_name = REGISTRATION_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = ["id", "name", "is_open", "start_date", "end_date", "registrationFee", "courses", 'cohort']
            ref_name = REGISTRATION_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Registration
            fields = ["id", "name", "is_open", "start_date", "end_date", "registrationFee", 'cohort']
            ref_name = REGISTRATION_REF_NAME
            extra_kwargs= { field: {"required": False} for field in fields}
            
        def update(self, instance, validated_data):
            instance.name= validated_data.get("name", instance.name)
            instance.is_open= validated_data.get("is_open", instance.is_open)
            instance.start_date= validated_data.get("start_date", instance.start_date)
            instance.end_date= validated_data.get("end_date", instance.end_date)
            instance.registrationFee= validated_data.get("registrationFee", instance.registrationFee)
            instance.cohort= validated_data.get("cohort", instance.cohort)
            instance.save()
            return instance

# Participant Serializer
class ParticipantSerializer:
    class Create(serializers.ModelSerializer):
        name = serializers.CharField(required=True)
        wallet_address = serializers.CharField(required=True)
        email = serializers.EmailField(required=True)
        registration = serializers.PrimaryKeyRelatedField(queryset=models.Registration.objects.all(), required=True)
        course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all(), required=True)
        motivation = serializers.CharField(required=True)
        achievement = serializers.CharField(required=True)
        city = serializers.CharField(required=True)
        state = serializers.CharField(required=True)
        country = serializers.CharField(required=True)
        gender = serializers.CharField(required=True)
        github = serializers.URLField(required=False)
        number = serializers.CharField(required=True)
        venue = serializers.CharField(required=True)
        class Meta:
            model = models.Participant
            exclude = ["status", "payment_status", "cohort"]
            ref_name= PARTICIPANT_REF_NAME

        def validate_email(self, email):
            request = self.context.get("request")
            if not request:
                raise serializers.ValidationError("Request context is required.")
            email = email
            course_id = request.data.get('course')
            try:
                course = models.Course.objects.get(id=course_id)
            except models.Course.DoesNotExist:
                raise serializers.ValidationError("Course does not exist")
            
            registration = course.registration

            participants = models.Participant.objects.filter(email=email).all()
            existing_participant = None
            for participant in participants:
                if participant.registration == registration or participant.course == course:
                    existing_participant = participant
                    break
            
            if existing_participant:
                if existing_participant.payment_status:
                    raise serializers.ValidationError("Participant already registered and paid for this cohort")
                else:
                    # User is registered but hasn't paid - provide payment link
                    raise serializers.ValidationError({
                        "already_registered_unpaid": True,
                        "message": "You are already registered for this course but haven't completed payment. Please proceed to payment to secure your spot.",
                        "payment_link": "https://payment.web3bridgeafrica.com",
                        "participant_id": existing_participant.id
                    })
            return email

        
        def create(self, validated_data):
            participant_obj = models.Participant.objects.create(**validated_data)
            registration = participant_obj.course.registration
            participant_obj.registration = registration
            cohort = participant_obj.registration.name
            participant_obj.cohort = cohort
            participant_obj.save()
            return participant_obj
                
    class List(serializers.ModelSerializer):
        course= CourseSerializer.Retrieve(read_only=True)
        registration = RegistrationSerializer.Retrieve(read_only=True)
        class Meta:
            model = models.Participant
            fields = "__all__"
            ref_name= PARTICIPANT_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        course= CourseSerializer.Retrieve(read_only=True)
        registration = RegistrationSerializer.Retrieve(read_only=True)
        class Meta:
            model = models.Participant
            fields = "__all__"
            ref_name= PARTICIPANT_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Participant
            fields = ["id", "name", "wallet_address", "email", "registration", "status", "motivation", "achievement", 
                      "city", "state", "country", "gender", "github", "number", "course", "cohort", "venue"]
            extra_kwargs= { field: {"required": False} for field in fields}
            ref_name= PARTICIPANT_REF_NAME

        def update(self, instance, validated_data):
            instance.name= validated_data.get("name", instance.name)
            instance.wallet_address= validated_data.get("wallet_address", instance.wallet_address)
            instance.email= validated_data.get("email", instance.email)
            instance.registration= validated_data.get("registration", instance.registration)
            instance.status= validated_data.get("status", instance.status)
            instance.motivation= validated_data.get("motivation", instance.motivation)
            instance.achievement= validated_data.get("achievement", instance.achievement)
            instance.city= validated_data.get("city", instance.city)
            instance.state= validated_data.get("state", instance.state)
            instance.country= validated_data.get("country", instance.country)
            # instance.duration= validated_data.get("duration", instance.duration)
            instance.gender= validated_data.get("gender", instance.gender)
            instance.github= validated_data.get("github", instance.github)
            instance.number= validated_data.get("number", instance.number)
            instance.course= validated_data.get("course", instance.course)
            instance.cohort= validated_data.get("cohort", instance.cohort)
            instance.venue= validated_data.get("venue", instance.venue)
            instance.payment_status= validated_data.get("payment_status", instance.payment_status)

            instance.save()
            return instance
        
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


# Testimonial Serializer
class TestimonialSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = ["id", "full_name", "testimony", "picture_link", "created_at", "updated_at"]
            ref_name = TESTIMONIAL_REF_NAME
        
        def create(self, validated_data):
            registration_obj = models.Testimonial.objects.create(**validated_data)
            registration_obj.save()
            return registration_obj
        
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = ["id", "full_name", "testimony", "picture_link", "created_at", "updated_at"]
            ref_name = TESTIMONIAL_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = ["id", "full_name", "testimony", "picture_link", "created_at", "updated_at"]
            ref_name = TESTIMONIAL_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Testimonial
            fields = ["id", "full_name", "testimony", "picture_link"]
            ref_name = TESTIMONIAL_REF_NAME
            extra_kwargs= { field: {"required": False} for field in fields}
            
        def update(self, instance, validated_data):
            instance.headline= validated_data.get("headline", instance.headline)
            instance.full_name= validated_data.get("full_name", instance.full_name)
            instance.testimony= validated_data.get("testimony", instance.testimony)
            instance.picture_link= validated_data.get("picture_link", instance.picture)
            instance.save()
            return instance


class BulkEmailSerializer(serializers.Serializer):
    recipients = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=models.Participant.objects.all()),
        help_text="List of participant IDs to send the email to"
    )
    subject = serializers.CharField(
        max_length=200,
        help_text="Email subject line"
    )
    body = serializers.CharField(
        help_text="Email body content"
    )

    class Meta:
        fields = ["recipients", "subject", "body"]

    def validate_recipients(self, value):
        if not value:
            raise serializers.ValidationError("At least one recipient is required")
        return value

