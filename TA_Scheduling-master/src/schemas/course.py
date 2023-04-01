from datetime import datetime, timezone
from typing import Union
from pydantic import BaseModel, Field

class Course(BaseModel):
    courseID: str = Field(..., alias="Section")
    enrollment: int = Field(..., alias="StudentCount")
    courseName: str = Field(..., alias="CourseTitle")
    #courseSection: str
    faculty: str = Field(..., alias="Faculty")
    term: str = Field(..., alias='Term')
    hours_allowed: int

class AssignmentExport(BaseModel):
    courseID: str
    student_email: str
    instructor_email: str
    support_type: str

class AssignmentTableInfo(BaseModel):
    courseID: str
    courseName: str
    fac_email: str
    facultyName: str
    stu_email: str
    studentName: str
    is_faculty_preferred: bool

class CourseManual(BaseModel):
    courseID: str = Field(..., alias="course_ID")
    enrollment: int
    faculty: str = Field(..., alias="instructor")
    term: str
    hours_allowed: int = Field(..., alias='hours')

class MatchedCourse(BaseModel):
    courseID: str
    email: Union[str, None] = ''
    approved: Union[bool, None] = False
    last_update: Union[datetime, None] = datetime.now(timezone.utc)