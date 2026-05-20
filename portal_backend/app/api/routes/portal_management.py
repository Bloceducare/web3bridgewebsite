from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin_user, get_current_staff_or_admin_user
from app.db.session import get_db_session
from app.models.portal import User
from app.schemas.auth import MessageResponse
from app.schemas.onboarding import OnboardingInviteResponse
from app.schemas.portal_management import (
    CourseMaterialCreateRequest,
    CourseMaterialResponse,
    CourseMaterialStructuredResponse,
    CourseMaterialUpdateRequest,
    GuarantorFormCreateRequest,
    GuarantorFormResponse,
    GuarantorFormUpdateRequest,
    InvitePortalUserRequest,
    InvitePortalUserResponse,
    InviteStudentByEmailRequest,
    MentorAssessmentCreateRequest,
    MentorAssessmentResponse,
    MentorAssessmentUpdateRequest,
    MentorCourseAssignRequest,
    MentorCreateRequest,
    MentorResponse,
    MentorUpdateRequest,
)
from app.services.portal_management import PortalManagementService

router = APIRouter(prefix="/admin/portal", tags=["Portal Management"])


@router.post("/mentors", response_model=MentorResponse, status_code=status.HTTP_201_CREATED)
async def create_mentor(
    payload: MentorCreateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorResponse:
    return await PortalManagementService(db).create_mentor(actor=current_user, payload=payload)


@router.post("/users/invite", response_model=InvitePortalUserResponse, status_code=status.HTTP_201_CREATED)
async def invite_portal_user(
    payload: InvitePortalUserRequest,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> InvitePortalUserResponse:
    return await PortalManagementService(db).invite_portal_user(
        actor=current_user, payload=payload
    )


@router.post(
    "/users/invite/student",
    response_model=OnboardingInviteResponse,
    status_code=status.HTTP_200_OK,
    summary="Invite a student by email",
    description=(
        "Creates or updates the student onboarding record using the same logic as "
        "internal non-ZK onboarding, then sends an activation email when applicable. "
        "Requires staff or admin authentication (includes general_admin). "
        "Body is only `email`."
    ),
)
async def invite_student_by_email(
    payload: InviteStudentByEmailRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> OnboardingInviteResponse:
    return await PortalManagementService(db).invite_student_by_email(
        actor=current_user, email=str(payload.email)
    )


@router.get("/mentors", response_model=list[MentorResponse], status_code=status.HTTP_200_OK)
async def list_mentors(
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MentorResponse]:
    return await PortalManagementService(db).list_mentors()


@router.patch("/mentors/{mentor_id}", response_model=MentorResponse, status_code=status.HTTP_200_OK)
async def update_mentor(
    mentor_id: int,
    payload: MentorUpdateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorResponse:
    return await PortalManagementService(db).update_mentor(
        actor=current_user, mentor_id=mentor_id, payload=payload
    )


@router.delete("/mentors/{mentor_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_mentor(
    mentor_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MessageResponse:
    await PortalManagementService(db).delete_mentor(actor=current_user, mentor_id=mentor_id)
    return MessageResponse(detail="Mentor removed")


@router.post("/mentors/{mentor_id}/courses", response_model=MentorResponse, status_code=status.HTTP_200_OK)
async def assign_mentor_course(
    mentor_id: int,
    payload: MentorCourseAssignRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorResponse:
    return await PortalManagementService(db).assign_mentor_course(
        actor=current_user, mentor_id=mentor_id, course_id=payload.course_id
    )


@router.delete(
    "/mentors/{mentor_id}/courses/{course_id}",
    response_model=MentorResponse,
    status_code=status.HTTP_200_OK,
)
async def remove_mentor_course(
    mentor_id: int,
    course_id: int,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorResponse:
    return await PortalManagementService(db).remove_mentor_course(
        actor=current_user, mentor_id=mentor_id, course_id=course_id
    )


@router.post("/materials", response_model=CourseMaterialResponse, status_code=status.HTTP_201_CREATED)
async def create_course_material(
    payload: CourseMaterialCreateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> CourseMaterialResponse:
    return await PortalManagementService(db).create_course_material(actor=current_user, payload=payload)


@router.get("/materials", response_model=list[CourseMaterialStructuredResponse], status_code=status.HTTP_200_OK)
async def list_course_materials(
    course_id: int | None = Query(default=None),
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[CourseMaterialStructuredResponse]:
    rows = await PortalManagementService(db).list_course_materials(course_id=course_id)
    return [
        CourseMaterialStructuredResponse(
            id=row.id,
            course_id=row.course_id,
            title=row.title,
            material={
                "type": row.material_type,
                "resource_url": row.resource_url,
                "content": row.content,
                "metadata": row.metadata,
            },
        )
        for row in rows
    ]


@router.patch("/materials/{material_id}", response_model=CourseMaterialResponse, status_code=status.HTTP_200_OK)
async def update_course_material(
    material_id: int,
    payload: CourseMaterialUpdateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> CourseMaterialResponse:
    return await PortalManagementService(db).update_course_material(
        actor=current_user, material_id=material_id, payload=payload
    )


@router.delete("/materials/{material_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_course_material(
    material_id: int,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MessageResponse:
    await PortalManagementService(db).delete_course_material(actor=current_user, material_id=material_id)
    return MessageResponse(detail="Course material deleted")


@router.post("/assessments", response_model=MentorAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    payload: MentorAssessmentCreateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorAssessmentResponse:
    return await PortalManagementService(db).create_assessment(actor=current_user, payload=payload)


@router.get("/assessments", response_model=list[MentorAssessmentResponse], status_code=status.HTTP_200_OK)
async def list_assessments(
    mentor_id: int | None = Query(default=None),
    course_id: int | None = Query(default=None),
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[MentorAssessmentResponse]:
    return await PortalManagementService(db).list_assessments(mentor_id=mentor_id, course_id=course_id)


@router.patch("/assessments/{assessment_id}", response_model=MentorAssessmentResponse, status_code=status.HTTP_200_OK)
async def update_assessment(
    assessment_id: int,
    payload: MentorAssessmentUpdateRequest,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorAssessmentResponse:
    return await PortalManagementService(db).update_assessment(
        actor=current_user, assessment_id=assessment_id, payload=payload
    )


@router.post("/assessments/{assessment_id}/release", response_model=MentorAssessmentResponse, status_code=status.HTTP_200_OK)
async def release_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MentorAssessmentResponse:
    return await PortalManagementService(db).release_assessment(
        actor=current_user, assessment_id=assessment_id
    )


@router.post("/guarantor-forms", response_model=GuarantorFormResponse, status_code=status.HTTP_201_CREATED)
async def create_guarantor_form(
    payload: GuarantorFormCreateRequest,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> GuarantorFormResponse:
    return await PortalManagementService(db).create_guarantor_form(actor=current_user, payload=payload)


@router.get("/guarantor-forms", response_model=list[GuarantorFormResponse], status_code=status.HTTP_200_OK)
async def list_guarantor_forms(
    cohort: str | None = Query(default=None),
    _: User = Depends(get_current_staff_or_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> list[GuarantorFormResponse]:
    return await PortalManagementService(db).list_guarantor_forms(cohort=cohort)


@router.patch("/guarantor-forms/{form_id}", response_model=GuarantorFormResponse, status_code=status.HTTP_200_OK)
async def update_guarantor_form(
    form_id: int,
    payload: GuarantorFormUpdateRequest,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> GuarantorFormResponse:
    return await PortalManagementService(db).update_guarantor_form(
        actor=current_user, form_id=form_id, payload=payload
    )


@router.delete("/guarantor-forms/{form_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def delete_guarantor_form(
    form_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db_session),
) -> MessageResponse:
    await PortalManagementService(db).delete_guarantor_form(actor=current_user, form_id=form_id)
    return MessageResponse(detail="Guarantor form deleted")
