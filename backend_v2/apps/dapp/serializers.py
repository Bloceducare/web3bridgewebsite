from rest_framework import serializers
from dapp import models
from .literals import DAPP_REF_NAME

# Dapp Serializer
class DappSerializer:
    class Create(serializers.ModelSerializer):
        class Meta:
            model = models.Dapp
            fields = ["id", "name", "url", "description", "picture"]
            ref_name = DAPP_REF_NAME
        
        def create(self, validated_data):
            dapp_obj = models.Dapp.objects.create(**validated_data)
            dapp_obj.save()
            return dapp_obj
        
    class List(serializers.ModelSerializer):
        class Meta:
            model = models.Dapp
            fields = ["id", "name", "url", "description", "picture"]
            ref_name = DAPP_REF_NAME
    
    class Retrieve(serializers.ModelSerializer):
        class Meta:
            model = models.Dapp
            fields = ["id", "name", "url", "description", "picture"]
            ref_name = DAPP_REF_NAME
    
    class Update(serializers.ModelSerializer):
        class Meta:
            model = models.Dapp
            fields = ["id", "name", "url", "description", "picture"]
            ref_name = DAPP_REF_NAME
            extra_kwargs= { field: {'required': False} for field in fields}
            
        def update(self, instance, validated_data):
            instance.name= validated_data.get('name', instance.name)
            instance.url= validated_data.get('url', instance.url)
            instance.description= validated_data.get('description', instance.description)
            instance.picture= validated_data.get('picture', instance.picture)
            instance.save()
            return instance