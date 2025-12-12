from rest_framework import decorators, status, viewsets
from django.db.models import Q, Count
from . import serializers, models
from utils.helpers.requests import Utils as requestUtils
from drf_yasg.utils import swagger_auto_schema
from utils.helpers.mixins import GuestReadAllWriteAdminOnlyPermissionMixin


class HubSpaceViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.HubSpace.objects.all()
    serializer_class = serializers.HubSpaceSerializer
    admin_actions = ["create", "update", "destroy"]
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request, *args, **kwargs):
        """Get all hub spaces"""
        queryset = self.queryset.filter(is_active=True).order_by('-created_at')
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs):
        """Get a specific hub space"""
        try:
            hub_space_obj = self.queryset.get(pk=pk)
            serializer = self.serializer_class.Retrieve(hub_space_obj)
            return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
        except models.HubSpace.DoesNotExist:
            return requestUtils.error_response(
                "Hub Space not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    @swagger_auto_schema(request_body=serializers.HubSpaceSerializer.Update)
    def update(self, request, pk, *args, **kwargs):
        """Update hub space (admin only)"""
        try:
            hub_space_obj = self.queryset.get(pk=pk)
            serializer = self.serializer_class.Update(hub_space_obj, data=request.data)
            
            if serializer.is_valid():
                updated_obj = serializer.save()
                serialized_obj = self.serializer_class.Retrieve(updated_obj).data
                return requestUtils.success_response(
                    data=serialized_obj, 
                    http_status=status.HTTP_200_OK
                )
            
            return requestUtils.error_response(
                "Error Updating Hub Space", 
                serializer.errors, 
                http_status=status.HTTP_400_BAD_REQUEST
            )
        except models.HubSpace.DoesNotExist:
            return requestUtils.error_response(
                "Hub Space not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    @decorators.action(detail=False, methods=["get"])
    def stats(self, request, *args, **kwargs):
        """Get hub space statistics"""
        spaces = self.queryset.filter(is_active=True)
        total_capacity = sum(space.total_capacity for space in spaces)
        total_occupancy = sum(space.current_occupancy for space in spaces)
        total_available = total_capacity - total_occupancy
        
        stats = {
            "total_spaces": spaces.count(),
            "total_capacity": total_capacity,
            "total_occupancy": total_occupancy,
            "total_available": total_available,
            "occupancy_percentage": (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0,
        }
        
        return requestUtils.success_response(data=stats, http_status=status.HTTP_200_OK)


class HubRegistrationViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.HubRegistration.objects.all()
    serializer_class = serializers.HubRegistrationSerializer
    admin_actions = ["list", "retrieve", "update", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.HubRegistrationSerializer.Create)
    def create(self, request, *args, **kwargs):
        """Create a new hub registration"""
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            hub_registration_obj = serializer.save()
            serialized_obj = self.serializer_class.Retrieve(hub_registration_obj).data
            return requestUtils.success_response(
                data=serialized_obj, 
                http_status=status.HTTP_201_CREATED
            )
        
        return requestUtils.error_response(
            "Error Creating Hub Registration", 
            serializer.errors, 
            http_status=status.HTTP_400_BAD_REQUEST
        )
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request, *args, **kwargs):
        """Get all hub registrations"""
        queryset = self.queryset.all().order_by('-created_at')
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs):
        """Get a specific hub registration"""
        try:
            hub_registration_obj = self.queryset.get(pk=pk)
            serializer = self.serializer_class.Retrieve(hub_registration_obj)
            return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
        except models.HubRegistration.DoesNotExist:
            return requestUtils.error_response(
                "Hub Registration not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    @swagger_auto_schema(request_body=serializers.HubRegistrationSerializer.Update)
    def update(self, request, pk, *args, **kwargs):
        """Update hub registration (admin only) - for approving/rejecting"""
        try:
            hub_registration_obj = self.queryset.get(pk=pk)
            serializer = self.serializer_class.Update(hub_registration_obj, data=request.data)
            
            if serializer.is_valid():
                updated_obj = serializer.save()
                serialized_obj = self.serializer_class.Retrieve(updated_obj).data
                return requestUtils.success_response(
                    data=serialized_obj, 
                    http_status=status.HTTP_200_OK
                )
            
            return requestUtils.error_response(
                "Error Updating Hub Registration", 
                serializer.errors, 
                http_status=status.HTTP_400_BAD_REQUEST
            )
        except models.HubRegistration.DoesNotExist:
            return requestUtils.error_response(
                "Hub Registration not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    def destroy(self, request, pk, *args, **kwargs):
        """Delete a hub registration (admin only)"""
        try:
            hub_registration_obj = self.queryset.get(pk=pk)
            hub_registration_obj.delete()
            return requestUtils.success_response(
                data={"message": "Hub Registration deleted successfully"}, 
                http_status=status.HTTP_200_OK
            )
        except models.HubRegistration.DoesNotExist:
            return requestUtils.error_response(
                "Hub Registration not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    @decorators.action(detail=False, methods=["get"])
    def stats(self, request, *args, **kwargs):
        """Get registration statistics (admin only)"""
        total = self.queryset.count()
        pending = self.queryset.filter(status='pending').count()
        approved = self.queryset.filter(status='approved').count()
        rejected = self.queryset.filter(status='rejected').count()
        
        stats = {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        }
        
        return requestUtils.success_response(data=stats, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def by_status(self, request, *args, **kwargs):
        """Get registrations by status (admin only)"""
        status_filter = request.query_params.get('status', None)
        if status_filter:
            queryset = self.queryset.filter(status=status_filter).order_by('-created_at')
        else:
            queryset = self.queryset.all().order_by('-created_at')
        
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)


class CheckInViewSet(GuestReadAllWriteAdminOnlyPermissionMixin, viewsets.ViewSet):
    queryset = models.CheckIn.objects.all()
    serializer_class = serializers.CheckInSerializer
    admin_actions = ["list", "retrieve", "destroy"]
    
    @swagger_auto_schema(request_body=serializers.CheckInSerializer.Create)
    def create(self, request, *args, **kwargs):
        """Check in a visitor"""
        serializer = self.serializer_class.Create(data=request.data)
        
        if serializer.is_valid():
            checkin_obj = serializer.save()
            serialized_obj = self.serializer_class.Retrieve(checkin_obj).data
            return requestUtils.success_response(
                data=serialized_obj, 
                http_status=status.HTTP_201_CREATED
            )
        
        return requestUtils.error_response(
            "Error Checking In", 
            serializer.errors, 
            http_status=status.HTTP_400_BAD_REQUEST
        )
    
    @decorators.action(detail=False, methods=["get"])
    def all(self, request, *args, **kwargs):
        """Get all check-ins (admin only)"""
        queryset = self.queryset.all().order_by('-check_in_time')
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    @decorators.action(detail=False, methods=["get"])
    def active(self, request, *args, **kwargs):
        """Get all currently checked-in visitors"""
        queryset = self.queryset.filter(status=models.CheckIn.CHECKED_IN).order_by('-check_in_time')
        serializer = self.serializer_class.List(queryset, many=True)
        return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk, *args, **kwargs):
        """Get a specific check-in"""
        try:
            checkin_obj = self.queryset.get(pk=pk)
            serializer = self.serializer_class.Retrieve(checkin_obj)
            return requestUtils.success_response(data=serializer.data, http_status=status.HTTP_200_OK)
        except models.CheckIn.DoesNotExist:
            return requestUtils.error_response(
                "Check-in not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    @decorators.action(detail=True, methods=["post"])
    def check_out(self, request, pk, *args, **kwargs):
        """Check out a visitor"""
        try:
            checkin_obj = self.queryset.get(pk=pk)
            
            if checkin_obj.status == models.CheckIn.CHECKED_OUT:
                return requestUtils.error_response(
                    "Visitor is already checked out", 
                    {}, 
                    http_status=status.HTTP_400_BAD_REQUEST
                )
            
            success = checkin_obj.check_out()
            
            if success:
                serialized_obj = self.serializer_class.Retrieve(checkin_obj).data
                return requestUtils.success_response(
                    data=serialized_obj, 
                    http_status=status.HTTP_200_OK
                )
            else:
                return requestUtils.error_response(
                    "Error checking out", 
                    {}, 
                    http_status=status.HTTP_400_BAD_REQUEST
                )
        except models.CheckIn.DoesNotExist:
            return requestUtils.error_response(
                "Check-in not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    @decorators.action(detail=False, methods=["post"])
    def check_out_by_registration(self, request, *args, **kwargs):
        """Check out by registration ID"""
        registration_id = request.data.get('registration_id')
        
        if not registration_id:
            return requestUtils.error_response(
                "registration_id is required", 
                {}, 
                http_status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            checkin_obj = self.queryset.filter(
                registration_id=registration_id,
                status=models.CheckIn.CHECKED_IN
            ).first()
            
            if not checkin_obj:
                return requestUtils.error_response(
                    "No active check-in found for this registration", 
                    {}, 
                    http_status=status.HTTP_404_NOT_FOUND
                )
            
            success = checkin_obj.check_out()
            
            if success:
                serialized_obj = self.serializer_class.Retrieve(checkin_obj).data
                return requestUtils.success_response(
                    data=serialized_obj, 
                    http_status=status.HTTP_200_OK
                )
            else:
                return requestUtils.error_response(
                    "Error checking out", 
                    {}, 
                    http_status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return requestUtils.error_response(
                "Error checking out", 
                {"error": str(e)}, 
                http_status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk, *args, **kwargs):
        """Delete a check-in (admin only)"""
        try:
            checkin_obj = self.queryset.get(pk=pk)
            
            # If checked in, decrease occupancy before deleting
            if checkin_obj.status == models.CheckIn.CHECKED_IN and checkin_obj.space:
                checkin_obj.space.current_occupancy = max(0, checkin_obj.space.current_occupancy - 1)
                checkin_obj.space.save()
            
            checkin_obj.delete()
            return requestUtils.success_response(
                data={"message": "Check-in deleted successfully"}, 
                http_status=status.HTTP_200_OK
            )
        except models.CheckIn.DoesNotExist:
            return requestUtils.error_response(
                "Check-in not found", 
                {}, 
                http_status=status.HTTP_404_NOT_FOUND
            )
    
    @decorators.action(detail=False, methods=["get"])
    def stats(self, request, *args, **kwargs):
        """Get check-in statistics (admin only)"""
        total = self.queryset.count()
        checked_in = self.queryset.filter(status=models.CheckIn.CHECKED_IN).count()
        checked_out = self.queryset.filter(status=models.CheckIn.CHECKED_OUT).count()
        
        # Get today's stats
        from django.utils import timezone
        from django.db.models import Count
        from datetime import timedelta
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_checkins = self.queryset.filter(check_in_time__gte=today_start).count()
        
        stats = {
            "total": total,
            "checked_in": checked_in,
            "checked_out": checked_out,
            "today_checkins": today_checkins,
        }
        
        return requestUtils.success_response(data=stats, http_status=status.HTTP_200_OK)

