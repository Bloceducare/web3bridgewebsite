from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api import deps
from app.db.session import get_db_session
from app.main import app
from app.models.portal import AccountState, User, UserRole
from app.schemas.attendance import (
    AttendanceCodeDetailResponse,
    AttendanceCodeResponse,
    AttendanceRecordResponse,
    CreateAttendanceCodeRequest,
    StudentAttendanceSubmitRequest,
    StudentAttendanceSubmitResponse,
)
from app.schemas.auth import MessageResponse
from app.services.attendance import AttendanceService

client = TestClient(app)


class DummyDBSession:
    pass


async def override_db_session() -> AsyncGenerator[DummyDBSession, None]:
    yield DummyDBSession()


def build_mentor_user(user_id: int = 1) -> User:
    return User(
        id=user_id,
        email=f"mentor{user_id}@example.com",
        role=UserRole.MENTOR.value,
        account_state=AccountState.ACTIVE.value,
        email_verified=True,
    )


def clear_overrides() -> None:
    app.dependency_overrides.clear()


def test_mentor_create_attendance_code_success() -> None:
    mentor_user = build_mentor_user()

    async def override_mentor_user() -> User:
        return mentor_user

    async def mock_create_attendance_code(
        self: AttendanceService, actor: User, payload: CreateAttendanceCodeRequest
    ) -> AttendanceCodeResponse:
        now = datetime.now(UTC)
        return AttendanceCodeResponse(
            id=101,
            code=payload.custom_code.upper() if payload.custom_code else "XYNMH",
            programme=payload.programme, 
            track=payload.track,
            duration=payload.duration,
            expiresAt=now + timedelta(minutes=payload.duration),
            isActive=True,
            mentorId=1,
            status="Active",
            createdAt=now,
            updatedAt=now,
            signedCount=0,
        )

    orig_method = AttendanceService.create_attendance_code
    AttendanceService.create_attendance_code = mock_create_attendance_code
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/mentor/attendance/codes",
            json={
                "programme": "Web3 Engineering",
                "track": "Solidity",
                "duration": 60,
                "custom_code": "XYNMH",
            },
        )
    finally:
        AttendanceService.create_attendance_code = orig_method
        clear_overrides()

    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "XYNMH"
    assert data["programme"] == "Web3 Engineering"
    assert data["track"] == "Solidity"
    assert data["duration"] == 60
    assert data["isActive"] is True
    assert data["status"] == "Active"


def test_mentor_create_duplicate_custom_code_fails() -> None:
    mentor_user = build_mentor_user()

    async def override_mentor_user() -> User:
        return mentor_user

    async def mock_create_attendance_code(
        self: AttendanceService, actor: User, payload: CreateAttendanceCodeRequest
    ) -> AttendanceCodeResponse:
        raise HTTPException(
            status_code=400,
            detail="Attendance code already exists. Please choose a different code.",
        )

    orig_method = AttendanceService.create_attendance_code
    AttendanceService.create_attendance_code = mock_create_attendance_code
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/mentor/attendance/codes",
            json={
                "programme": "Web3 Engineering",
                "track": "Solidity",
                "duration": 60,
                "custom_code": "XYNMH",
            },
        )
    finally:
        AttendanceService.create_attendance_code = orig_method
        clear_overrides()

    assert response.status_code == 400
    assert response.json()["detail"] == "Attendance code already exists. Please choose a different code."


def test_mentor_list_attendance_codes() -> None:
    mentor_user = build_mentor_user()

    async def override_mentor_user() -> User:
        return mentor_user

    async def mock_list_mentor_attendance_codes(
        self: AttendanceService, actor: User
    ) -> list[AttendanceCodeResponse]:
        now = datetime.now(UTC)
        return [
            AttendanceCodeResponse(
                id=1,
                code="XYNMH",
                programme="Web3",
                track="Solidity",
                duration=60,
                expiresAt=now + timedelta(minutes=60),
                isActive=True,
                mentorId=1,
                status="Active",
                createdAt=now,
                updatedAt=now,
                signedCount=5,
            )
        ]

    orig_method = AttendanceService.list_mentor_attendance_codes
    AttendanceService.list_mentor_attendance_codes = mock_list_mentor_attendance_codes
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/mentor/attendance/codes")
    finally:
        AttendanceService.list_mentor_attendance_codes = orig_method
        clear_overrides()

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "XYNMH"
    assert data[0]["signedCount"] == 5


def test_mentor_get_attendance_code_details() -> None:
    mentor_user = build_mentor_user()

    async def override_mentor_user() -> User:
        return mentor_user

    async def mock_get_attendance_code_details(
        self: AttendanceService, actor: User, code_id: int
    ) -> AttendanceCodeDetailResponse:
        now = datetime.now(UTC)
        return AttendanceCodeDetailResponse(
            id=code_id,
            code="XYNMH",
            programme="Web3",
            track="Solidity",
            duration=60,
            expiresAt=now + timedelta(minutes=60),
            isActive=True,
            mentorId=1,
            status="Active",
            createdAt=now,
            updatedAt=now,
            signedCount=2,
            attendees=[
                AttendanceRecordResponse(
                    id=1,
                    attendanceCodeId=code_id,
                    studentName="Alice Johnson",
                    date=now.strftime("%Y-%m-%d"),
                    time=now.strftime("%H:%M:%S"),
                    createdAt=now,
                    updatedAt=now,
                ),
                AttendanceRecordResponse(
                    id=2,
                    attendanceCodeId=code_id,
                    studentName="Bob Smith",
                    date=now.strftime("%Y-%m-%d"),
                    time=now.strftime("%H:%M:%S"),
                    createdAt=now,
                    updatedAt=now,
                ),
            ],
        )

    orig_method = AttendanceService.get_attendance_code_details
    AttendanceService.get_attendance_code_details = mock_get_attendance_code_details
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.get("/api/v1/mentor/attendance/codes/1")
    finally:
        AttendanceService.get_attendance_code_details = orig_method
        clear_overrides()

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "XYNMH"
    assert len(data["attendees"]) == 2
    assert data["attendees"][0]["studentName"] == "Alice Johnson"


def test_mentor_deactivate_attendance_code() -> None:
    mentor_user = build_mentor_user()

    async def override_mentor_user() -> User:
        return mentor_user

    async def mock_deactivate_attendance_code(
        self: AttendanceService, actor: User, code_id: int
    ) -> AttendanceCodeResponse:
        now = datetime.now(UTC)
        return AttendanceCodeResponse(
            id=code_id,
            code="XYNMH",
            programme="Web3",
            track="Solidity",
            duration=60,
            expiresAt=now + timedelta(minutes=60),
            isActive=False,
            mentorId=1,
            status="Inactive",
            createdAt=now,
            updatedAt=now,
            signedCount=2,
        )

    orig_method = AttendanceService.deactivate_attendance_code
    AttendanceService.deactivate_attendance_code = mock_deactivate_attendance_code
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.patch("/api/v1/mentor/attendance/codes/1/deactivate")
    finally:
        AttendanceService.deactivate_attendance_code = orig_method
        clear_overrides()

    assert response.status_code == 200
    data = response.json()
    assert data["isActive"] is False
    assert data["status"] == "Inactive"


def test_mentor_delete_attendance_code() -> None:
    mentor_user = build_mentor_user()

    async def override_mentor_user() -> User:
        return mentor_user

    async def mock_delete_attendance_code(
        self: AttendanceService, actor: User, code_id: int
    ) -> MessageResponse:
        return MessageResponse(detail="Attendance code deleted successfully")

    orig_method = AttendanceService.delete_attendance_code
    AttendanceService.delete_attendance_code = mock_delete_attendance_code
    app.dependency_overrides[deps.get_current_mentor_user] = override_mentor_user
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.delete("/api/v1/mentor/attendance/codes/1")
    finally:
        AttendanceService.delete_attendance_code = orig_method
        clear_overrides()

    assert response.status_code == 200
    assert response.json()["detail"] == "Attendance code deleted successfully"



def test_student_submit_attendance_success() -> None:
    async def mock_submit_student_attendance(
        self: AttendanceService, payload: StudentAttendanceSubmitRequest
    ) -> StudentAttendanceSubmitResponse:
        now = datetime.now(UTC)
        return StudentAttendanceSubmitResponse(
            message="Attendance recorded successfully",
            attendance=AttendanceRecordResponse(
                id=10,
                attendanceCodeId=1,
                studentName=payload.full_name,
                date=now.strftime("%Y-%m-%d"),
                time=now.strftime("%H:%M:%S"),
                createdAt=now,
                updatedAt=now,
            ),
        )

    orig_method = AttendanceService.submit_student_attendance
    AttendanceService.submit_student_attendance = mock_submit_student_attendance
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/attendance/submit",
            json={"studentName": "John Doe", "code": "XYNMH"},
        )
    finally:
        AttendanceService.submit_student_attendance = orig_method
        clear_overrides()

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Attendance recorded successfully"
    assert data["attendance"]["studentName"] == "John Doe"


def test_student_submit_duplicate_attendance_fails() -> None:
    async def mock_submit_student_attendance(
        self: AttendanceService, payload: StudentAttendanceSubmitRequest
    ) -> StudentAttendanceSubmitResponse:
        raise HTTPException(
            status_code=400,
            detail="You have already signed attendance for this class.",
        )

    orig_method = AttendanceService.submit_student_attendance
    AttendanceService.submit_student_attendance = mock_submit_student_attendance
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/attendance/submit",
            json={"studentName": "John Doe", "code": "XYNMH"},
        )
    finally:
        AttendanceService.submit_student_attendance = orig_method
        clear_overrides()

    assert response.status_code == 400
    assert response.json()["detail"] == "You have already signed attendance for this class."


def test_student_submit_expired_attendance_fails() -> None:
    async def mock_submit_student_attendance(
        self: AttendanceService, payload: StudentAttendanceSubmitRequest
    ) -> StudentAttendanceSubmitResponse:
        raise HTTPException(
            status_code=400,
            detail="Attendance session has expired",
        )

    orig_method = AttendanceService.submit_student_attendance
    AttendanceService.submit_student_attendance = mock_submit_student_attendance
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/attendance/submit",
            json={"studentName": "John Doe", "code": "XYNMH"},
        )
    finally:
        AttendanceService.submit_student_attendance = orig_method
        clear_overrides()

    assert response.status_code == 400
    assert response.json()["detail"] == "Attendance session has expired"


def test_student_submit_deactivated_attendance_fails() -> None:
    async def mock_submit_student_attendance(
        self: AttendanceService, payload: StudentAttendanceSubmitRequest
    ) -> StudentAttendanceSubmitResponse:
        raise HTTPException(
            status_code=400,
            detail="Attendance session has been deactivated by the mentor",
        )

    orig_method = AttendanceService.submit_student_attendance
    AttendanceService.submit_student_attendance = mock_submit_student_attendance
    app.dependency_overrides[get_db_session] = override_db_session

    try:
        response = client.post(
            "/api/v1/attendance/submit",
            json={"studentName": "John Doe", "code": "XYNMH"},
        )
    finally:
        AttendanceService.submit_student_attendance = orig_method
        clear_overrides()

    assert response.status_code == 400
    assert response.json()["detail"] == "Attendance session has been deactivated by the mentor"
