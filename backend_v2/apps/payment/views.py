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
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    admin_actions = ["retrieve", "all"]

    def retrieve(self, request, pk=None):
        payment_object = self.queryset.get(pk=pk)
        serialized_payment_obj = self.serializer_class(payment_object)
        return requestUtils.success_response(data=serialized_payment_obj.data, http_status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=["get"])
    def all(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)


# Discount Code viewset
class DiscountCodeViewset(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    discount = models.DiscountCode
    queryset = models.DiscountCode.objects.all()
    serializer_class = serializers.DiscountCodeSerializer
    admin_actions = ["all", "generate", "retrieve", "destroy"]

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
                generated_codes = []

            for _ in range(quantity):
                code = self.discount.generate_code()
                discount = self.queryset.create(code=code)
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
        serializer = self.serializer_class(self.queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)

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
            discount_code_object = self.queryset.get(code=code)
            
            # Debug log
            print(f"Discount code status - is_used: {discount_code_object.is_used}, code: {code}, claimant: {discount_code_object.claimant}")

            # Check if code is already used by someone else
            if discount_code_object.is_used and discount_code_object.claimant:
                return requestUtils.error_response(
                    "Discount code already used",
                    {}, http_status=status.HTTP_403_FORBIDDEN
                )

            # Code is valid and available
            return requestUtils.success_response(
                data={
                    "message": "Code is valid.",
                    "percentage": float(discount_code_object.percentage) if discount_code_object.percentage is not None else None
                },
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
