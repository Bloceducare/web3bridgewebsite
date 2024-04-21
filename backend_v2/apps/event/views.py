from rest_framework import decorators, status, viewsets
from . import serializers, models
from utils.helpers.requests import Utils as requestUtils
from drf_yasg.utils import swagger_auto_schema
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin


class EventViewSet(viewsets.ViewSet, GuestReadAllWriteAdminOnlyPermissionMixin):
        query_set = models.Event.objects.all()
        serializer_class = serializers.EventSerializer
        admin_actions = ["create", "update", "destroy"]

        @swagger_auto_schema(request_body=serializers.EventSerializer.Create())
        def create(self, request, *args, **kwargs):
            serializer = self.serializer_class.Create(data=request.data)

            if serializer.is_valid():
                event_obj = serializer.save()
                serialized_event_obj = self.serializer_class.Retrieve(event_obj).data
                return requestUtils.success_response(data=serialized_event_obj, http_status=status.HTTP_201_CREATED)

            return requestUtils.error_response("Error Creating Event", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)

        @swagger_auto_schema(request_body=serializers.EventSerializer.Update())
        def update(self, request, pk, *args, **kwargs):
            event_object = self.query_set.get(pk=pk)
            serializer = self.serializer_class.Update(event_object, data=request.data)

            if serializer.is_valid():
                event_obj = serializer.save()
                serialized_event_obj = self.serializer_class.Retrieve(event_obj).data
                return requestUtils.success_response(data=serialized_event_obj, http_status=status.HTTP_200_OK)
            else:
                return requestUtils.error_response("Error Updating Event", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
            
        def destroy(self, request, pk, *args, **kwargs):
            event_object = self.query_set.get(pk=pk)
            event_object.delete()
            return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)

        @decorators.action(detail=False, methods=["get"])
        def all(self, request):
            serializer = self.serializer_class.List(self.query_set, many=True)
            return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
        
        def retrieve(self, request, pk, *args, **kwargs):
            event_object = self.query_set.get(pk=pk)
            serialized_event_obj = self.serializer_class.Retrieve(event_object).data
            return requestUtils.success_response(data=serialized_event_obj, http_status=status.HTTP_200_OK)
        
        @decorators.action(detail=False, methods=["get"])
        def all(self, request):
            serializer = self.serializer_class.List(self.query_set, many=True)
            return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)