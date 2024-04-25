from rest_framework import serializers
from operation import models
from .literals import TEAM_REF_NAME, MENTOR_REF_NAME, PARTNER_REF_NAME

# Team Serializer
class TeamSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Team
            fields = ["id", "full_name", "brief", "extra_info", "picture"]
            ref_name = TEAM_REF_NAME
        
        def create(self, validated_data):
            team_obj = models.Team.objects.create(**validated_data)
            team_obj.save()
            return team_obj
        
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Team
            fields = ["id", "full_name", "brief", "extra_info", "picture"]
            ref_name = TEAM_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Team
            fields = ["id", "full_name", "brief", "extra_info", "picture"]
            ref_name = TEAM_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Team
            fields = ["id", "full_name", "brief", "extra_info", "picture"]
            ref_name = TEAM_REF_NAME
            extra_kwargs= { field: {'required': False} for field in fields}
            
        def update(self, instance, validated_data):
            instance.full_name= validated_data.get('full_name', instance.full_name)
            instance.brief= validated_data.get('brief', instance.brief)
            instance.extra_info= validated_data.get('extra_info', instance.extra_info)
            instance.picture= validated_data.get('picture', instance.picture)
            instance.save()
            return instance
        
        

# Mentor Serializer
class MentorSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Mentor
            fields = ["id", "full_name", "repo", "extra_info", "picture"]
            ref_name = MENTOR_REF_NAME
        
        def create(self, validated_data):
            mentor_obj = models.Mentor.objects.create(**validated_data)
            mentor_obj.save()
            return mentor_obj
        
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Mentor
            fields = ["id", "full_name", "repo", "extra_info", "picture"]
            ref_name = MENTOR_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Mentor
            fields = ["id", "full_name", "repo", "extra_info", "picture"]
            ref_name = MENTOR_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Mentor
            fields = ["id", "full_name", "repo", "extra_info", "picture"]
            ref_name = MENTOR_REF_NAME
            extra_kwargs= { field: {'required': False} for field in fields}
            
        def update(self, instance, validated_data):
            instance.full_name= validated_data.get('full_name', instance.full_name)
            instance.repo= validated_data.get('repo', instance.repo)
            instance.extra_info= validated_data.get('extra_info', instance.extra_info)
            instance.picture= validated_data.get('picture', instance.picture)
            instance.save()
            return instance
        
        
# Partner Serializer
class PartnerSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Partner
            fields = ["id", "name", "url", "extra_info", "picture"]
            ref_name = PARTNER_REF_NAME
        
        def create(self, validated_data):
            partner_obj = models.Partner.objects.create(**validated_data)
            partner_obj.save()
            return partner_obj
        
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Partner
            fields = ["id", "name", "url", "extra_info", "picture"]
            ref_name = PARTNER_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Partner
            fields = ["id", "name", "url", "extra_info", "picture"]
            ref_name = PARTNER_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Partner
            fields = ["id", "name", "url", "extra_info", "picture"]
            ref_name = PARTNER_REF_NAME
            extra_kwargs= { field: {'required': False} for field in fields}
            
        def update(self, instance, validated_data):
            instance.name= validated_data.get('name', instance.name)
            instance.url= validated_data.get('url', instance.url)
            instance.extra_info= validated_data.get('extra_info', instance.extra_info)
            instance.picture= validated_data.get('picture', instance.picture)
            instance.save()
            return instance