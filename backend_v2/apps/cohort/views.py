from django.forms import ValidationError
from rest_framework.response import Response
from payment.models import DiscountCode, Payment
from rest_framework import decorators, pagination, status, viewsets
from . import serializers, models
from utils.helpers.requests import Utils as requestUtils
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from .helpers.model import send_registration_success_mail, send_participant_details
from backend_v2.scripts.mail import send_bulk_email
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin 

API_KEY = config("PAYMENT_API_KEY")

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
    admin_actions= ["update", "destroy", "send_confirmation_email"]

    def check_api_key(self, request):
        api_key = request.headers.get('API-Key')
        if not api_key or api_key != API_KEY:
            return False
        return True
    
    @swagger_auto_schema(request_body=serializers.ParticipantSerializer.Create())
    def create(self, request, *args, **kwargs):
        # Check if registration is open
        registration_id = request.data.get('registration')
        try:
            registration_obj = models.Registration.objects.get(pk=registration_id)
            if not registration_obj.is_open:
                return requestUtils.error_response(
                    "Registration is closed", {}, http_status=status.HTTP_400_BAD_REQUEST
                )
        except models.Registration.DoesNotExist:
            return requestUtils.error_response(
                "Invalid registration ID", {}, http_status=status.HTTP_400_BAD_REQUEST
            )

        # Handle request data and discount code
        request_data = request.data
        discount_code = request_data.pop("discount", None)

        # Validate discount code if provided
        if discount_code:
            discount_obj = DiscountCode.objects.filter(code=discount_code).first()
            if not discount_obj:
                return requestUtils.error_response(
                    "Invalid discount code", {}, http_status=status.HTTP_400_BAD_REQUEST
                )
            
            # Use the new validation logic
            user_email = request_data.get('email')
            if user_email:
                can_use, message = discount_obj.can_be_used_by(user_email)
                if not can_use:
                    return requestUtils.error_response(
                        message, {}, http_status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # Fallback for legacy validation
                if discount_obj.is_used:
                    return requestUtils.error_response(
                        "Discount code has already been used", {}, http_status=status.HTTP_400_BAD_REQUEST
                    )

        # Serialize and save participant only after successful discount validation
        serializer = self.serializer_class.Create(data=request_data, context={'request': request})

        if serializer.is_valid():
            try:
                participant_obj = serializer.save()
            except Exception as e:
                return requestUtils.error_response(
                    "Error Creating Participant", str(e), http_status=status.HTTP_400_BAD_REQUEST
                )
            serialized_participant_obj = self.serializer_class.Retrieve(participant_obj).data

            # If a valid discount code was provided, mark it as used
            if discount_code:
                user_email = serialized_participant_obj.get('email')
                participant_id = participant_obj.id
                
                # Use the new mark_usage method
                discount_obj.mark_usage(user_email, participant_id)
                
                # For legacy single-use codes, also update claimant
                if discount_obj.offset == 1:
                    discount_obj.claimant = user_email
                    discount_obj.save()
                
                participant_obj.payment_status = True
                participant_obj.save()
                serialized_participant_obj = self.serializer_class.Retrieve(participant_obj).data

                # Send registration success email
                email = serialized_participant_obj.get('email')
                participant_name = serialized_participant_obj.get('name')
                course_id = serialized_participant_obj.get('course').get('id')

                send_registration_success_mail(email, course_id, participant_name)
                send_participant_details(email, course_id, serialized_participant_obj)

            # Return success response
            return requestUtils.success_response(
                data=serialized_participant_obj, http_status=status.HTTP_201_CREATED
            )

        # Check for special case: user already registered but unpaid
        if serializer.errors and 'email' in serializer.errors:
            email_errors = serializer.errors['email']
            if any('payment pending' in str(error) for error in email_errors):
                # Find the existing participant
                email = request_data.get('email')
                course_id = request_data.get('course')
                try:
                    course = models.Course.objects.get(id=course_id)
                    participant = models.Participant.objects.filter(
                        email=email,
                        course=course
                    ).first()
                    
                    if participant and not participant.payment_status:
                        return requestUtils.error_response(
                            "Already Registered - Payment Pending", {
                                "already_registered_unpaid": True,
                                "message": "You are already registered for this course but haven't completed payment. Please proceed to payment to secure your spot.",
                                "payment_link": "https://payment.web3bridgeafrica.com",
                                "participant_id": participant.id
                            }, http_status=status.HTTP_400_BAD_REQUEST
                        )
                except models.Course.DoesNotExist:
                    pass

        # Return error response if serializer is invalid
        return requestUtils.error_response(
            "Error Creating Participant", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(request_body=serializers.EmailSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="verify-payment-by-email")
    def verify_payment_by_email(self, request, *args, **kwargs):
        if not self.check_api_key(request):
            return Response(
                {"error": "Invalid or missing API key"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        email = request.data.get("email")
        if not email:
            return requestUtils.error_response("Email is required", {}, http_status=status.HTTP_400_BAD_REQUEST)
        
        participant_object = self.queryset.filter(email=email).order_by('-created_at').first()
        if not participant_object:
            return requestUtils.error_response("Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND)
        
        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        participant_object.payment_status = True
        participant_object.save()

        # Send registration success email
        email = serialized_participant_obj.get('email')
        participant_name = serialized_participant_obj.get('name')
        course_id = serialized_participant_obj.get('course').get('id')

        send_registration_success_mail(email, course_id, participant_name)
        send_participant_details(email, course_id, serialized_participant_obj)
        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)
        
    @swagger_auto_schema(request_body=serializers.EmailSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="check-registration-status")
    def check_registration_status(self, request, *args, **kwargs):
        """Check if a user is already registered and their payment status"""
        email = request.data.get("email")
        course_id = request.data.get("course")
        
        if not email or not course_id:
            return requestUtils.error_response(
                "Email and course ID are required", {}, http_status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            course = models.Course.objects.get(id=course_id)
            registration = course.registration
            
            # Find existing participant
            participant = models.Participant.objects.filter(
                email=email,
                course=course
            ).first()
            
            if not participant:
                return requestUtils.success_response({
                    "registered": False,
                    "message": "No registration found for this email and course"
                }, http_status=status.HTTP_200_OK)
            
            return requestUtils.success_response({
                "registered": True,
                "payment_status": participant.payment_status,
                "participant_id": participant.id,
                "message": "Already paid" if participant.payment_status else "Registered but payment pending",
                "payment_link": "https://payment.web3bridgeafrica.com" if not participant.payment_status else None
            }, http_status=status.HTTP_200_OK)
            
        except models.Course.DoesNotExist:
            return requestUtils.error_response(
                "Course not found", {}, http_status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(request_body=serializers.EmailSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="send-confirmation-email")
    def send_confirmation_email(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return requestUtils.error_response("Email is required", {}, http_status=status.HTTP_400_BAD_REQUEST)
        
        participant_object = self.queryset.filter(email=email).order_by('-created_at').first()
        if not participant_object:
            return requestUtils.error_response("Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND)
        
        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        participant_object.payment_status = True
        participant_object.save()

        # Send registration success email
        email = serialized_participant_obj.get('email')
        participant_name = serialized_participant_obj.get('name')
        course_id = serialized_participant_obj.get('course').get('id')

        send_registration_success_mail(email, course_id, participant_name)
        send_participant_details(email, course_id, serialized_participant_obj)
        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)

    
    
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
        participant_object= self.queryset.get(pk=pk)
        participant_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        page_size = 50
        paginator = pagination.PageNumberPagination()
        paginator.page_size = page_size
        
        page = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class.List(page, many=True)
        
        return requestUtils.success_response(
            data={
                'count': self.queryset.count(),
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': serializer.data
            }, 
            http_status=status.HTTP_200_OK
        )
    
    
    @decorators.action(detail=True, methods=["get"])
    def registration(self, request, pk):
        query_set= self.queryset.filter(registration=pk)
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
            subject = serializer.validated_data['subject']
            html_body = serializer.validated_data['body']
            recipients = request.data.get('recipients', [])
            from_admission = request.data.get('from_admission', False)  # New parameter
            if not recipients:
                return Response({"message": "No recipients provided"}, status=status.HTTP_400_BAD_REQUEST)
            send_bulk_email(subject, html_body, recipients, from_admission=from_admission)
            return Response({"message": "Emails sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.BulkEmailSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="send-admission-email")
    def send_admission_bulk_email(self, request):
        """Send bulk emails from admission@web3bridge.com"""
        serializer = serializers.BulkEmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            html_body = serializer.validated_data['body']
            recipients = request.data.get('recipients', [])
            if not recipients:
                return Response({"message": "No recipients provided"}, status=status.HTTP_400_BAD_REQUEST)
            send_bulk_email(subject, html_body, recipients, from_admission=True)
            return Response({"message": "Admission emails sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
