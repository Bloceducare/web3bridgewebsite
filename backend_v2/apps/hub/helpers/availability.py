"""
Helper functions for calculating hub availability based on bookings and capacity
"""
from django.utils import timezone
from datetime import datetime, timedelta, time as dt_time
from django.db.models import Q, Count, Sum
from .. import models


def get_available_slots(start_date=None, end_date=None, space_id=None):
    """
    Calculate available time slots for hub booking.
    Returns a list of available date/time combinations.
    
    Args:
        start_date: Start date for availability (default: today)
        end_date: End date for availability (default: 30 days from start)
        space_id: Optional specific space ID, otherwise checks all active spaces
    
    Returns:
        List of dicts with date, time, and available_spaces info
    """
    if start_date is None:
        start_date = timezone.now().date()
    
    if end_date is None:
        end_date = start_date + timedelta(days=30)
    
    # Get active spaces
    if space_id:
        spaces = models.HubSpace.objects.filter(id=space_id, is_active=True)
    else:
        spaces = models.HubSpace.objects.filter(is_active=True)
    
    if not spaces.exists():
        return []
    
    # Define available time slots (e.g., 9 AM to 6 PM, hourly)
    time_slots = [
        dt_time(9, 0),   # 9:00 AM
        dt_time(10, 0),  # 10:00 AM
        dt_time(11, 0),  # 11:00 AM
        dt_time(12, 0),  # 12:00 PM
        dt_time(13, 0),  # 1:00 PM
        dt_time(14, 0),  # 2:00 PM
        dt_time(15, 0),  # 3:00 PM
        dt_time(16, 0),  # 4:00 PM
        dt_time(17, 0),  # 5:00 PM
    ]
    
    available_slots = []
    current_date = start_date
    
    # Define blocked date range: from tomorrow until January 11th
    tomorrow = timezone.now().date() + timedelta(days=1)
    current_year = timezone.now().year
    january_11 = datetime(current_year, 1, 11).date()
    
    # If January 11th has already passed this year, use next year
    if january_11 < tomorrow:
        january_11 = datetime(current_year + 1, 1, 11).date()
    
    while current_date <= end_date:
        # Skip past dates
        if current_date < timezone.now().date():
            current_date += timedelta(days=1)
            continue
        
        # Skip dates from tomorrow until January 11th (inclusive)
        if tomorrow <= current_date <= january_11:
            current_date += timedelta(days=1)
            continue
        
        # Skip weekends (optional - can be made configurable)
        # if current_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
        #     current_date += timedelta(days=1)
        #     continue
        
        for time_slot in time_slots:
            # For today, skip past time slots
            if current_date == timezone.now().date():
                current_time = timezone.now().time()
                if time_slot < current_time:
                    continue
            
            # Calculate total capacity across all spaces
            total_capacity = sum(space.total_capacity for space in spaces)
            
            # Count bookings for this date/time slot
            slot_datetime = datetime.combine(current_date, time_slot)
            slot_end = slot_datetime + timedelta(hours=4)  # Default 4-hour duration
            
            # Convert to timezone-aware datetime for database queries
            from django.utils import timezone as tz
            slot_datetime_aware = tz.make_aware(slot_datetime) if tz.is_naive(slot_datetime) else slot_datetime
            slot_end_aware = tz.make_aware(slot_end) if tz.is_naive(slot_end) else slot_end
            
            # Count approved/pending registrations for this exact slot (booked but not checked in)
            slot_bookings = models.HubRegistration.objects.filter(
                preferred_date=current_date,
                preferred_time=time_slot,
                status__in=[models.HubRegistration.APPROVED, models.HubRegistration.PENDING]
            ).exclude(
                status=models.HubRegistration.REJECTED
            )
            booked_count = slot_bookings.count()
            
            # Count active check-ins that will overlap with this slot
            # These are people currently checked in or will be during this time
            overlapping_checkins = models.CheckIn.objects.filter(
                Q(status=models.CheckIn.CHECKED_IN) &
                (
                    # Check-ins that started before slot ends and haven't checked out yet
                    Q(check_in_time__lt=slot_end_aware) &
                    (Q(check_out_time__isnull=True) | Q(check_out_time__gt=slot_datetime_aware))
                )
            )
            
            # Also count check-ins scheduled for this exact slot (from registrations)
            scheduled_checkins = models.CheckIn.objects.filter(
                registration__preferred_date=current_date,
                registration__preferred_time=time_slot,
                status=models.CheckIn.CHECKED_IN
            )
            
            # Count unique people (by registration) that will occupy space during this slot
            active_checkin_count = overlapping_checkins.values('registration').distinct().count()
            scheduled_checkin_count = scheduled_checkins.values('registration').distinct().count()
            
            # Total occupied = currently checked in + booked (not yet checked in)
            # We use distinct registrations to avoid double counting
            total_occupied = active_checkin_count + booked_count
            
            # Available spots
            available = max(0, total_capacity - total_occupied)
            
            if available > 0:
                available_slots.append({
                    "date": current_date.isoformat(),
                    "time": time_slot.strftime("%H:%M"),
                    "datetime": slot_datetime.isoformat(),
                    "available_spaces": available,
                    "total_capacity": total_capacity,
                    "booked": booked_count,
                    "currently_occupied": active_checkin_count,
                })
        
        current_date += timedelta(days=1)
    
    return available_slots


def is_slot_available(date, time, space_id=None):
    """
    Check if a specific date/time slot is available.
    
    Args:
        date: Date object
        time: Time object
        space_id: Optional specific space ID
    
    Returns:
        dict with availability info
    """
    slots = get_available_slots(
        start_date=date,
        end_date=date,
        space_id=space_id
    )
    
    time_str = time.strftime("%H:%M")
    for slot in slots:
        if slot["date"] == date.isoformat() and slot["time"] == time_str:
            return {
                "available": True,
                "available_spaces": slot["available_spaces"],
                "total_capacity": slot["total_capacity"],
            }
    
    return {
        "available": False,
        "available_spaces": 0,
        "total_capacity": 0,
    }


def get_time_slots():
    """Get list of available time slots for the day"""
    return [
        {"value": "09:00", "label": "9:00 AM"},
        {"value": "10:00", "label": "10:00 AM"},
        {"value": "11:00", "label": "11:00 AM"},
        {"value": "12:00", "label": "12:00 PM"},
        {"value": "13:00", "label": "1:00 PM"},
        {"value": "14:00", "label": "2:00 PM"},
        {"value": "15:00", "label": "3:00 PM"},
        {"value": "16:00", "label": "4:00 PM"},
        {"value": "17:00", "label": "5:00 PM"},
    ]

