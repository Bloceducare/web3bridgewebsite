from django.forms import ValidationError
from django.core.cache import cache
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from payment.models import DiscountCode, Payment
from rest_framework import decorators, pagination, status, viewsets
from . import serializers, models
from utils.helpers.requests import Utils as requestUtils
from decouple import config
import threading
import json
from drf_yasg.utils import swagger_auto_schema
from .helpers.model import send_registration_success_mail, send_participant_details, send_approval_email
from backend_v2.scripts.mail import send_bulk_email
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin 
from utils.enums.models import RegistrationStatus
from django.conf import settings

def invalidate_participant_cache():
    """Helper function to invalidate participant cache"""
    try:
        # Try to use delete_pattern if available (django-redis)
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern('participants_all_page_*')
        else:
            # Fallback: clear all cache or use a different approach
            # For now, we'll just clear the entire cache namespace
            # In production, you might want to track cache keys
            cache.clear()
    except Exception:
        # If cache operations fail, continue without cache invalidation
        pass

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
    serializer_class = serializers.ParticipantSerializer
    admin_actions= ["update", "destroy", "send_confirmation_email", "approve"]
    
    def get_queryset(self):
        """
        Optimized queryset with select_related, prefetch_related, and ordering.
        This prevents N+1 queries and ensures data is ordered by newest first.
        """
        return models.Participant.objects.select_related(
            'course',
            'registration',
            'course__registration'
        ).prefetch_related(
            'course__images'
        ).order_by('-created_at')
    
    @property
    def queryset(self):
        """Property to maintain backward compatibility"""
        return self.get_queryset()

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
                # Invalidate cache when new participant is created
                invalidate_participant_cache()
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
        
        participant_object = self.get_queryset().filter(email=email).first()
        if not participant_object:
            return requestUtils.error_response("Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND)
        
        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        participant_object.payment_status = True
        participant_object.save()
        # Invalidate cache when payment status changes
        invalidate_participant_cache()

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
        
        participant_object = self.get_queryset().filter(email=email).first()
        if not participant_object:
            return requestUtils.error_response("Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND)
        
        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        participant_object.payment_status = True
        participant_object.save()
        # Invalidate cache when payment status changes
        invalidate_participant_cache()

        # Send registration success email
        email = serialized_participant_obj.get('email')
        participant_name = serialized_participant_obj.get('name')
        course_id = serialized_participant_obj.get('course').get('id')

        send_registration_success_mail(email, course_id, participant_name)
        send_participant_details(email, course_id, serialized_participant_obj)
        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)

    @decorators.action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None, *args, **kwargs):
        """
        Approve a participant: sets status to ACCEPTED and sends course-based email.
        For ZK courses, includes a payment link in the email.
        """
        try:
            participant_object = self.get_queryset().get(pk=pk)
        except models.Participant.DoesNotExist:
            return requestUtils.error_response("Participant not found", {}, http_status=status.HTTP_404_NOT_FOUND)

        # Update status to ACCEPTED
        participant_object.status = RegistrationStatus.ACCEPTED.value
        participant_object.save()
        # Invalidate cache when participant is updated
        invalidate_participant_cache()

        # Send course-based approval email (ZK includes payment link)
        payment_link = "https://payment.web3bridgeafrica.com"
        send_approval_email(participant_object, payment_link=payment_link)

        serialized_participant_obj = self.serializer_class.Retrieve(participant_object).data
        return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(request_body=serializers.ParticipantSerializer.Update())
    def update(self, request, pk, *args, **kwargs): 
        participant_object= self.get_queryset().get(pk=pk)
        serializer = self.serializer_class.Update(participant_object, data=request.data)
        
        if serializer.is_valid():
            participant_obj= serializer.save()
            # Invalidate cache when participant is updated
            invalidate_participant_cache()
            serialized_participant_obj= self.serializer_class.Retrieve(participant_obj).data
            return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)
        else:
            return requestUtils.error_response("Error Updating Participant", serializer.errors, http_status=status.HTTP_400_BAD_REQUEST)
       
        
    def retrieve(self, request, pk, *args, **kwargs): 
        participant_object= self.get_queryset().get(pk=pk)
        serialized_participant_obj= self.serializer_class.Retrieve(participant_object).data
        return requestUtils.success_response(data=serialized_participant_obj, http_status=status.HTTP_200_OK)
    
    
    def destroy(self, request, pk, *args, **kwargs): 
        participant_object= self.get_queryset().get(pk=pk)
        participant_object.delete()
        # Invalidate cache when participant is deleted
        invalidate_participant_cache()
        return requestUtils.success_response(data={}, http_status=status.HTTP_200_OK)
    
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        """
        Optimized participant listing endpoint with:
        - Redis caching
        - Optimized pagination (no expensive count query)
        - Query optimization (select_related/prefetch_related)
        - Ordering by newest first
        """
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 50))
        
        # Ensure limit doesn't exceed 200 for performance
        limit = min(limit, 200)
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Create cache key based on page and limit
        cache_key = f'participants_all_page_{page}_limit_{limit}'
        
        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return requestUtils.success_response(
                data=cached_data,
                http_status=status.HTTP_200_OK
            )
        
        # Get optimized queryset
        queryset = self.get_queryset()
        
        # Get one extra item to check if there's a next page (without expensive count)
        paginated_queryset = queryset[offset:offset + limit + 1]
        
        # Check if there's a next page
        has_next = len(paginated_queryset) > limit
        if has_next:
            paginated_queryset = paginated_queryset[:limit]  # Remove the extra item
        
        # Serialize the data
        serializer = self.serializer_class.List(paginated_queryset, many=True)
        
        # Calculate pagination info without expensive count query
        has_previous = page > 1
        
        response_data = {
            'results': serializer.data,
            'pagination': {
                'current_page': page,
                'limit': limit,
                'has_next': has_next,
                'has_previous': has_previous,
                'next_page': page + 1 if has_next else None,
                'previous_page': page - 1 if has_previous else None,
                # Don't include total_count or total_pages to avoid expensive queries
            }
        }
        
        # Cache the response for 10 minutes (configurable)
        cache_timeout = getattr(settings, 'PARTICIPANT_CACHE_TIMEOUT', 600)
        cache.set(cache_key, response_data, cache_timeout)
        
        return requestUtils.success_response(
            data=response_data,
            http_status=status.HTTP_200_OK
        )
    
    
    @decorators.action(detail=True, methods=["get"])
    def registration(self, request, pk):
        """
        Get participants by registration ID with optimization
        """
        queryset = self.get_queryset().filter(registration=pk)
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"], url_path="stream")
    def stream(self, request):
        """
        Streaming endpoint for large datasets.
        Returns data in chunks using Server-Sent Events (SSE) or JSON streaming.
        This is optimized for fetching thousands of participants without timeout.
        """
        from django.http import StreamingHttpResponse
        
        # Get parameters
        chunk_size = int(request.GET.get('chunk_size', 100))
        registration_id = request.GET.get('registration', None)
        course_id = request.GET.get('course', None)
        
        # Build optimized queryset
        queryset = self.get_queryset()
        
        if registration_id:
            queryset = queryset.filter(registration_id=registration_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        def generate():
            """Generator function that yields JSON chunks"""
            # Send initial metadata
            yield '{"status": "started", "chunk_size": ' + str(chunk_size) + '}\n'
            
            # Process in chunks
            offset = 0
            total_sent = 0
            
            while True:
                # Get chunk
                chunk = queryset[offset:offset + chunk_size]
                chunk_list = list(chunk)
                
                if not chunk_list:
                    break
                
                # Serialize chunk
                serializer = self.serializer_class.List(chunk_list, many=True)
                chunk_data = serializer.data
                
                # Yield chunk as JSON
                yield json.dumps({
                    'chunk': chunk_data,
                    'offset': offset,
                    'count': len(chunk_data),
                    'total_sent': total_sent + len(chunk_data)
                }) + '\n'
                
                offset += chunk_size
                total_sent += len(chunk_data)
                
                # If we got fewer items than chunk_size, we're done
                if len(chunk_list) < chunk_size:
                    break
            
            # Send completion message
            yield json.dumps({
                'status': 'completed',
                'total_sent': total_sent
            }) + '\n'
        
        response = StreamingHttpResponse(
            generate(),
            content_type='application/x-ndjson'  # Newline-delimited JSON
        )
        response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
        return response

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
            recipient_ids = serializer.validated_data['recipients']  # Already validated as integers
            from_admission = request.data.get('from_admission', False)  # New parameter
            
            if not recipient_ids:
                return Response({"message": "No recipients provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Send email asynchronously in background to avoid timeout
            print(f"[API] Bulk email request received")
            print(f"[API] Subject: {subject}")
            print(f"[API] Recipient IDs: {recipient_ids}")
            print(f"[API] From admission: {from_admission}")
            print(f"[API] Starting background thread...")
            
            thread = threading.Thread(
                target=send_bulk_email,
                args=(subject, html_body, recipient_ids, from_admission),
                daemon=True
            )
            thread.start()
            print(f"[API] Background thread started, returning 200 response")
            
            # Return immediately
            return Response({
                "message": "Email sending initiated",
                "recipient_count": len(recipient_ids)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=serializers.BulkEmailSerializer)
    @decorators.action(detail=False, methods=["post"], url_path="send-admission-email")
    def send_admission_bulk_email(self, request):
        """Send bulk emails from admission@web3bridge.com"""
        serializer = serializers.BulkEmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            html_body = serializer.validated_data['body']
            recipient_ids = serializer.validated_data['recipients']  # Already validated as integers
            
            if not recipient_ids:
                return Response({"message": "No recipients provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Send email asynchronously in background to avoid timeout
            print(f"[API] Admission bulk email request received")
            print(f"[API] Subject: {subject}")
            print(f"[API] Recipient IDs: {recipient_ids}")
            print(f"[API] Starting background thread for admission emails...")
            
            thread = threading.Thread(
                target=send_bulk_email,
                args=(subject, html_body, recipient_ids, True),
                daemon=True
            )
            thread.start()
            print(f"[API] Background thread started, returning 200 response")
            
            # Return immediately
            return Response({
                "message": "Admission email sending initiated",
                "recipient_count": len(recipient_ids)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
