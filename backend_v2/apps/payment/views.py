from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
from . import models, serializers
from utils.helpers.requests import Utils as requestUtils
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin

# Static API key for demonstration - in production, this should be in environment variables
API_KEY = config("PAYMENT_API_KEY")

# Payment viewset


class PaymentViewset(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.Payment.objects.all().order_by('-created_at')
    serializer_class = serializers.PaymentSerializer
    admin_actions = ["retrieve", "all"]

    def retrieve(self, request, pk=None):
        payment_object = self.queryset.get(pk=pk)
        serialized_payment_obj = self.serializer_class(payment_object)
        return requestUtils.success_response(data=serialized_payment_obj.data, http_status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 25))  # Reduced default limit
        
        # Ensure limit doesn't exceed 50
        limit = min(limit, 50)
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Get paginated data (already ordered by created_at desc)
        # Get one extra item to check if there's a next page
        paginated_queryset = self.queryset[offset:offset + limit + 1]
        
        # Check if there's a next page
        has_next = len(paginated_queryset) > limit
        if has_next:
            paginated_queryset = paginated_queryset[:limit]  # Remove the extra item
        
        serializer = self.serializer_class(paginated_queryset, many=True)
        
        # Calculate pagination info without expensive count query
        has_previous = page > 1
        
        response_data = {
            "results": serializer.data,
            "pagination": {
                "current_page": page,
                "total_pages": None,  # Don't calculate total pages to avoid expensive count
                "total_count": None,  # Don't calculate total count to avoid expensive count
                "limit": limit,
                "has_next": has_next,
                "has_previous": has_previous,
                "next_page": page + 1 if has_next else None,
                "previous_page": page - 1 if has_previous else None
            }
        }
        
        return requestUtils.success_response(data=response_data, http_status=status.HTTP_200_OK)


# Discount Code viewset
class DiscountCodeViewset(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    discount = models.DiscountCode
    queryset = models.DiscountCode.objects.all().order_by('-created_at')
    serializer_class = serializers.DiscountCodeSerializer
    admin_actions = ["all", "generate", "generate_custom", "retrieve", "destroy", "mark_usage"]

    def get_permissions(self):
        if self.action == 'validate':
            return []
        return super().get_permissions()

    @swagger_auto_schema(
        request_body=serializers.GenerateCodeInputSerializer,
        responses={200: serializer_class(many=True)}
    )
    @decorators.action(detail=False, methods=["post"])
    def generate(self, request):
        try:
            input_serializer = serializers.GenerateCodeInputSerializer(
                data=request.data)
            if input_serializer.is_valid():
                quantity = input_serializer.validated_data.get("quantity")
                percentage = input_serializer.validated_data.get("percentage")
                generated_codes = []

                for _ in range(quantity):
                    code = self.discount.generate_code()
                    discount = self.queryset.create(
                        code=code,
                        percentage=percentage
                    )
                    generated_codes.append(discount)

                serialized_discount_code_obj = self.serializer_class(
                    generated_codes, many=True)

                return requestUtils.success_response(
                    data=serialized_discount_code_obj.data,
                    http_status=status.HTTP_201_CREATED
                )

        except Exception as e:
            return requestUtils.error_response(
                message="Error creating Discount Code",
                errors=str(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )
        
    @swagger_auto_schema(
        request_body=serializers.GenerateCustomCodeInputSerializer,
        responses={200: serializer_class}
    )
    @decorators.action(detail=False, methods=["post"])
    def generate_custom(self, request):
        try:
            input_serializer = serializers.GenerateCustomCodeInputSerializer(
                data=request.data)
            if input_serializer.is_valid():
                offset = input_serializer.validated_data.get("offset")
                percentage = input_serializer.validated_data.get("percentage")
                code = input_serializer.validated_data.get("code")
                discount = self.queryset.create(
                        code=code,
                        percentage=percentage,
                        offset=offset
                    )
                    
                serialized_discount_code_obj = self.serializer_class(
                    discount)
                
                return requestUtils.success_response(
                    data=serialized_discount_code_obj.data,
                    http_status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return requestUtils.error_response(
                message="Error generating custom code",
                errors=str(e),
                http_status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        discount_code_object = self.queryset.get(pk=pk)
        serialized_discount_code_obj = self.serializer_class(
            discount_code_object)
        return requestUtils.success_response(data=serialized_discount_code_obj.data, http_status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        discount_code_object = self.queryset.get(pk=pk)
        discount_code_object.delete()
        return requestUtils.success_response(data={}, http_status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 25))  # Reduced default limit
        
        # Ensure limit doesn't exceed 50
        limit = min(limit, 50)
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Get paginated data (already ordered by created_at desc)
        # Get one extra item to check if there's a next page
        paginated_queryset = self.queryset[offset:offset + limit + 1]
        
        # Check if there's a next page
        has_next = len(paginated_queryset) > limit
        if has_next:
            paginated_queryset = paginated_queryset[:limit]  # Remove the extra item
        
        serializer = self.serializer_class(paginated_queryset, many=True)
        
        # Calculate pagination info without expensive count query
        has_previous = page > 1
        
        response_data = {
            "results": serializer.data,
            "pagination": {
                "current_page": page,
                "total_pages": None,  # Don't calculate total pages to avoid expensive count
                "total_count": None,  # Don't calculate total count to avoid expensive count
                "limit": limit,
                "has_next": has_next,
                "has_previous": has_previous,
                "next_page": page + 1 if has_next else None,
                "previous_page": page - 1 if has_previous else None
            }
        }
        
        return requestUtils.success_response(data=response_data, http_status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=serializers.ValidateCodeInputSerializer,
        responses={200: serializer_class}
    )
    @decorators.action(detail=False, methods=["post"])
    def validate(self, request):
        input_serializer = serializers.ValidateCodeInputSerializer(
            data=request.data)
        if not input_serializer.is_valid():
            return requestUtils.error_response(
                "Invalid input format", input_serializer.errors, status.HTTP_400_BAD_REQUEST
            )
        data = request.data

        try:
            code = data.get("code")
            user_email = data.get("user_email")
            discount_code_object = self.queryset.get(code=code)
            
            # Debug log
            print(f"Discount code status - is_used: {discount_code_object.is_used}, code: {code}, claimant: {discount_code_object.claimant}, offset: {discount_code_object.offset}")

            # Handle legacy single-use codes (offset = 1)
            if discount_code_object.offset == 1:
                # Check if code is already used by someone else
                if discount_code_object.is_used and discount_code_object.claimant:
                    return requestUtils.error_response(
                        "Discount code already used",
                        {}, http_status=status.HTTP_403_FORBIDDEN
                    )
            else:
                # Handle multi-use codes
                if user_email:
                    can_use, message = discount_code_object.can_be_used_by(user_email)
                    if not can_use:
                        return requestUtils.error_response(
                            message,
                            {}, http_status=status.HTTP_403_FORBIDDEN
                        )
                else:
                    # If no email provided, just check if code has remaining uses
                    if discount_code_object.is_fully_used():
                        return requestUtils.error_response(
                            "This discount code has reached its usage limit",
                            {}, http_status=status.HTTP_403_FORBIDDEN
                        )

            # Code is valid and available
            response_data = {
                "message": "Code is valid.",
                "percentage": float(discount_code_object.percentage) if discount_code_object.percentage is not None else None,
                "offset": discount_code_object.offset,
                "usage_count": discount_code_object.get_usage_count(),
                "remaining_uses": discount_code_object.get_remaining_uses()
            }
            
            return requestUtils.success_response(
                data=response_data,
                http_status=status.HTTP_200_OK
            )

        except self.discount.DoesNotExist as e:
            return requestUtils.error_response(
                "Discount code not found", str(e), http_status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return requestUtils.error_response(
                "Error validating discount code", str(e), http_status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=serializers.MarkCodeUsageInputSerializer,
        responses={201: serializers.DiscountCodeUsageSerializer}
    )
    @decorators.action(detail=False, methods=["post"])
    def mark_usage(self, request):
        """Mark a discount code as used by a specific user"""
        input_serializer = serializers.MarkCodeUsageInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return requestUtils.error_response(
                "Invalid input format", input_serializer.errors, status.HTTP_400_BAD_REQUEST
            )
        
        data = request.data
        try:
            code = data.get("code")
            user_email = data.get("user_email")
            participant_id = data.get("participant_id")
            
            discount_code_object = self.queryset.get(code=code)
            
            # Check if user can use this code
            can_use, message = discount_code_object.can_be_used_by(user_email)
            if not can_use:
                return requestUtils.error_response(
                    message,
                    {}, http_status=status.HTTP_403_FORBIDDEN
                )
            
            # Use the model's mark_usage method
            usage_record = discount_code_object.mark_usage(user_email, participant_id)
            
            serialized_usage = serializers.DiscountCodeUsageSerializer(usage_record)
            
            return requestUtils.success_response(
                data={
                    "message": "Code usage recorded successfully",
                    "usage_record": serialized_usage.data,
                    "remaining_uses": discount_code_object.get_remaining_uses(),
                    "is_used": discount_code_object.is_used
                },
                http_status=status.HTTP_201_CREATED
            )
            
        except self.discount.DoesNotExist as e:
            return requestUtils.error_response(
                "Discount code not found", str(e), http_status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return requestUtils.error_response(
                "Error recording code usage", str(e), http_status=status.HTTP_400_BAD_REQUEST
            )

class APIGenerateDiscountCode(APIView):
    permission_classes = []  # No default permission required
    
    def check_api_key(self, request):
        api_key = request.headers.get('API-Key')
        if not api_key or api_key != API_KEY:
            return False
        return True
    
    @swagger_auto_schema(
        request_body=serializers.GenerateCodeInputSerializer,
        responses={201: serializers.DiscountCodeSerializer(many=True)}
    )
    def post(self, request):
        if not self.check_api_key(request):
            return Response(
                {"error": "Invalid or missing API key"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            input_serializer = serializers.GenerateCodeInputSerializer(data=request.data)
            if input_serializer.is_valid():
                quantity = input_serializer.validated_data.get("quantity")
                generated_codes = []

                for _ in range(quantity):
                    code = models.DiscountCode.generate_code()
                    discount = models.DiscountCode.objects.create(code=code)
                    generated_codes.append(discount)

                serialized_discount_code_obj = serializers.DiscountCodeSerializer(
                    generated_codes, many=True
                )

                return Response(
                    {
                        "status": "success",
                        "data": serialized_discount_code_obj.data
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"error": "Invalid input", "details": input_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": "Error creating Discount Code", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
