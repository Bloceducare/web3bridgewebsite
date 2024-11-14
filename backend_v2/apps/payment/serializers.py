from rest_framework import serializers
from payment import models

# Payment serializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "id", "name", "email", "phone_number", "amount",
            "currency", "status", "transaction_id",
            "transaction_ref", "created_at"
        ]
        read_only_fields = ["id", "created_at"]


# Discount Code serializers
class DiscountCodeSerializer(serializers.ModelSerializer):
    validity = serializers.SerializerMethodField()

    class Meta:
        model = models.DiscountCode
        fields = ["id", "code", "created_at",
                  "is_used", "validity", "claimant"]
        read_only_fields = ["id", "code", "created_at",
                            "is_used", "validity", "claimant"]

    def get_validity(self, obj):
        return "Valid" if not obj.is_used else "Invalid"


class GenerateCodeInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        min_value=1,
        max_value=100,
        default=1,
        help_text="Number of discount codes to generate (1-100)"
    )


class ValidateCodeInputSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=16,
        help_text="The discount code to validate"
    )
