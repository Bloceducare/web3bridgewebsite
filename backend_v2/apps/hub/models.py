from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.helpers.models import BaseModelBaseMixin


class HubSpace(BaseModelBaseMixin, models.Model):
    """Model for managing hub capacity and spaces"""
    name = models.CharField(_('space name'), max_length=255, blank=False, null=False, default="Main Hub")
    total_capacity = models.IntegerField(_('total capacity'), default=50, help_text="Total number of people the hub can accommodate")
    current_occupancy = models.IntegerField(_('current occupancy'), default=0, help_text="Current number of people in the hub")
    is_active = models.BooleanField(_('is active'), default=True, help_text="Whether this space is currently active")
    
    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hub Space"
        verbose_name_plural = "Hub Spaces"
    
    @property
    def available_spaces(self):
        """Calculate available spaces"""
        return max(0, self.total_capacity - self.current_occupancy)
    
    @property
    def occupancy_percentage(self):
        """Calculate occupancy percentage"""
        if self.total_capacity == 0:
            return 0
        return (self.current_occupancy / self.total_capacity) * 100
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name} - {self.current_occupancy}/{self.total_capacity}) >"


class HubRegistration(BaseModelBaseMixin, models.Model):
    """Model for Lagos Ethereum Community Hub registration"""
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    CHECKED_OUT = 'checked_out'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CHECKED_OUT, 'Checked Out'),
    ]
    
    name = models.CharField(_('full name'), max_length=255, blank=False, null=False)
    email = models.EmailField(_('email address'), max_length=255, blank=False, null=False)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=False, null=False)
    location = models.CharField(_('location'), max_length=255, blank=False, null=False, 
                                help_text="Where are you coming to the hub from")
    reason = models.TextField(_('reason'), blank=False, null=False,
                              help_text="Why do you want to come and use the hub")
    role = models.CharField(_('role'), max_length=255, blank=False, null=False,
                            help_text="Describe your role in the ecosystem (e.g. Developer, founder, creator…)")
    contribution = models.TextField(_('contribution'), blank=False, null=False,
                                   help_text="Please share how you contribute to Ethereum")
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(_('admin notes'), blank=True, null=True, help_text="Internal notes for admins")
    
    # Booking fields
    preferred_date = models.DateField(_('preferred date'), blank=True, null=True, 
                                      help_text="Preferred date for visiting the hub")
    preferred_time = models.TimeField(_('preferred time'), blank=True, null=True,
                                     help_text="Preferred time for visiting the hub")
    expected_duration_hours = models.IntegerField(_('expected duration hours'), default=4,
                                                  help_text="Expected duration of visit in hours")
    
    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hub Registration"
        verbose_name_plural = "Hub Registrations"
        indexes = [
            models.Index(fields=['-created_at'], name='hub_reg_created_at_idx'),
            models.Index(fields=['email'], name='hub_reg_email_idx'),
            models.Index(fields=['status'], name='hub_reg_status_idx'),
            models.Index(fields=['preferred_date', 'preferred_time'], name='hub_reg_date_time_idx'),
        ]
    
    def __str__(self):
        return f"< {type(self).__name__}({self.name} - {self.email} - {self.status}) >"


class CheckIn(BaseModelBaseMixin, models.Model):
    """Model for tracking check-ins and check-outs at the hub"""
    CHECKED_IN = 'checked_in'
    CHECKED_OUT = 'checked_out'
    
    STATUS_CHOICES = [
        (CHECKED_IN, 'Checked In'),
        (CHECKED_OUT, 'Checked Out'),
    ]
    
    registration = models.ForeignKey(
        HubRegistration, 
        on_delete=models.CASCADE, 
        related_name='check_ins',
        help_text="The registration this check-in belongs to"
    )
    space = models.ForeignKey(
        HubSpace,
        on_delete=models.SET_NULL,
        null=True,
        related_name='check_ins',
        help_text="The space being used"
    )
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=CHECKED_IN)
    check_in_time = models.DateTimeField(_('check in time'), auto_now_add=True)
    check_out_time = models.DateTimeField(_('check out time'), blank=True, null=True)
    purpose = models.TextField(_('purpose'), blank=True, null=True, help_text="Purpose of visit")
    notes = models.TextField(_('notes'), blank=True, null=True, help_text="Additional notes")
    
    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Check In"
        verbose_name_plural = "Check Ins"
        indexes = [
            models.Index(fields=['-check_in_time'], name='checkin_time_idx'),
            models.Index(fields=['status'], name='checkin_status_idx'),
            models.Index(fields=['registration'], name='checkin_registration_idx'),
        ]
        ordering = ['-check_in_time']
    
    def check_out(self):
        """Check out the visitor, update space occupancy, and mark registration as checked out"""
        if self.status == self.CHECKED_OUT:
            return False
        
        from django.utils import timezone
        self.status = self.CHECKED_OUT
        self.check_out_time = timezone.now()
        self.save()
        
        # Decrease space occupancy
        if self.space:
            self.space.current_occupancy = max(0, self.space.current_occupancy - 1)
            self.space.save()
        
        # Mark registration as checked out to prevent reuse
        if self.registration.status == self.registration.APPROVED:
            self.registration.status = self.registration.CHECKED_OUT
            self.registration.save()
        
        return True
    
    def __str__(self):
        return f"< {type(self).__name__}({self.registration.name} - {self.status} - {self.check_in_time}) >"


class BlockedDateRange(BaseModelBaseMixin, models.Model):
    """Model for managing blocked date ranges when hub is unavailable"""
    start_date = models.DateField(_('start date'), blank=False, null=False, 
                                  help_text="Start date of the blocked period (inclusive)")
    end_date = models.DateField(_('end date'), blank=False, null=False,
                                help_text="End date of the blocked period (inclusive)")
    reason = models.TextField(_('reason'), blank=True, null=True,
                             help_text="Reason for blocking these dates (e.g., 'Holiday', 'Maintenance', etc.)")
    is_active = models.BooleanField(_('is active'), default=True,
                                   help_text="Whether this blocked date range is currently active")
    
    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Blocked Date Range"
        verbose_name_plural = "Blocked Date Ranges"
        indexes = [
            models.Index(fields=['start_date', 'end_date'], name='blocked_date_range_idx'),
            models.Index(fields=['is_active'], name='blocked_date_range_active_idx'),
        ]
        ordering = ['start_date']
    
    def clean(self):
        """Validate that end_date is after start_date"""
        from django.core.exceptions import ValidationError
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after or equal to start date.")
    
    def save(self, *args, **kwargs):
        """Override save to run validation"""
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"< {type(self).__name__}({self.start_date} to {self.end_date} - {'Active' if self.is_active else 'Inactive'}) >"

