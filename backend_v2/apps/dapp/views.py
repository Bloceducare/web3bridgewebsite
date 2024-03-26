from rest_framework import decorators, response, status, viewsets
from . import serializers, models
from utils.helpers.requests import Utils as requestUtils
from drf_yasg.utils import swagger_auto_schema
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin 

class DappViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Dapp.objects.all()
    serializer_class = serializers.DappSerializer
    admin_actions= ["create", "update", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.DappSerializer.Create())
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            dapp_obj= serializer.save()
            serialized_testimonial_obj= self.serializer_class.Retrieve(dapp_obj).data
            return requestUtils.success_response(data=serialized_testimonial_obj, http_status=status.HTTP_201_CREATED)
        
        return requestUtils.error_response("Error Creating Dapp", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=serializers.DappSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        dapp_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(dapp_object, data=request.data)
        
        if serializer.is_valid():
            dapp_obj= serializer.save()
            serialized_testimonial_obj= self.serializer_class.Retrieve(dapp_obj).data
            return requestUtils.success_response(data=serialized_testimonial_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Dapp", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk, *args, **kwargs): 
        dapp_object= self.queryset.get(pk=pk)
        dapp_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs): 
        dapp_object= self.queryset.get(pk=pk)
        serialized_dapp_obj= self.serializer_class.Retrieve(dapp_object).data
        return requestUtils.success_response(data=serialized_dapp_obj, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
