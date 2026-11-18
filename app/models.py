from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Students(Base):
    __tablename__ = "students"

    stu_id = Column(Integer, primary_key=True, index=True)
    register_no = Column(String(10), unique=True, nullable=False)
    name = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    dept = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    email = Column(String(100), unique=True)
    phone_no = Column(String(15), nullable=False)
    city = Column(String(30))
    state = Column(String(30))

    # Relationship: One student -> Many courses
    courses = relationship(
        "Courses",
        back_populates="student",
        cascade="all, delete-orphan"
    )


class Courses(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)

    # Foreign key
    stu_id = Column(Integer, ForeignKey("students.stu_id"), nullable=False)

    course = Column(String(50), nullable=False)

    # Relationship: Many courses -> One student
    student = relationship("Students", back_populates="courses")