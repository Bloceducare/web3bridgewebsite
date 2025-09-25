import string
import secrets


from django.db import models

# Models


# Payment

class Payment(models.Model):
    name = models.CharField(max_length=127, blank=True, null=True)
    email = models.EmailField(max_length=127, unique=False)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, blank=True, null=True)
    status = models.BooleanField()
    transaction_id = models.CharField(max_length=50, unique=True)
    transaction_ref = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'
        managed = False
        indexes = [
            models.Index(fields=['email'], name='payment_email_idx'),
            models.Index(fields=['transaction_id'],
                         name='payment_transaction_id_idx'),
            models.Index(fields=['transaction_ref'],
                         name='payment_transaction_ref_idx'),
        ]

    def __str__(self):
        return f"< {type(self).__name__} : ({self.transaction_id}) >"


# Discount Code

class DiscountCode(models.Model):
    code = models.CharField(max_length=16, unique=True)
    is_used = models.BooleanField(default=False)
    claimant = models.EmailField(max_length=127, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    offset = models.IntegerField(default=1, help_text="maximum number of users that can use the code")
    updated_at = models.DateTimeField(auto_now=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, help_text="Discount percentage (0-100)")

    @classmethod
    def generate_code(cls, length=5):
        while True:
            alphanum = string.ascii_uppercase + string.digits
            code = 'WEB3BRIDGE' + '-' + \
                ''.join(secrets.choice(alphanum) for _ in range(length))

            if not cls.objects.filter(code=code).exists():
                return code

    def get_usage_count(self):
        """Get the number of times this code has been used"""
        return self.usage_records.count()

    def get_remaining_uses(self):
        """Get the number of remaining uses for this code"""
        return max(0, self.offset - self.get_usage_count())

    def is_fully_used(self):
        """Check if the code has reached its usage limit"""
        return self.get_usage_count() >= self.offset

    def can_be_used_by(self, email):
        """Check if a specific email can use this code"""
        # Check if user has already used this code
        if self.usage_records.filter(user_email=email).exists():
            return False, "You have already used this discount code"
        
        # Check if code has remaining uses
        if self.is_fully_used():
            return False, "This discount code has reached its usage limit"
        
        return True, "Code is valid"

    def mark_usage(self, user_email, participant_id=None):
        """Mark the code as used by a specific user and update is_used if needed"""
        # Create usage record
        usage_record = self.usage_records.create(
            user_email=user_email,
            participant_id=participant_id
        )
        
        # Update is_used if usage count reaches offset
        if self.get_usage_count() >= self.offset:
            self.is_used = True
            self.save()
        
        return usage_record

    def __str__(self):
        return f"< {type(self).__name__} : ({self.created_at}) >"


class DiscountCodeUsage(models.Model):
    """Track individual usage of discount codes"""
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name='usage_records')
    user_email = models.EmailField(max_length=127)
    used_at = models.DateTimeField(auto_now_add=True)
    participant_id = models.IntegerField(null=True, blank=True, help_text="ID of the participant who used the code")

    class Meta:
        unique_together = ('discount_code', 'user_email')
        indexes = [
            models.Index(fields=['discount_code', 'user_email'], name='discount_usage_idx'),
            models.Index(fields=['user_email'], name='user_email_idx'),
        ]

    def __str__(self):
        return f"< {self.discount_code.code} used by {self.user_email} >"
