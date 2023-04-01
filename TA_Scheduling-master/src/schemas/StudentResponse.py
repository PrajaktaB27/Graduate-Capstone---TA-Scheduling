from enum import Enum
from typing import List, Union
from pydantic import BaseModel, Field

class CourseTaken(Enum):
    Yes = "1"
    Yes_Not_SU = "2"
    No = "3"
    Left_Blank = ''
    def __str__(self) -> str:
        if self == CourseTaken.Yes_Not_SU:
            return 'Yes, not SU'
        if self == CourseTaken.Left_Blank:
            return ''
        return self.name

class PreferenceLevel(Enum):
    Preferred = "1"
    OK = "2"
    No = "3"
    Left_Blank = ''
    def __str__(self) -> str:
        if self == PreferenceLevel.Left_Blank:
            return ''
        return self.name
    
class Grade(Enum):
    A = "1"
    AMinus = "2"
    BPlus = "3"
    B = "4"
    BMinus = "5"
    CPlus = "6"
    C = "7"
    Left_Blank = ""

    def __str__(self):
        if self == Grade.AMinus:
            return "A-"
        if self == Grade.BPlus:
            return "B+"
        if self == Grade.BMinus:
            return "B-"
        if self == Grade.CPlus:
            return "C+"
        if self == Grade.Left_Blank:
            return ''
        return self.name
        

class ClassStanding(Enum):
    Freshman =  "1"
    Sophomore = "2"
    Junior =    "3"
    Senior =    "4"
    Certificate = "5"
    MSCS = "6"

    def __str__(self) -> str:
        return self.name

class IsEmployee(Enum):
    Yes = "1"
    No = "2"
    def __str__(self) -> str:
        return self.name

class StudentResponse(BaseModel):
    firstName: str = Field(..., alias="Q1_1")
    lastName: str = Field(..., alias="Q1_2")
    email: str = Field(..., alias="Q2")
    class_standing: ClassStanding = Field(..., alias="Q3")
    cGPA: float = Field(..., alias="Q4") 
    reference: str = Field(..., alias="Q5")
    employee: IsEmployee = Field(..., alias="Q6")
    arrange_instructor: List[str] = Field(default=[], alias='Q7') #FIXME: ENFORCE EMAIL ADDRESS IN SURVEY
    #course_preference: List[str] = Field(default=[], alias='Q9') #will be processed through StudentCourse
    comments: Union[str, None] = Field(None, alias='Q9')

class StudentCourse(BaseModel):
    email: str
    courseID: str
    courseTaken: CourseTaken
    course_GPA: Union[Grade, None] = Grade.Left_Blank
    preferenceLevel: PreferenceLevel
