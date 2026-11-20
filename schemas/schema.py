from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List


class CourseBase(BaseModel):
    
    stud_id : int
    course: str

class CourseResponse(CourseBase):

    course_id : int
    


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

    stud_id : int
    course : str

