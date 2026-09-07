from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_staff_or_admin_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.dashboard import AdminDashboardOverviewResponse
from app.schemas.dashboard_activity import MentorActivityResponse
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get(
    "/overview",
    response_model=AdminDashboardOverviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Get admin dashboard overview",
    description="Return aggregate metrics and recent students for the admin dashboard home page.",
)
async def get_admin_dashboard_overview(
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> AdminDashboardOverviewResponse:
    service = DashboardService(db)
    return await service.get_admin_overview()


@router.get(
    "/mentor-activity",
    response_model=list[MentorActivityResponse],
    status_code=status.HTTP_200_OK,
    summary="Get recent activities performed by mentors",
    description="Return recent log activities performed only by mentors. Staff or admin only.",
)
async def get_recent_mentor_activities(
    limit: int = Query(default=20, ge=1, le=100),
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MentorActivityResponse]:
    service = DashboardService(db)
    return await service.list_recent_mentor_activity(limit=limit)
