from .assessments import router as assessments_router
from .auth import router as auth_router
from .courses import router as courses_router
from .dashboard import router as dashboard_router
from .discord import router as discord_router
from .health import router as health_router
from .notifications import router as notifications_router
from .onboarding import router as onboarding_router
from .portal_management import router as portal_management_router
from .profile import router as profile_router
from .sync import router as sync_router
from .students import router as students_router
from .updates import router as updates_router

__all__ = [
    "assessments_router",
    "auth_router",
    "courses_router",
    "dashboard_router",
    "discord_router",
    "health_router",
    "notifications_router",
    "onboarding_router",
    "portal_management_router",
    "profile_router",
    "sync_router",
    "students_router",
    "updates_router",
]
