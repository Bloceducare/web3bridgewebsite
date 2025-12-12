from rest_framework import serializers
from . import models
from .literals import HUB_REGISTRATION_REF_NAME, HUB_SPACE_REF_NAME, HUB_CHECKIN_REF_NAME


class HubSpaceSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.HubSpace
            fields = ["name", "total_capacity", "current_occupancy", "is_active"]
            ref_name = HUB_SPACE_REF_NAME
        
        def create(self, validated_data):
            hub_space_obj = models.HubSpace.objects.create(**validated_data)
            hub_space_obj.save()
            return hub_space_obj
    
    class List(serializers.ModelSerializer):
        available_spaces = serializers.ReadOnlyField()
        occupancy_percentage = serializers.ReadOnlyField()
        
        class Meta:
            model = models.HubSpace
            fields = ["id", "name", "total_capacity", "current_occupancy", "available_spaces", 
                     "occupancy_percentage", "is_active", "created_at", "updated_at"]
            ref_name = HUB_SPACE_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        available_spaces = serializers.ReadOnlyField()
        occupancy_percentage = serializers.ReadOnlyField()
        
        class Meta:
            model = models.HubSpace
            fields = ["id", "name", "total_capacity", "current_occupancy", "available_spaces", 
                     "occupancy_percentage", "is_active", "created_at", "updated_at"]
            ref_name = HUB_SPACE_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.HubSpace
            fields = ["name", "total_capacity", "current_occupancy", "is_active"]
            extra_kwargs = {field: {"required": False} for field in fields}
            ref_name = HUB_SPACE_REF_NAME


class HubRegistrationSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.HubRegistration
            fields = ["name", "email", "phone_number", "location", "reason", "role", "contribution"]
            ref_name = HUB_REGISTRATION_REF_NAME
        
        def create(self, validated_data):
            hub_registration_obj = models.HubRegistration.objects.create(**validated_data)
            hub_registration_obj.save()
            return hub_registration_obj
    
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.HubRegistration
            fields = ["id", "name", "email", "phone_number", "location", "reason", "role", 
                     "contribution", "status", "created_at"]
            ref_name = HUB_REGISTRATION_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.HubRegistration
            fields = ["id", "name", "email", "phone_number", "location", "reason", "role", 
                     "contribution", "status", "notes", "created_at", "updated_at"]
            ref_name = HUB_REGISTRATION_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.HubRegistration
            fields = ["status", "notes"]
            extra_kwargs = {field: {"required": False} for field in fields}
            ref_name = HUB_REGISTRATION_REF_NAME
        
        def update(self, instance, validated_data):
            instance.status = validated_data.get("status", instance.status)
            instance.notes = validated_data.get("notes", instance.notes)
            instance.save()
            return instance


class CheckInSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.CheckIn
            fields = ["registration", "space", "purpose", "notes"]
            ref_name = HUB_CHECKIN_REF_NAME
        
        def create(self, validated_data):
            registration = validated_data.get('registration')
            space = validated_data.get('space')
            
            # Check if registration is approved
            if registration.status != models.HubRegistration.APPROVED:
                raise serializers.ValidationError(
                    {"registration": "Registration must be approved before checking in."}
                )
            
            # Check if space has available capacity
            if space and space.current_occupancy >= space.total_capacity:
                raise serializers.ValidationError(
                    {"space": "Space is at full capacity."}
                )
            
            # Check if user is already checked in
            active_checkin = models.CheckIn.objects.filter(
                registration=registration,
                status=models.CheckIn.CHECKED_IN
            ).first()
            
            if active_checkin:
                raise serializers.ValidationError(
                    {"registration": "User is already checked in. Please check out first."}
                )
            
            checkin_obj = models.CheckIn.objects.create(**validated_data)
            
            # Increase space occupancy
            if space:
                space.current_occupancy += 1
                space.save()
            
            return checkin_obj
    
    class List(serializers.ModelSerializer):
        registration_name = serializers.CharField(source='registration.name', read_only=True)
        registration_email = serializers.EmailField(source='registration.email', read_only=True)
        space_name = serializers.CharField(source='space.name', read_only=True)
        
        class Meta:
            model = models.CheckIn
            fields = ["id", "registration", "registration_name", "registration_email", 
                     "space", "space_name", "status", "check_in_time", "check_out_time", 
                     "purpose", "created_at"]
            ref_name = HUB_CHECKIN_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        registration_name = serializers.CharField(source='registration.name', read_only=True)
        registration_email = serializers.EmailField(source='registration.email', read_only=True)
        registration_phone = serializers.CharField(source='registration.phone_number', read_only=True)
        space_name = serializers.CharField(source='space.name', read_only=True)
        
        class Meta:
            model = models.CheckIn
            fields = ["id", "registration", "registration_name", "registration_email", 
                     "registration_phone", "space", "space_name", "status", 
                     "check_in_time", "check_out_time", "purpose", "notes", 
                     "created_at", "updated_at"]
            ref_name = HUB_CHECKIN_REF_NAME

