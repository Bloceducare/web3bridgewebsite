from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, permissions, status, viewsets

from . import models, serializers
from utils.helpers.requests import Utils as requestUtils
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin

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
    def validate(self, data):
        input_serializer = serializers.ValidateCodeInputSerializer(
            data=data)
        if not input_serializer.is_valid():
            return requestUtils.error_response(
                "Invalid input format", input_serializer.errors, status.HTTP_400_BAD_REQUEST
            )

        try:
            code = data.get("code")
            claimant_email = data.get("email")
            discount_code_object = self.queryset.get(code=code)

            if discount_code_object.is_used:
                if discount_code_object.claimant == claimant_email:
                    return requestUtils.success_response(
                        "Code already used by this user.",
                        http_status=status.HTTP_200_OK
                    )
                else:
                    return requestUtils.error_response(
                        "Discount code already used by another user.",
                        str(e), http_status=status.HTTP_403_FORBIDDEN
                    )

            discount_code_object.is_used = True
            discount_code_object.claimant = claimant_email
            discount_code_object.save()

            serializer = self.serializer_class(discount_code_object)
            return requestUtils.success_response(
                data=serializer.data, http_status=status.HTTP_200_OK
            )
        except self.discount.DoesNotExist as e:
            return requestUtils.error_response(
                "Discount code not found", str(e), http_status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return requestUtils.error_response(
                "Error validating discount code", str(e), http_status=status.HTTP_400_BAD_REQUEST
            )
