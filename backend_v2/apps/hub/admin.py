from django.contrib import admin
from .models import HubRegistration, HubSpace, CheckIn


@admin.register(HubSpace)
class HubSpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_capacity', 'current_occupancy', 'available_spaces', 'occupancy_percentage', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'available_spaces', 'occupancy_percentage']
    ordering = ['-created_at']


@admin.register(HubRegistration)
class HubRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'location', 'role', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'role']
    search_fields = ['name', 'email', 'phone_number', 'location']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    actions = ['approve_registrations', 'reject_registrations']
    
    def approve_registrations(self, request, queryset):
        queryset.update(status=HubRegistration.APPROVED)
        self.message_user(request, f"{queryset.count()} registration(s) approved.")
    approve_registrations.short_description = "Approve selected registrations"
    
    def reject_registrations(self, request, queryset):
        queryset.update(status=HubRegistration.REJECTED)
        self.message_user(request, f"{queryset.count()} registration(s) rejected.")
    reject_registrations.short_description = "Reject selected registrations"


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ['registration', 'space', 'status', 'check_in_time', 'check_out_time', 'created_at']
    list_filter = ['status', 'space', 'check_in_time', 'created_at']
    search_fields = ['registration__name', 'registration__email', 'purpose']
    readonly_fields = ['created_at', 'updated_at', 'check_in_time']
    ordering = ['-check_in_time']
    date_hierarchy = 'check_in_time'
    
    actions = ['check_out_selected']
    
    def check_out_selected(self, request, queryset):
        """Bulk check out action"""
        count = 0
        for checkin in queryset.filter(status=CheckIn.CHECKED_IN):
            if checkin.check_out():
                count += 1
        self.message_user(request, f"{count} visitor(s) checked out successfully.")
    check_out_selected.short_description = "Check out selected visitors"

