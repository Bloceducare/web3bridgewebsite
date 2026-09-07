import secrets
import string
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.portal import Attendance, AttendanceCode, Mentor, User, UserRole
from app.schemas.attendance import (
    AttendanceCodeDetailResponse,
    AttendanceCodeResponse,
    AttendanceRecordResponse,
    CreateAttendanceCodeRequest,
    StudentAttendanceSubmitRequest,
    StudentAttendanceSubmitResponse,
)
from app.schemas.auth import MessageResponse


class AttendanceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _require_mentor(self, actor: User) -> Mentor:
        if actor.role != UserRole.MENTOR.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Mentor access required",
            )
        result = await self.session.execute(
            select(Mentor).where(Mentor.user_id == actor.id, Mentor.is_active.is_(True))
        )
        mentor = result.scalar_one_or_none()
        if mentor is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Active mentor profile required",
            )
        return mentor

    def _determine_status(self, code: AttendanceCode, now: datetime) -> str:
        if not code.is_active:
            return "Inactive"
        expires_at = code.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if now > expires_at:
            return "Expired"
        return "Active"

    def _generate_code_string(self, length: int = 5) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(chars) for _ in range(length))

    async def create_attendance_code(
        self, actor: User, payload: CreateAttendanceCodeRequest
    ) -> AttendanceCodeResponse:
        mentor = await self._require_mentor(actor)

        if payload.custom_code and payload.custom_code.strip():
            code_str = payload.custom_code.strip().upper()
            existing = await self.session.execute(
                select(AttendanceCode).where(func.upper(AttendanceCode.code) == code_str)
            )
            if existing.scalar_one_or_none() is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Attendance code already exists. Please choose a different code.",
                )
        else:
            # Generate unique code
            for _ in range(10):
                code_str = self._generate_code_string()
                existing = await self.session.execute(
                    select(AttendanceCode).where(func.upper(AttendanceCode.code) == code_str)
                )
                if existing.scalar_one_or_none() is None:
                    break
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate a unique attendance code. Please try again.",
                )

        now = datetime.now(UTC)
        expires_at = now + timedelta(minutes=payload.duration)

        attendance_code = AttendanceCode(
            code=code_str,
            programme=payload.programme.strip(),
            track=payload.track.strip(),
            duration=payload.duration,
            expires_at=expires_at,
            is_active=True,
            mentor_id=mentor.id,
        )
        self.session.add(attendance_code)
        await self.session.commit()
        await self.session.refresh(attendance_code)

        status_str = self._determine_status(attendance_code, now)
        return AttendanceCodeResponse(
            id=attendance_code.id,
            code=attendance_code.code,
            programme=attendance_code.programme,
            track=attendance_code.track,
            duration=attendance_code.duration,
            expiresAt=attendance_code.expires_at,
            isActive=attendance_code.is_active,
            mentorId=attendance_code.mentor_id,
            status=status_str,
            createdAt=attendance_code.created_at,
            updatedAt=attendance_code.updated_at,
            signedCount=0,
        )

    async def list_mentor_attendance_codes(self, actor: User) -> list[AttendanceCodeResponse]:
        mentor = await self._require_mentor(actor)
        now = datetime.now(UTC)

        stmt = (
            select(AttendanceCode)
            .options(selectinload(AttendanceCode.attendances))
            .where(AttendanceCode.mentor_id == mentor.id)
            .order_by(AttendanceCode.created_at.desc())
        )
        result = await self.session.execute(stmt)
        codes = result.scalars().all()

        responses: list[AttendanceCodeResponse] = []
        for code in codes:
            status_str = self._determine_status(code, now)
            responses.append(
                AttendanceCodeResponse(
                    id=code.id,
                    code=code.code,
                    programme=code.programme,
                    track=code.track,
                    duration=code.duration,
                    expiresAt=code.expires_at,
                    isActive=code.is_active,
                    mentorId=code.mentor_id,
                    status=status_str,
                    createdAt=code.created_at,
                    updatedAt=code.updated_at,
                    signedCount=len(code.attendances),
                )
            )
        return responses

    async def get_attendance_code_details(
        self, actor: User, code_id: int
    ) -> AttendanceCodeDetailResponse:
        mentor = await self._require_mentor(actor)
        now = datetime.now(UTC)

        stmt = (
            select(AttendanceCode)
            .options(selectinload(AttendanceCode.attendances))
            .where(AttendanceCode.id == code_id, AttendanceCode.mentor_id == mentor.id)
        )
        result = await self.session.execute(stmt)
        code = result.scalar_one_or_none()
        if code is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance code not found",
            )

        status_str = self._determine_status(code, now)
        sorted_attendances = sorted(code.attendances, key=lambda a: a.created_at)

        attendees = [
            AttendanceRecordResponse(
                id=att.id,
                attendanceCodeId=att.attendance_code_id,
                studentName=att.student_name,
                date=att.date,
                time=att.time,
                timeIn=att.time_in,
                timeOut=att.time_out,
                createdAt=att.created_at,
                updatedAt=att.updated_at,
            )
            for att in sorted_attendances
        ]

        return AttendanceCodeDetailResponse(
            id=code.id,
            code=code.code,
            programme=code.programme,
            track=code.track,
            duration=code.duration,
            expiresAt=code.expires_at,
            isActive=code.is_active,
            mentorId=code.mentor_id,
            status=status_str,
            createdAt=code.created_at,
            updatedAt=code.updated_at,
            signedCount=len(attendees),
            attendees=attendees,
        )

    async def deactivate_attendance_code(
        self, actor: User, code_id: int
    ) -> AttendanceCodeResponse:
        mentor = await self._require_mentor(actor)
        now = datetime.now(UTC)

        stmt = (
            select(AttendanceCode)
            .options(selectinload(AttendanceCode.attendances))
            .where(AttendanceCode.id == code_id, AttendanceCode.mentor_id == mentor.id)
        )
        result = await self.session.execute(stmt)
        code = result.scalar_one_or_none()
        if code is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance code not found",
            )

        code.is_active = False
        await self.session.commit()
        await self.session.refresh(code)

        status_str = self._determine_status(code, now)
        return AttendanceCodeResponse(
            id=code.id,
            code=code.code,
            programme=code.programme,
            track=code.track,
            duration=code.duration,
            expiresAt=code.expires_at,
            isActive=code.is_active,
            mentorId=code.mentor_id,
            status=status_str,
            createdAt=code.created_at,
            updatedAt=code.updated_at,
            signedCount=len(code.attendances),
        )

    async def reactivate_attendance_code(
        self, actor: User, code_id: int
    ) -> AttendanceCodeResponse:
        mentor = await self._require_mentor(actor)
        now = datetime.now(UTC)

        stmt = (
            select(AttendanceCode)
            .options(selectinload(AttendanceCode.attendances))
            .where(AttendanceCode.id == code_id, AttendanceCode.mentor_id == mentor.id)
        )
        result = await self.session.execute(stmt)
        code = result.scalar_one_or_none()
        if code is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance code not found",
            )

        from datetime import timedelta
        code.is_active = True
        code.expires_at = now + timedelta(minutes=code.duration)
        await self.session.commit()
        await self.session.refresh(code)

        status_str = self._determine_status(code, now)
        return AttendanceCodeResponse(
            id=code.id,
            code=code.code,
            programme=code.programme,
            track=code.track,
            duration=code.duration,
            expiresAt=code.expires_at,
            isActive=code.is_active,
            mentorId=code.mentor_id,
            status=status_str,
            createdAt=code.created_at,
            updatedAt=code.updated_at,
            signedCount=len(code.attendances),
        )

    async def delete_attendance_code(self, actor: User, code_id: int) -> MessageResponse:
        mentor = await self._require_mentor(actor)

        stmt = select(AttendanceCode).where(
            AttendanceCode.id == code_id, AttendanceCode.mentor_id == mentor.id
        )
        result = await self.session.execute(stmt)
        code = result.scalar_one_or_none()
        if code is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attendance code not found",
            )

        await self.session.delete(code)
        await self.session.commit()
        return MessageResponse(detail="Attendance code deleted successfully")


    async def submit_student_attendance(
        self, payload: StudentAttendanceSubmitRequest
    ) -> StudentAttendanceSubmitResponse:
        code_str = payload.code.strip().upper()
        student_name = payload.full_name.strip()

        if not code_str or not student_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student name and attendance code are required.",
            )

        stmt = select(AttendanceCode).where(func.upper(AttendanceCode.code) == code_str)
        result = await self.session.execute(stmt)
        attendance_code = result.scalar_one_or_none()

        if attendance_code is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid attendance code",
            )

        if not attendance_code.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance session has been deactivated by the mentor",
            )

        now = datetime.now(UTC)
        expires_at = attendance_code.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)

        if now > expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance session has expired",
            )

        # Check for existing attendance
        stmt = select(Attendance).where(
            Attendance.attendance_code_id == attendance_code.id,
            func.lower(Attendance.student_name) == student_name.lower(),
        )
        res = await self.session.execute(stmt)
        existing_attendance = res.scalar_one_or_none()

        if existing_attendance is not None:
            if existing_attendance.time_out is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already signed out of attendance for this class.",
                )
            
            existing_attendance.time_out = now.strftime("%H:%M:%S")
            await self.session.commit()
            await self.session.refresh(existing_attendance)

            record_resp = AttendanceRecordResponse(
                id=existing_attendance.id,
                attendanceCodeId=existing_attendance.attendance_code_id,
                studentName=existing_attendance.student_name,
                date=existing_attendance.date,
                time=existing_attendance.time,
                timeIn=existing_attendance.time_in,
                timeOut=existing_attendance.time_out,
                createdAt=existing_attendance.created_at,
                updatedAt=existing_attendance.updated_at,
            )

            return StudentAttendanceSubmitResponse(
                message="Attendance signed out successfully",
                attendance=record_resp,
            )

        time_str = now.strftime("%H:%M:%S")
        new_attendance = Attendance(
            attendance_code_id=attendance_code.id,
            student_name=student_name,
            date=now.strftime("%Y-%m-%d"),
            time=time_str,
            time_in=time_str,
            time_out=None,
        )
        self.session.add(new_attendance)
        await self.session.commit()
        await self.session.refresh(new_attendance)

        record_resp = AttendanceRecordResponse(
            id=new_attendance.id,
            attendanceCodeId=new_attendance.attendance_code_id,
            studentName=new_attendance.student_name,
            date=new_attendance.date,
            time=new_attendance.time,
            timeIn=new_attendance.time_in,
            timeOut=new_attendance.time_out,
            createdAt=new_attendance.created_at,
            updatedAt=new_attendance.updated_at,
        )

        return StudentAttendanceSubmitResponse(
            message="Attendance recorded successfully",
            attendance=record_resp,
        )

    async def admin_list_attendance_codes(
        self, programme: str, page: int = 1, page_size: int = 20
    ) -> dict:
        count_stmt = select(func.count(AttendanceCode.id)).where(
            func.lower(func.trim(AttendanceCode.programme)) == programme.lower().strip()
        )
        count_res = await self.session.execute(count_stmt)
        total = count_res.scalar() or 0

        stmt = (
            select(AttendanceCode)
            .where(func.lower(func.trim(AttendanceCode.programme)) == programme.lower().strip())
            .order_by(AttendanceCode.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        res = await self.session.execute(stmt)
        codes = res.scalars().all()

        return {
            "success": True,
            "data": [
                {
                    "code": c.code,
                    "programme": c.programme,
                    "createdAt": c.created_at,
                }
                for c in codes
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def admin_get_attendance_code_details(
        self, code_str: str, page: int = 1, page_size: int = 50
    ) -> dict:
        stmt = (
            select(AttendanceCode)
            .where(func.lower(func.trim(AttendanceCode.code)) == code_str.lower().strip())
        )
        res = await self.session.execute(stmt)
        code = res.scalar_one_or_none()
        if not code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance code {code_str} not found",
            )

        mentor_stmt = (
            select(Mentor, User)
            .join(User, User.id == Mentor.user_id)
            .where(Mentor.id == code.mentor_id)
        )
        mentor_res = await self.session.execute(mentor_stmt)
        mentor_row = mentor_res.first()
        mentor_data = {
            "id": code.mentor_id,
            "name": "Unknown",
            "email": "Unknown",
        }
        if mentor_row:
            mentor, user = mentor_row
            mentor_data = {
                "id": mentor.id,
                "name": mentor.full_name or user.full_name or "Mentor",
                "email": user.email,
            }

        count_stmt = select(func.count(Attendance.id)).where(
            Attendance.attendance_code_id == code.id
        )
        count_res = await self.session.execute(count_stmt)
        total_attendance = count_res.scalar() or 0

        attendance_stmt = (
            select(Attendance)
            .where(Attendance.attendance_code_id == code.id)
            .order_by(Attendance.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        attendance_res = await self.session.execute(attendance_stmt)
        records = attendance_res.scalars().all()

        now = datetime.now(UTC)
        status_str = self._determine_status(code, now)

        return {
            "success": True,
            "data": {
                "code": code.code,
                "programme": code.programme,
                "track": code.track,
                "duration": code.duration,
                "expiresAt": code.expires_at,
                "isActive": code.is_active,
                "status": status_str,
                "createdAt": code.created_at,
                "mentor": mentor_data,
                "attendance": [
                    {
                        "id": r.id,
                        "studentName": r.student_name,
                        "date": r.date,
                        "time": r.time,
                        "timeIn": r.time_in,
                        "timeOut": r.time_out,
                        "createdAt": r.created_at,
                    }
                    for r in records
                ],
                "totalAttendance": total_attendance,
                "page": page,
                "page_size": page_size,
            }
        }

