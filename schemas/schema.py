from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List



class CourseBase(BaseModel):
    
    stu_id : int
    course: str

class CourseResponse(BaseModel):

    course_id : int
    stu_id : int
    course : str
    


class StudentBase(BaseModel):
    register_no: str
    name: str
    age: int
    dept: str
    year: int
    email: Optional[EmailStr] = None
    phone_no: str
    city: Optional[str] = None
    state: Optional[str] = None

class StudentResponse(StudentBase):

    model_config = ConfigDict(from_attributes=True)

    stu_id : int
    courses : List[CourseResponse] = []

class CourseCreate(BaseModel):

    stu_id : int
    course : str

class CourseUpdate(BaseModel):

    course : str