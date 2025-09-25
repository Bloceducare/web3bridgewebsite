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
    usage_count = serializers.SerializerMethodField()
    remaining_uses = serializers.SerializerMethodField()
    usage_records = serializers.SerializerMethodField()

    class Meta:
        model = models.DiscountCode
        fields = ["id", "code", "created_at",
                  "is_used", "validity", "claimant", "percentage", "offset",
                  "usage_count", "remaining_uses", "usage_records"]
        read_only_fields = ["id", "code", "created_at",
                            "is_used", "validity", "claimant", "percentage", "offset",
                            "usage_count", "remaining_uses", "usage_records"]

    def get_validity(self, obj):
        if obj.offset == 1:
            # Legacy single-use codes
            return "Valid" if not obj.is_used else "Invalid"
        else:
            # Multi-use codes
            return "Valid" if not obj.is_fully_used() else "Invalid"

    def get_usage_count(self, obj):
        return obj.get_usage_count()

    def get_remaining_uses(self, obj):
        return obj.get_remaining_uses()

    def get_usage_records(self, obj):
        return DiscountCodeUsageSerializer(obj.usage_records.all(), many=True).data


class DiscountCodeUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DiscountCodeUsage
        fields = ["id", "user_email", "used_at", "participant_id"]
        read_only_fields = ["id", "used_at"]


class GenerateCodeInputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        min_value=1,
        max_value=100,
        default=1,
        help_text="Number of discount codes to generate (1-100)"
    )
    percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
        help_text="Discount percentage (0-100)"
    )

class GenerateCustomCodeInputSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=16,
        help_text="The discount code to generate"
    )
    offset = serializers.IntegerField(
        min_value=1,
        default=1,
        help_text="maximum number of users that can use the code"
    )
    percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
        help_text="Discount percentage (0-100)"
    )

class ValidateCodeInputSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=16,
        help_text="The discount code to validate"
    )
    user_email = serializers.EmailField(
        required=False,
        help_text="Email of the user trying to use the code (optional for backward compatibility)"
    )


class MarkCodeUsageInputSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=16,
        help_text="The discount code that was used"
    )
    user_email = serializers.EmailField(
        help_text="Email of the user who used the code"
    )
    participant_id = serializers.IntegerField(
        required=False,
        help_text="ID of the participant who used the code"
    )