from datetime import UTC, datetime
from urllib.parse import urlencode

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import (
    AccountState,
    AuditLog,
    CourseMaterial,
    GuarantorForm,
    Mentor,
    MentorAssessment,
    MentorCourseMap,
    UserRole,
    User,
)
from app.schemas.portal_management import (
    CourseMaterialCreateRequest,
    CourseMaterialResponse,
    CourseMaterialUpdateRequest,
    GuarantorFormCreateRequest,
    GuarantorFormResponse,
    GuarantorFormUpdateRequest,
    MentorAssessmentCreateRequest,
    MentorAssessmentResponse,
    MentorAssessmentUpdateRequest,
    MentorCreateRequest,
    MentorResponse,
    MentorUpdateRequest,
    InvitePortalUserRequest,
    InvitePortalUserResponse,
)
from app.services.auth import AuthService
from app.services.email import EmailService
from app.core.config import get_settings

settings = get_settings()


class PortalManagementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.auth_service = AuthService(session)
        self.email_service = EmailService()

    async def create_mentor(self, *, actor: User, payload: MentorCreateRequest) -> MentorResponse:
        mentor = Mentor(
            full_name=payload.full_name,
            email=payload.email.strip().lower(),
            bio=payload.bio,
            is_active=payload.is_active,
        )
        self.session.add(mentor)
        await self.session.flush()
        self._audit(actor=actor, action="mentor_created", resource_id=str(mentor.id))
        await self.session.commit()
        await self.session.refresh(mentor)
        return await self._mentor_response(mentor)

    async def invite_portal_user(
        self, *, actor: User, payload: InvitePortalUserRequest
    ) -> InvitePortalUserResponse:
        normalized_email = payload.email.strip().lower()
        allowed_roles = {
            UserRole.MENTOR.value,
            UserRole.GENERAL_ADMIN.value,
            UserRole.SYSTEM_ADMIN.value,
        }
        if payload.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Only mentor, general_admin, and system_admin can be invited here",
            )

        result = await self.session.execute(select(User).where(User.email == normalized_email))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(
                email=normalized_email,
                role=payload.role.value,
                account_state=AccountState.INVITED.value,
                email_verified=False,
            )
            self.session.add(user)
            await self.session.flush()
        else:
            user.role = payload.role.value
            if user.account_state not in {AccountState.SUSPENDED.value, AccountState.DEACTIVATED.value}:
                user.account_state = AccountState.INVITED.value
            user.email_verified = False

        if payload.role.value == UserRole.MENTOR.value:
            mentor_row = await self._get_mentor_by_user_id(user.id)
            if mentor_row is None:
                mentor_row = Mentor(
                    user_id=user.id,
                    full_name=payload.full_name,
                    email=normalized_email,
                    bio=payload.bio,
                    is_active=True,
                )
                self.session.add(mentor_row)
            else:
                mentor_row.full_name = payload.full_name
                mentor_row.email = normalized_email
                mentor_row.bio = payload.bio
                mentor_row.is_active = True

        activation_token = await self.auth_service.create_activation_token_for_user(user=user)
        query = urlencode({"token": activation_token})
        activation_url = f"{settings.PORTAL_FRONTEND_URL.rstrip('/')}/activate/onboard?{query}"
        await self.session.commit()

        self._audit(actor=actor, action="portal_user_invited", resource_id=str(user.id))
        await self.session.commit()

        await self.email_service.send_onboarding_email(
            to_email=normalized_email,
            student_name=payload.full_name,
            activation_url=activation_url,
        )

        return InvitePortalUserResponse(
            user_id=user.id,
            email=user.email,
            role=user.role,
            account_state=user.account_state,
            activation_url=activation_url,
        )

    async def list_mentors(self) -> list[MentorResponse]:
        result = await self.session.execute(select(Mentor).order_by(Mentor.id.desc()))
        return [await self._mentor_response(item) for item in result.scalars().all()]

    async def update_mentor(
        self, *, actor: User, mentor_id: int, payload: MentorUpdateRequest
    ) -> MentorResponse:
        mentor = await self._get_mentor(mentor_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(mentor, key, value)
        self._audit(actor=actor, action="mentor_updated", resource_id=str(mentor.id))
        await self.session.commit()
        await self.session.refresh(mentor)
        return await self._mentor_response(mentor)

    async def delete_mentor(self, *, actor: User, mentor_id: int) -> None:
        mentor = await self._get_mentor(mentor_id)
        await self.session.delete(mentor)
        self._audit(actor=actor, action="mentor_deleted", resource_id=str(mentor_id))
        await self.session.commit()

    async def assign_mentor_course(self, *, actor: User, mentor_id: int, course_id: int) -> MentorResponse:
        await self._get_mentor(mentor_id)
        result = await self.session.execute(
            select(MentorCourseMap).where(
                MentorCourseMap.mentor_id == mentor_id, MentorCourseMap.course_id == course_id
            )
        )
        row = result.scalar_one_or_none()
        if row is None:
            self.session.add(MentorCourseMap(mentor_id=mentor_id, course_id=course_id))
        self._audit(actor=actor, action="mentor_course_assigned", resource_id=f"{mentor_id}:{course_id}")
        await self.session.commit()
        mentor = await self._get_mentor(mentor_id)
        return await self._mentor_response(mentor)

    async def remove_mentor_course(self, *, actor: User, mentor_id: int, course_id: int) -> MentorResponse:
        await self.session.execute(
            delete(MentorCourseMap).where(
                MentorCourseMap.mentor_id == mentor_id, MentorCourseMap.course_id == course_id
            )
        )
        self._audit(actor=actor, action="mentor_course_removed", resource_id=f"{mentor_id}:{course_id}")
        await self.session.commit()
        mentor = await self._get_mentor(mentor_id)
        return await self._mentor_response(mentor)

    async def create_course_material(
        self, *, actor: User, payload: CourseMaterialCreateRequest
    ) -> CourseMaterialResponse:
        material = CourseMaterial(
            course_id=payload.course_id,
            title=payload.title,
            material_type=payload.material_type.value,
            resource_url=str(payload.resource_url) if payload.resource_url else None,
            content=payload.content,
            metadata_json=payload.metadata,
            uploaded_by=actor.id,
        )
        self.session.add(material)
        await self.session.commit()
        await self.session.refresh(material)
        return self._material_response(material)

    async def list_course_materials(self, *, course_id: int | None = None) -> list[CourseMaterialResponse]:
        statement = select(CourseMaterial).order_by(CourseMaterial.created_at.desc())
        if course_id is not None:
            statement = statement.where(CourseMaterial.course_id == course_id)
        result = await self.session.execute(statement)
        return [self._material_response(item) for item in result.scalars().all()]

    async def update_course_material(
        self, *, actor: User, material_id: int, payload: CourseMaterialUpdateRequest
    ) -> CourseMaterialResponse:
        material = await self._get_material(material_id)
        updates = payload.model_dump(exclude_unset=True)
        if "material_type" in updates and updates["material_type"] is not None:
            updates["material_type"] = updates["material_type"].value
        if "resource_url" in updates and updates["resource_url"] is not None:
            updates["resource_url"] = str(updates["resource_url"])
        if "metadata" in updates:
            updates["metadata_json"] = updates.pop("metadata")
        for key, value in updates.items():
            setattr(material, key, value)
        self._audit(actor=actor, action="course_material_updated", resource_id=str(material.id))
        await self.session.commit()
        await self.session.refresh(material)
        return self._material_response(material)

    async def delete_course_material(self, *, actor: User, material_id: int) -> None:
        material = await self._get_material(material_id)
        await self.session.delete(material)
        self._audit(actor=actor, action="course_material_deleted", resource_id=str(material_id))
        await self.session.commit()

    async def create_assessment(
        self, *, actor: User, payload: MentorAssessmentCreateRequest
    ) -> MentorAssessmentResponse:
        row = MentorAssessment(
            mentor_id=payload.mentor_id,
            course_id=payload.course_id,
            title=payload.title,
            special_prompt=payload.special_prompt,
            input_context=payload.input_context,
            generated_assessment=payload.generated_assessment,
            assessment_type=payload.assessment_type.value,
            evaluation_mode=payload.evaluation_mode.value,
            result_release_mode=payload.result_release_mode.value,
            accepted=payload.accepted,
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        self._audit(actor=actor, action="mentor_assessment_created", resource_id=str(row.id))
        return self._assessment_response(row)

    async def list_assessments(
        self, *, mentor_id: int | None = None, course_id: int | None = None
    ) -> list[MentorAssessmentResponse]:
        statement = select(MentorAssessment).order_by(MentorAssessment.created_at.desc())
        if mentor_id is not None:
            statement = statement.where(MentorAssessment.mentor_id == mentor_id)
        if course_id is not None:
            statement = statement.where(MentorAssessment.course_id == course_id)
        result = await self.session.execute(statement)
        return [self._assessment_response(item) for item in result.scalars().all()]

    async def update_assessment(
        self, *, actor: User, assessment_id: int, payload: MentorAssessmentUpdateRequest
    ) -> MentorAssessmentResponse:
        row = await self._get_assessment(assessment_id)
        updates = payload.model_dump(exclude_unset=True)
        for enum_field in ("assessment_type", "evaluation_mode", "result_release_mode"):
            if enum_field in updates and updates[enum_field] is not None:
                updates[enum_field] = updates[enum_field].value
        for key, value in updates.items():
            setattr(row, key, value)
        self._audit(actor=actor, action="mentor_assessment_updated", resource_id=str(row.id))
        await self.session.commit()
        await self.session.refresh(row)
        return self._assessment_response(row)

    async def release_assessment(self, *, actor: User, assessment_id: int) -> MentorAssessmentResponse:
        row = await self._get_assessment(assessment_id)
        row.released_at = datetime.now(UTC)
        self._audit(actor=actor, action="mentor_assessment_released", resource_id=str(row.id))
        await self.session.commit()
        await self.session.refresh(row)
        return self._assessment_response(row)

    async def create_guarantor_form(
        self, *, actor: User, payload: GuarantorFormCreateRequest
    ) -> GuarantorFormResponse:
        row = GuarantorForm(
            title=payload.title,
            form_url=str(payload.form_url),
            cohort=payload.cohort,
            is_active=payload.is_active,
            uploaded_by=actor.id,
        )
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return self._guarantor_response(row)

    async def list_guarantor_forms(self, *, cohort: str | None = None) -> list[GuarantorFormResponse]:
        statement = select(GuarantorForm).order_by(GuarantorForm.created_at.desc())
        if cohort:
            statement = statement.where(GuarantorForm.cohort == cohort)
        result = await self.session.execute(statement)
        return [self._guarantor_response(item) for item in result.scalars().all()]

    async def update_guarantor_form(
        self, *, actor: User, form_id: int, payload: GuarantorFormUpdateRequest
    ) -> GuarantorFormResponse:
        row = await self._get_guarantor_form(form_id)
        updates = payload.model_dump(exclude_unset=True)
        if "form_url" in updates and updates["form_url"] is not None:
            updates["form_url"] = str(updates["form_url"])
        for key, value in updates.items():
            setattr(row, key, value)
        self._audit(actor=actor, action="guarantor_form_updated", resource_id=str(row.id))
        await self.session.commit()
        await self.session.refresh(row)
        return self._guarantor_response(row)

    async def delete_guarantor_form(self, *, actor: User, form_id: int) -> None:
        row = await self._get_guarantor_form(form_id)
        await self.session.delete(row)
        self._audit(actor=actor, action="guarantor_form_deleted", resource_id=str(form_id))
        await self.session.commit()

    async def _mentor_response(self, mentor: Mentor) -> MentorResponse:
        result = await self.session.execute(
            select(MentorCourseMap.course_id).where(MentorCourseMap.mentor_id == mentor.id)
        )
        return MentorResponse(
            id=mentor.id,
            full_name=mentor.full_name,
            email=mentor.email,
            bio=mentor.bio,
            is_active=mentor.is_active,
            created_at=mentor.created_at,
            updated_at=mentor.updated_at,
            course_ids=list(result.scalars().all()),
        )

    @staticmethod
    def _material_response(material: CourseMaterial) -> CourseMaterialResponse:
        return CourseMaterialResponse(
            id=material.id,
            course_id=material.course_id,
            title=material.title,
            material_type=material.material_type,
            resource_url=material.resource_url,
            content=material.content,
            metadata=material.metadata_json or {},
            created_at=material.created_at,
            updated_at=material.updated_at,
        )

    @staticmethod
    def _assessment_response(row: MentorAssessment) -> MentorAssessmentResponse:
        return MentorAssessmentResponse(
            id=row.id,
            mentor_id=row.mentor_id,
            course_id=row.course_id,
            title=row.title,
            special_prompt=row.special_prompt,
            input_context=row.input_context or {},
            assessment_type=row.assessment_type,
            evaluation_mode=row.evaluation_mode,
            result_release_mode=row.result_release_mode,
            generated_assessment=row.generated_assessment or {},
            accepted=row.accepted,
            released_at=row.released_at,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    @staticmethod
    def _guarantor_response(row: GuarantorForm) -> GuarantorFormResponse:
        return GuarantorFormResponse(
            id=row.id,
            title=row.title,
            form_url=row.form_url,
            cohort=row.cohort,
            is_active=row.is_active,
            uploaded_by=row.uploaded_by,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def _get_mentor(self, mentor_id: int) -> Mentor:
        result = await self.session.execute(select(Mentor).where(Mentor.id == mentor_id))
        mentor = result.scalar_one_or_none()
        if mentor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor not found")
        return mentor

    async def _get_mentor_by_user_id(self, user_id: int) -> Mentor | None:
        result = await self.session.execute(select(Mentor).where(Mentor.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_material(self, material_id: int) -> CourseMaterial:
        result = await self.session.execute(select(CourseMaterial).where(CourseMaterial.id == material_id))
        row = result.scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course material not found")
        return row

    async def _get_assessment(self, assessment_id: int) -> MentorAssessment:
        result = await self.session.execute(select(MentorAssessment).where(MentorAssessment.id == assessment_id))
        row = result.scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")
        return row

    async def _get_guarantor_form(self, form_id: int) -> GuarantorForm:
        result = await self.session.execute(select(GuarantorForm).where(GuarantorForm.id == form_id))
        row = result.scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guarantor form not found")
        return row

    def _audit(self, *, actor: User, action: str, resource_id: str) -> None:
        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action=action,
                resource_type="portal_management",
                resource_id=resource_id,
                created_at=datetime.now(UTC),
            )
        )
