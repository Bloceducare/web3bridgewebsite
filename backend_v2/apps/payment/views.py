from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, permissions, status, viewsets
from rest_framework.permissions import IsAdminUser

from . import models, serializers
from utils.helpers.requests import Utils as requestUtils


# Payment viewset
class PaymentViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    admin_actions= ["create", "read", "update", "destroy"]
    permission_classes = [IsAdminUser]


# Discount Code viewset
class DiscountCodeViewset(viewsets.ViewSet):
    discount = models.DiscountCode
    queryset = models.DiscountCode.objects.all()
    serializer_class = serializers.DiscountCodeSerializer

    def get_permissions(self):
        if self.action == "validate":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @swagger_auto_schema(
        request_body=serializers.GenerateCodeInputSerializer,
        responses={200: serializer_class(many=True)}
    )
    @decorators.action(detail=False, methods=["post"])
    def generate(self, request):
        try:
            input_serializer = serializers.GenerateCodeInputSerializer(data=request.data)
            if input_serializer.is_valid():
                quantity = input_serializer.validated_data.get("quantity")
                generated_codes = []

            for _ in range(quantity):
                code = self.discount.generate_code()
                discount = self.queryset.create(code=code)
                generated_codes.append(discount)

            serialized_discount_code_obj = self.serializer_class(generated_codes, many=True)

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
        serialized_discount_code_obj = self.serializer_class(discount_code_object)
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
        try:
            input_serializer = serializers.ValidateCodeInputSerializer(data=request.data)
            if not input_serializer.is_valid():
                return requestUtils.error_response(
                    "Error validating discount code", str(e), http_status=status.HTTP_400_BAD_REQUEST
                )

            code = request.data.get("code")
            discount_code_object = self.queryset.get(code=code)
            serializer = self.serializer_class(discount_code_object)

            if discount_code_object.is_used:
                return requestUtils.error_response(
                    "Discount code invalid", http_status=status.HTTP_403_FORBIDDEN
                )

            discount_code_object.is_used = True
            discount_code_object.save()
            discount_code_object.delete()

            return requestUtils.success_response(
                data=serializer.data, http_status=status.HTTP_200_OK
            )
        except Exception as e:
            return requestUtils.error_response(
                "Error validating discount code", str(e), http_status=status.HTTP_400_BAD_REQUEST
            )


