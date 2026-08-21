from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class CreateAttendanceCodeRequest(BaseModel):
    programme: str = Field(min_length=1, max_length=255)
    track: str = Field(min_length=1, max_length=255)
    duration: int = Field(gt=0, description="Duration in minutes")
    custom_code: str | None = Field(default=None, min_length=1, max_length=50)


class AttendanceCodeResponse(BaseModel):
    id: int
    code: str
    programme: str
    track: str
    duration: int
    expiresAt: datetime = Field(validation_alias=AliasChoices("expires_at", "expiresAt"))
    isActive: bool = Field(validation_alias=AliasChoices("is_active", "isActive"))
    mentorId: int = Field(validation_alias=AliasChoices("mentor_id", "mentorId"))
    status: str
    createdAt: datetime = Field(validation_alias=AliasChoices("created_at", "createdAt"))
    updatedAt: datetime = Field(validation_alias=AliasChoices("updated_at", "updatedAt"))
    signedCount: int = Field(default=0, validation_alias=AliasChoices("signed_count", "signedCount"))

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class StudentAttendanceSubmitRequest(BaseModel):
    full_name: str = Field(
        min_length=1,
        max_length=255,
        validation_alias=AliasChoices("full_name", "studentName", "fullName"),
    )
    code: str = Field(min_length=1, max_length=50)

    model_config = ConfigDict(populate_by_name=True)



class AttendanceRecordResponse(BaseModel):
    id: int
    attendanceCodeId: int = Field(
        validation_alias=AliasChoices("attendance_code_id", "attendanceCodeId")
    )
    studentName: str = Field(validation_alias=AliasChoices("student_name", "studentName"))
    date: str
    time: str
    timeIn: str | None = Field(default=None, validation_alias=AliasChoices("time_in", "timeIn"))
    timeOut: str | None = Field(default=None, validation_alias=AliasChoices("time_out", "timeOut"))
    createdAt: datetime = Field(validation_alias=AliasChoices("created_at", "createdAt"))
    updatedAt: datetime = Field(validation_alias=AliasChoices("updated_at", "updatedAt"))

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class StudentAttendanceSubmitResponse(BaseModel):
    message: str
    attendance: AttendanceRecordResponse


class AttendanceCodeDetailResponse(BaseModel):
    id: int
    code: str
    programme: str
    track: str
    duration: int
    expiresAt: datetime = Field(validation_alias=AliasChoices("expires_at", "expiresAt"))
    isActive: bool = Field(validation_alias=AliasChoices("is_active", "isActive"))
    mentorId: int = Field(validation_alias=AliasChoices("mentor_id", "mentorId"))
    status: str
    createdAt: datetime = Field(validation_alias=AliasChoices("created_at", "createdAt"))
    updatedAt: datetime = Field(validation_alias=AliasChoices("updated_at", "updatedAt"))
    signedCount: int = Field(default=0, validation_alias=AliasChoices("signed_count", "signedCount"))
    attendees: list[AttendanceRecordResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class AdminAttendanceCodeItem(BaseModel):
    code: str
    programme: str
    createdAt: datetime = Field(validation_alias=AliasChoices("created_at", "createdAt"))

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class AdminAttendanceCodesResponse(BaseModel):
    success: bool = True
    data: list[AdminAttendanceCodeItem]
    total: int
    page: int
    page_size: int


class AdminAttendanceMentor(BaseModel):
    id: int
    name: str
    email: str


class AdminAttendanceDetailRecord(BaseModel):
    id: int
    studentName: str = Field(validation_alias=AliasChoices("student_name", "studentName"))
    date: str
    time: str
    timeIn: str | None = Field(default=None, validation_alias=AliasChoices("time_in", "timeIn"))
    timeOut: str | None = Field(default=None, validation_alias=AliasChoices("time_out", "timeOut"))
    createdAt: datetime = Field(validation_alias=AliasChoices("created_at", "createdAt"))

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class AdminAttendanceDetailData(BaseModel):
    code: str
    programme: str
    track: str
    duration: int
    expiresAt: datetime = Field(validation_alias=AliasChoices("expires_at", "expiresAt"))
    isActive: bool = Field(validation_alias=AliasChoices("is_active", "isActive"))
    status: str
    createdAt: datetime = Field(validation_alias=AliasChoices("created_at", "createdAt"))
    mentor: AdminAttendanceMentor
    attendance: list[AdminAttendanceDetailRecord]
    totalAttendance: int
    page: int
    page_size: int


class AdminAttendanceDetailResponse(BaseModel):
    success: bool = True
    data: AdminAttendanceDetailData

