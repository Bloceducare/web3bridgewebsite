from rest_framework import decorators, response, status, viewsets
from . import serializers, models
from utils.helpers.requests import Utils as requestUtils
from drf_yasg.utils import swagger_auto_schema
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin 

class TeamViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    admin_actions= ["create", "update", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.TeamSerializer.Create())
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            team_obj= serializer.save()
            serialized_team_obj= self.serializer_class.Retrieve(team_obj).data
            return requestUtils.success_response(data=serialized_team_obj, http_status=status.HTTP_201_CREATED)
        
        return requestUtils.error_response("Error Creating Team", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=serializers.TeamSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        dapp_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(dapp_object, data=request.data)
        
        if serializer.is_valid():
            team_obj= serializer.save()
            serialized_team_obj= self.serializer_class.Retrieve(team_obj).data
            return requestUtils.success_response(data=serialized_team_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Team", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk, *args, **kwargs): 
        team_object= self.queryset.get(pk=pk)
        team_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs): 
        team_object= self.queryset.get(pk=pk)
        serialized_team_obj= self.serializer_class.Retrieve(team_object).data
        return requestUtils.success_response(data=serialized_team_obj, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)


class MentorViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Mentor.objects.all()
    serializer_class = serializers.MentorSerializer
    admin_actions= ["create", "update", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.MentorSerializer.Create())
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            mentor_obj= serializer.save()
            serialized_mentor_obj= self.serializer_class.Retrieve(mentor_obj).data
            return requestUtils.success_response(data=serialized_mentor_obj, http_status=status.HTTP_201_CREATED)
        
        return requestUtils.error_response("Error Creating Mentor", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=serializers.MentorSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        mentor_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(mentor_object, data=request.data)
        
        if serializer.is_valid():
            mentor_obj= serializer.save()
            serialized_mentor_obj= self.serializer_class.Retrieve(mentor_obj).data
            return requestUtils.success_response(data=serialized_mentor_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Mentor", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk, *args, **kwargs): 
        mentor_object= self.queryset.get(pk=pk)
        mentor_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs): 
        mentor_object= self.queryset.get(pk=pk)
        serialized_mentor_obj= self.serializer_class.Retrieve(mentor_object).data
        return requestUtils.success_response(data=serialized_mentor_obj, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)


class PartnerViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer
    # admin_actions= ["create", "update", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.PartnerSerializer.Create())
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            mentor_obj= serializer.save()
            serialized_partner_obj= self.serializer_class.Retrieve(mentor_obj).data
            return requestUtils.success_response(data=serialized_partner_obj, http_status=status.HTTP_201_CREATED)
        
        return requestUtils.error_response("Error Creating Patner", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=serializers.PartnerSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        partner_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(partner_object, data=request.data)
        
        if serializer.is_valid():
            partner_obj= serializer.save()
            serialized_partner_obj= self.serializer_class.Retrieve(partner_obj).data
            return requestUtils.success_response(data=serialized_partner_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Partner", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk, *args, **kwargs): 
        partner_object= self.queryset.get(pk=pk)
        partner_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs): 
        partner_object= self.queryset.get(pk=pk)
        serialized_partner_obj= self.serializer_class.Retrieve(partner_object).data
        return requestUtils.success_response(data=serialized_partner_obj, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)