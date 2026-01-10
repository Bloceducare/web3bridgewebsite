from django.contrib import admin
from .models import Course, Registration, Participant, Testimonial, ApprovedWeb3Participant

# Register your models here.
admin.site.register(Course)
admin.site.register(Registration)
admin.site.register(Participant)
admin.site.register(Testimonial)


@admin.register(ApprovedWeb3Participant)
class ApprovedWeb3ParticipantAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_name', 'get_cohort', 'participant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('email', 'participant__name', 'participant__email')
    readonly_fields = ('created_at', 'updated_at', 'get_name', 'get_cohort')
    ordering = ['-created_at']
    fields = ('participant', 'email', 'notes', 'get_name', 'get_cohort', 'created_at', 'updated_at')
    
    def get_name(self, obj):
        return obj.name or 'N/A'
    get_name.short_description = 'Name'
    
    def get_cohort(self, obj):
        return obj.cohort or 'N/A'
    get_cohort.short_description = 'Cohort'