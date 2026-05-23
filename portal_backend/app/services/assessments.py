from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import and_, nulls_last, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.portal import (
    AssessmentResult,
    AuditLog,
    Mentor,
    MentorAssessment,
    ResultReleaseMode,
    StudentAssessmentStatus,
    User,
    UserRole,
)
from app.schemas.assessments import (
    AssessmentResultDetailResponse,
    MentorGradeRequest,
    MentorGradeResponse,
    PublishedAssessmentResponse,
    QuestionGradeBreakdown,
    SaveMentorAssessmentRequest,
    SaveMentorAssessmentResponse,
    StartAssessmentResponse,
    StudentAssessmentListItemResponse,
    SubmitAssessmentRequest,
    SubmitAssessmentResponse,
)
from app.services.assessment_grading import (
    SUBMISSION_GRACE_SECONDS,
    auto_grade_submission,
    questions_for_student,
    serialize_questions,
)


class AssessmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_mentor_assessment(
        self,
        *,
        actor: User | None,
        mentor_assessment_id: int,
        payload: SaveMentorAssessmentRequest,
        bypass_mentor_access: bool = False,
    ) -> SaveMentorAssessmentResponse:
        row = await self._get_mentor_assessment(mentor_assessment_id)
        if not bypass_mentor_access:
            if actor is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Mentor access required",
                )
            await self._ensure_mentor_access(actor=actor, mentor_assessment=row)

        questions = serialize_questions(payload.questions)
        if payload.title is not None:
            row.title = payload.title
        row.duration_minutes = payload.duration_minutes
        row.due_at = payload.due_at
        row.questions = questions
        row.total_questions = len(questions)
        if payload.assessment_type is not None:
            row.assessment_type = payload.assessment_type.value
        if payload.evaluation_mode is not None:
            row.evaluation_mode = payload.evaluation_mode.value
        if payload.result_release_mode is not None:
            row.result_release_mode = payload.result_release_mode.value
        if payload.accepted is not None:
            row.accepted = payload.accepted

        await self.session.commit()
        await self.session.refresh(row)

        return SaveMentorAssessmentResponse(
            mentor_assessment_id=row.id,
            title=row.title,
            duration_minutes=row.duration_minutes,
            due_at=row.due_at,
            total_questions=row.total_questions,
            questions=row.questions,
        )

    async def publish_assessment(
        self,
        *,
        actor: User,
        mentor_assessment_id: int,
    ) -> PublishedAssessmentResponse:
        row = await self._get_mentor_assessment(mentor_assessment_id)
        await self._ensure_mentor_access(actor=actor, mentor_assessment=row)

        if not row.questions:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Save assessment questions before publishing",
            )
        if row.due_at is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Set due_at before publishing",
            )

        row.released_at = datetime.now(UTC)
        row.accepted = True
        await self.session.commit()
        await self.session.refresh(row)

        return PublishedAssessmentResponse(
            id=row.id,
            course_id=row.course_id,
            title=row.title,
            due_at=row.due_at,
            duration_minutes=row.duration_minutes,
            total_questions=row.total_questions,
            released_at=row.released_at,
        )

    async def list_student_assessments(
        self,
        *,
        student: User,
        course_id: int | None = None,
    ) -> list[StudentAssessmentListItemResponse]:
        self._ensure_student_role(student)
        course_ids = await self._get_student_course_ids(student)
        if not course_ids:
            return []
        if course_id is not None:
            if course_id not in course_ids:
                return []
            course_ids = [course_id]

        statement = (
            select(MentorAssessment, AssessmentResult)
            .outerjoin(
                AssessmentResult,
                and_(
                    AssessmentResult.mentor_assessment_id == MentorAssessment.id,
                    AssessmentResult.user_id == student.id,
                ),
            )
            .where(
                MentorAssessment.released_at.is_not(None),
                MentorAssessment.course_id.in_(course_ids),
            )
            .order_by(
                nulls_last(MentorAssessment.due_at.asc()),
                MentorAssessment.released_at.desc(),
            )
        )
        rows = (await self.session.execute(statement)).all()
        now = datetime.now(UTC)
        return [
            self._student_assessment_list_item(
                assessment=assessment,
                result=result,
                now=now,
            )
            for assessment, result in rows
        ]

    async def start_assessment(
        self,
        *,
        student: User,
        mentor_assessment_id: int,
    ) -> StartAssessmentResponse:
        assessment = await self._get_released_assessment(mentor_assessment_id)
        self._ensure_student_role(student)
        now = datetime.now(UTC)
        if assessment.due_at and now > assessment.due_at:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assessment due date has passed",
            )

        result = await self._get_or_create_result(
            mentor_assessment_id=assessment.id,
            user_id=student.id,
        )
        if result.status in {
            StudentAssessmentStatus.SUBMITTED.value,
            StudentAssessmentStatus.GRADED.value,
        }:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Assessment already submitted",
            )

        if result.status == StudentAssessmentStatus.IN_PROGRESS.value and result.started_at:
            expires_at = result.expires_at
            if expires_at is None:
                expires_at = self._compute_expires_at(
                    started_at=result.started_at,
                    duration_minutes=assessment.duration_minutes,
                )
        else:
            result.status = StudentAssessmentStatus.IN_PROGRESS.value
            result.started_at = now
            result.expires_at = self._compute_expires_at(
                started_at=now,
                duration_minutes=assessment.duration_minutes,
            )
            await self.session.commit()
            await self.session.refresh(result)
            expires_at = result.expires_at

        if expires_at and now > expires_at:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assessment time window has expired",
            )

        return StartAssessmentResponse(
            result_id=result.id,
            mentor_assessment_id=assessment.id,
            started_at=result.started_at,
            expires_at=expires_at,
            duration_minutes=assessment.duration_minutes,
            questions=questions_for_student(assessment.questions),
        )

    async def submit_assessment(
        self,
        *,
        student: User,
        mentor_assessment_id: int,
        payload: SubmitAssessmentRequest,
    ) -> SubmitAssessmentResponse:
        assessment = await self._get_released_assessment(mentor_assessment_id)
        self._ensure_student_role(student)
        now = datetime.now(UTC)

        result = await self._get_result(
            mentor_assessment_id=assessment.id,
            user_id=student.id,
        )
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start the assessment before submitting",
            )
        if result.status in {
            StudentAssessmentStatus.SUBMITTED.value,
            StudentAssessmentStatus.GRADED.value,
        }:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Assessment already submitted",
            )
        if result.started_at is None or result.expires_at is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start the assessment before submitting",
            )
        if now > result.expires_at:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Submission window closed (duration plus 2 minute grace exceeded)",
            )

        answer_payload = [item.model_dump() for item in payload.answers]
        score, breakdown = auto_grade_submission(assessment.questions, answer_payload)
        max_score = len(assessment.questions)
        has_manual_items = any(not item.get("auto_graded") for item in breakdown)
        final_status = (
            StudentAssessmentStatus.GRADED.value
            if not has_manual_items
            else StudentAssessmentStatus.SUBMITTED.value
        )

        result.responses = {"answers": answer_payload}
        result.grading = {"breakdown": breakdown}
        result.score = score
        result.status = final_status
        result.submitted_at = now

        await self.session.commit()
        await self.session.refresh(result)

        return SubmitAssessmentResponse(
            result_id=result.id,
            mentor_assessment_id=assessment.id,
            score=score,
            max_score=max_score,
            status=result.status,
            submitted_at=result.submitted_at,
            breakdown=[QuestionGradeBreakdown(**item) for item in breakdown],
        )

    async def mentor_grade_result(
        self,
        *,
        actor: User,
        result_id: int,
        payload: MentorGradeRequest,
    ) -> MentorGradeResponse:
        result = await self._get_result_by_id(result_id)
        assessment = await self._get_mentor_assessment(result.mentor_assessment_id)
        await self._ensure_mentor_access(actor=actor, mentor_assessment=assessment)

        if result.status == StudentAssessmentStatus.NOT_STARTED.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student has not started this assessment",
            )

        max_score = len(assessment.questions)
        breakdown = self._resolve_breakdown_for_grading(
            assessment=assessment,
            result=result,
            payload=payload,
        )
        score = payload.score
        if score is None:
            score = sum(1 for item in breakdown if item.correct is True)

        result.grading = {
            "breakdown": [item.model_dump() for item in breakdown],
            "feedback": payload.feedback,
            "graded_by_mentor": True,
        }
        result.score = score
        result.status = StudentAssessmentStatus.GRADED.value
        if result.submitted_at is None:
            result.submitted_at = datetime.now(UTC)

        self.session.add(
            AuditLog(
                actor_user_id=actor.id,
                action="assessment_result_graded",
                resource_type="assessment_result",
                resource_id=str(result.id),
                after_json={"score": score, "max_score": max_score},
                created_at=datetime.now(UTC),
            )
        )
        await self.session.commit()
        await self.session.refresh(result)

        return MentorGradeResponse(
            result_id=result.id,
            user_id=result.user_id,
            mentor_assessment_id=result.mentor_assessment_id,
            score=score,
            max_score=max_score,
            status=result.status,
            breakdown=breakdown,
            graded_by_mentor=True,
        )

    async def get_result_detail(
        self,
        *,
        actor: User,
        result_id: int,
    ) -> AssessmentResultDetailResponse:
        result = await self._get_result_by_id(result_id)
        assessment = await self._get_mentor_assessment(result.mentor_assessment_id)

        if actor.role == UserRole.STUDENT.value and result.user_id != actor.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your assessment")
        if actor.role == UserRole.MENTOR.value:
            await self._ensure_mentor_access(actor=actor, mentor_assessment=assessment)
        elif actor.role not in {
            UserRole.STAFF.value,
            UserRole.ADMIN.value,
            UserRole.GENERAL_ADMIN.value,
            UserRole.SYSTEM_ADMIN.value,
        }:
            if result.user_id != actor.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        breakdown = [
            QuestionGradeBreakdown(**item)
            for item in (result.grading or {}).get("breakdown", [])
        ]
        return AssessmentResultDetailResponse(
            id=result.id,
            mentor_assessment_id=result.mentor_assessment_id,
            user_id=result.user_id,
            score=result.score,
            max_score=len(assessment.questions),
            status=result.status,
            started_at=result.started_at,
            expires_at=result.expires_at,
            submitted_at=result.submitted_at,
            responses=result.responses or {},
            breakdown=breakdown,
        )

    @staticmethod
    def _compute_expires_at(*, started_at: datetime, duration_minutes: int) -> datetime:
        return started_at + timedelta(minutes=duration_minutes, seconds=SUBMISSION_GRACE_SECONDS)

    @staticmethod
    def _ensure_student_role(user: User) -> None:
        if user.role != UserRole.STUDENT.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student access required",
            )

    async def _get_student_course_ids(self, student: User) -> list[int]:
        statement = text(
            """
            SELECT DISTINCT p.course_id
            FROM cohort_participant AS p
            WHERE LOWER(TRIM(p.email)) = :email
              AND p.course_id IS NOT NULL
            """
        )
        result = await self.session.execute(
            statement,
            {"email": student.email.lower().strip()},
        )
        return [int(row[0]) for row in result.all()]

    @classmethod
    def _student_assessment_list_item(
        cls,
        *,
        assessment: MentorAssessment,
        result: AssessmentResult | None,
        now: datetime,
    ) -> StudentAssessmentListItemResponse:
        if assessment.released_at is None:
            raise ValueError("released_at is required for published assessments")
        status_value = (
            result.status
            if result is not None
            else StudentAssessmentStatus.NOT_STARTED.value
        )
        return StudentAssessmentListItemResponse(
            mentor_assessment_id=assessment.id,
            course_id=assessment.course_id,
            title=assessment.title,
            assessment_type=assessment.assessment_type,
            duration_minutes=assessment.duration_minutes,
            due_at=assessment.due_at,
            total_questions=assessment.total_questions,
            released_at=assessment.released_at,
            result_id=result.id if result is not None else None,
            status=status_value,
            score=cls._student_visible_score(assessment=assessment, result=result),
            max_score=assessment.total_questions,
            started_at=result.started_at if result is not None else None,
            expires_at=result.expires_at if result is not None else None,
            submitted_at=result.submitted_at if result is not None else None,
            can_start=cls._can_start_assessment(
                assessment=assessment,
                result=result,
                now=now,
            ),
            is_overdue=cls._is_assessment_overdue(
                assessment=assessment,
                status_value=status_value,
                now=now,
            ),
        )

    @staticmethod
    def _student_visible_score(
        *,
        assessment: MentorAssessment,
        result: AssessmentResult | None,
    ) -> int | None:
        if result is None or result.score is None:
            return None
        if result.status not in {
            StudentAssessmentStatus.SUBMITTED.value,
            StudentAssessmentStatus.GRADED.value,
        }:
            return None
        if assessment.result_release_mode == ResultReleaseMode.MENTOR_CONTROLLED.value:
            if result.status != StudentAssessmentStatus.GRADED.value:
                return None
        return result.score

    @staticmethod
    def _is_assessment_overdue(
        *,
        assessment: MentorAssessment,
        status_value: str,
        now: datetime,
    ) -> bool:
        if assessment.due_at is None:
            return False
        if status_value in {
            StudentAssessmentStatus.SUBMITTED.value,
            StudentAssessmentStatus.GRADED.value,
        }:
            return False
        return now > assessment.due_at

    @staticmethod
    def _can_start_assessment(
        *,
        assessment: MentorAssessment,
        result: AssessmentResult | None,
        now: datetime,
    ) -> bool:
        status_value = (
            result.status
            if result is not None
            else StudentAssessmentStatus.NOT_STARTED.value
        )
        if status_value in {
            StudentAssessmentStatus.SUBMITTED.value,
            StudentAssessmentStatus.GRADED.value,
        }:
            return False
        if assessment.due_at and now > assessment.due_at:
            return False
        if (
            status_value == StudentAssessmentStatus.IN_PROGRESS.value
            and result is not None
            and result.expires_at
            and now > result.expires_at
        ):
            return False
        return True

    async def _ensure_mentor_access(self, *, actor: User, mentor_assessment: MentorAssessment) -> None:
        if actor.role in {
            UserRole.STAFF.value,
            UserRole.ADMIN.value,
            UserRole.GENERAL_ADMIN.value,
            UserRole.SYSTEM_ADMIN.value,
        }:
            return
        if actor.role != UserRole.MENTOR.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Mentor access required")

        mentor = await self._get_mentor_for_user(actor.id)
        if mentor is None or mentor.id != mentor_assessment.mentor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only manage your own assessments",
            )

    def _resolve_breakdown_for_grading(
        self,
        *,
        assessment: MentorAssessment,
        result: AssessmentResult,
        payload: MentorGradeRequest,
    ) -> list[QuestionGradeBreakdown]:
        if payload.breakdown is not None:
            return [
                item.model_copy(update={"mentor_override": True, "auto_graded": item.auto_graded})
                for item in payload.breakdown
            ]

        existing = [
            QuestionGradeBreakdown(**item)
            for item in (result.grading or {}).get("breakdown", [])
        ]
        if existing:
            return [item.model_copy(update={"mentor_override": True}) for item in existing]

        answers = (result.responses or {}).get("answers", [])
        _, auto_breakdown = auto_grade_submission(assessment.questions, answers)
        return [
            QuestionGradeBreakdown(**{**item, "mentor_override": True})
            for item in auto_breakdown
        ]

    async def _get_mentor_assessment(self, mentor_assessment_id: int) -> MentorAssessment:
        result = await self.session.execute(
            select(MentorAssessment).where(MentorAssessment.id == mentor_assessment_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor assessment not found")
        return row

    async def _get_released_assessment(self, mentor_assessment_id: int) -> MentorAssessment:
        row = await self._get_mentor_assessment(mentor_assessment_id)
        if row.released_at is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment is not published yet",
            )
        return row

    async def _get_mentor_for_user(self, user_id: int) -> Mentor | None:
        result = await self.session.execute(select(Mentor).where(Mentor.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_or_create_result(
        self, *, mentor_assessment_id: int, user_id: int
    ) -> AssessmentResult:
        result = await self._get_result(
            mentor_assessment_id=mentor_assessment_id,
            user_id=user_id,
        )
        if result is not None:
            return result
        row = AssessmentResult(mentor_assessment_id=mentor_assessment_id, user_id=user_id)
        self.session.add(row)
        await self.session.flush()
        return row

    async def _get_result(
        self, *, mentor_assessment_id: int, user_id: int
    ) -> AssessmentResult | None:
        result = await self.session.execute(
            select(AssessmentResult).where(
                AssessmentResult.mentor_assessment_id == mentor_assessment_id,
                AssessmentResult.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def _get_result_by_id(self, result_id: int) -> AssessmentResult:
        result = await self.session.execute(
            select(AssessmentResult).where(AssessmentResult.id == result_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment result not found")
        return row
