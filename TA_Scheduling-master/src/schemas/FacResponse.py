from enum import Enum
from typing import List, Union
from pydantic import BaseModel, Field

class SharedEnum(Enum):
    Yes = "1"
    No = "2"
    def __str__(self) -> str:
        return self.name

class Completed(Enum):
    Yes = "1"
    Preferred = "2"
    No = "3"
    def __str__(self) -> str:
        return self.name

class SupportType(Enum):
    Grader = "1"
    TA = "2"
    Tutor = "3"
    def __str__(self) -> str:
        return self.name

class FacResponse(BaseModel):
    faculty_first_name: str = Field(..., alias="Q1_1") 
    faculty_last_name: str = Field(..., alias="Q1_2")  
    email: str = Field(..., alias="Q2")
    courseID: str = Field(..., alias="Q3")
    support_type: SupportType = Field(..., alias="Q4") 
    completed: Completed = Field(..., alias="Q5") 
    share_student_approved: SharedEnum = Field(..., alias="Q6")
    number_needed: int = Field(0, alias="Q7")
    preferred_Student: List[str] = Field(default=[], alias='Q8') #Q8#1
    not_preferred_Student: List[str] = Field(default=[], alias='Q9') #Q9#1
    additional_req: Union[str, None] = Field(None, alias='Q10')
    hoursAllowed: int
