from requests import Response
from rest_framework import decorators, status, viewsets
from . import serializers, models
from utils.helpers.requests import Utils as requestUtils
from drf_yasg.utils import swagger_auto_schema
from .helpers.model import send_registration_success_mail 
from backend_v2.scripts.mail import send_bulk_email
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin 

class CouresViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset= models.Course.objects
    serializer_class= serializers.CourseSerializer
    admin_actions= ["create", "update", "destroy", "open_course", "close_course"]
    
    @swagger_auto_schema(request_body=serializers.CourseSerializer.Create)
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            course_obj= serializer.save()
            serialized_course_obj= self.serializer_class.Retrieve(course_obj).data
            return requestUtils.success_response(data=serialized_course_obj, http_status=status.HTTP_201_CREATED)
        
        return requestUtils.error_response("Error Creating Course", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    
    def retrieve(self, request, pk, *args, **kwargs): 
        course_object= self.queryset.get(pk=pk)
        serialized_course_obj= self.serializer_class.Retrieve(course_object).data
        return requestUtils.success_response(data=serialized_course_obj, http_status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=serializers.CourseSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        course_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(course_object, data=request.data)
        
        if serializer.is_valid():
            registration_obj= serializer.save()
            serialized_registration_obj= self.serializer_class.Retrieve(registration_obj).data
            return requestUtils.success_response(data=serialized_registration_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Registration", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
   
   
    def destroy(self, request, pk, *args, **kwargs): 
        course_object= self.queryset.get(pk=pk)
        course_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def all_opened(self, request):
        query_set= self.queryset.filter(status= True)
        serializer = self.serializer_class.List(query_set, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=True, methods=["put"])
    def open_course(self, request, pk):
        course_object= self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(course_object, data={"status": True})
        
        if serializer.is_valid():
            course_obj= serializer.save()
            serialized_course_obj= self.serializer_class.Retrieve(course_obj).data
            return requestUtils.success_response(data=serialized_course_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Opening Course", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    @decorators.action(detail=True, methods=["put"])
    def close_course(self, request, pk):
        course_object= self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(course_object, data={"status": False})
        
        if serializer.is_valid():
            course_obj= serializer.save()
            serialized_course_obj= self.serializer_class.Retrieve(course_obj).data
            return requestUtils.success_response(data=serialized_course_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Opening Course", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    

    
class RegistrationViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset= models.Registration.objects
    serializer_class= serializers.RegistrationSerializer
    admin_actions= ["create", "update", "destroy", "close_registration", "open_registration"]
    
    @swagger_auto_schema(request_body=serializers.RegistrationSerializer.Create)
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            registration_obj= serializer.save()
            serialized_registration_obj= self.serializer_class.Retrieve(registration_obj).data
            return requestUtils.success_response(data=serialized_registration_obj, http_status=status.HTTP_201_CREATED)
        
        return requestUtils.error_response("Error Creating Registration", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(request_body=serializers.RegistrationSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        registration_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(registration_object, data=request.data)
        
        if serializer.is_valid():
            registration_obj= serializer.save()
            serialized_registration_obj= self.serializer_class.Retrieve(registration_obj).data
            return requestUtils.success_response(data=serialized_registration_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Registration", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
        
        
    def retrieve(self, request, pk, *args, **kwargs): 
        registration_object= self.queryset.get(pk=pk)
        serialized_registration_obj= self.serializer_class.Retrieve(registration_object).data
        return requestUtils.success_response(data=serialized_registration_obj, http_status=status.HTTP_200_OK)
     
     
    def destroy(self, request, pk, *args, **kwargs): 
        registration_object= self.queryset.get(pk=pk)
        registration_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=False, methods=["get"])
    def all_opened(self, request):
        query_set= self.queryset.filter(is_open= True)
        serializer = self.serializer_class.List(query_set, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=True, methods=["put"])
    def close_registration(self, request,  pk=None):
        registration_object= self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(registration_object, data={"is_open": False})
        
        if serializer.is_valid():
            registration_obj= serializer.save()
            serialized_registration_obj= self.serializer_class.Retrieve(registration_obj).data
            return requestUtils.success_response(data=serialized_registration_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Closing Registration", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
            
        
    @decorators.action(detail=True, methods=["put"])
    def open_registration(self, request,  pk=None):
        registration_object= self.queryset.get(pk=pk)
        serializer = self.serializer_class.Update(registration_object, data={"is_open": True})
        
        if serializer.is_valid():
            registration_obj= serializer.save()
            serialized_registration_obj= self.serializer_class.Retrieve(registration_obj).data
            return requestUtils.success_response(data=serialized_registration_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Opening Registration", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)

class ParticipantViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Participant.objects.all()
    serializer_class = serializers.ParticipantSerializer
    admin_actions= ["update", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.ParticipantSerializer.Create())
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            participant_obj= serializer.save()
            serialized_participant_obj= self.serializer_class.Retrieve(participant_obj).data
            email = serialized_participant_obj.get('email')
            course = serialized_participant_obj.get('course').get('id') 
            participant = serialized_participant_obj.get('name')
            send_registration_success_mail(email, course, participant)
            return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_201_CREATED)
        return requestUtils.error_response("Error Creating Participant", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(request_body=serializers.ParticipantSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        participant_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(participant_object, data=request.data)
        
        if serializer.is_valid():
            participant_obj= serializer.save()
            serialized_participant_obj= self.serializer_class.Retrieve(participant_obj).data
            return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Participant", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
       
        
    def retrieve(self, request, pk, *args, **kwargs): 
        participant_object= self.queryset.get(pk=pk)
        serialized_participant_obj= self.serializer_class.Retrieve(participant_object).data
        return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)
    
    
    def destroy(self, request, pk, *args, **kwargs): 
        registration_object= self.queryset.get(pk=pk)
        registration_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=True, methods=["get"])
    def registration(self, request, pk):
        query_set= self.queryset.filter(registration= pk)
        serializer = self.serializer_class.List(query_set, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)

class TestimonialViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Testimonial.objects.all()
    serializer_class = serializers.TestimonialSerializer
    admin_actions= ["create", "update", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.TestimonialSerializer.Create())
    def create(self, request, *args, **kwargs): 
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            testimonial_obj= serializer.save()
            serialized_testimonial_obj= self.serializer_class.Retrieve(testimonial_obj).data
            return requestUtils.success_response(data=serialized_testimonial_obj, http_status=status.HTTP_201_CREATED)
        
        return requestUtils.error_response("Error Creating Testimonial", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=serializers.TestimonialSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        testimonial_object= self.queryset.get(pk=pk)    
        serializer = self.serializer_class.Update(testimonial_object, data=request.data)
        
        if serializer.is_valid():
            testimonial_obj= serializer.save()
            serialized_testimonial_obj= self.serializer_class.Retrieve(testimonial_obj).data
            return requestUtils.success_response(data=serialized_testimonial_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Testimonial", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk, *args, **kwargs): 
        testimonial_object= self.queryset.get(pk=pk)
        testimonial_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs): 
        testimonial_object= self.queryset.get(pk=pk)
        serialized_testimonial_obj= self.serializer_class.Retrieve(testimonial_object).data
        return requestUtils.success_response(data=serialized_testimonial_obj, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class.List(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    



class BulkEmailViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):

    @swagger_auto_schema(request_body=serializers.BulkEmailSerializer)
    @decorators.action(detail=False, methods=["post"])
    def send_bulk_email(self, request):
        serializer = serializers.BulkEmailSerializer(data=request.data)
        if serializer.is_valid():
            send_bulk_email()
            return Response({"message": "Emails sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)