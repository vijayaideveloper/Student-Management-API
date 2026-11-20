from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Students, Courses
from schemas.schema import (CourseBase,
                            CourseResponse,
                            CourseCreate,
                            CourseUpdate)




course_router = APIRouter(prefix="/courses", 
                          tags=['Courses API'])


@course_router.get('/',
                   response_model=list[CourseResponse])

def get_courses(db : Session = Depends(get_db)):

    all_courses = db.query(Courses).all()

    return all_courses



@course_router.get('/{course_id}',
                   response_model=CourseResponse)

def get_course(course_id : int,
               db : Session = Depends(get_db)):

    course = db.query(Courses).filter(
        Courses.course_id == course_id
    ).first()

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course ID {id} not found"
        )

    return course


@course_router.post('/assign',
                    response_model=CourseResponse)
def assign_course(
                  course : CourseCreate,
                  db : Session = Depends(get_db)):

    student = db.query(Students).filter(Students.stu_id==course.stu_id).first()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student ID {course.stu_id} not found"
        )



    new_course = Courses(stu_id = course.stu_id,
                         course = course.course)

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course



@course_router.put(
    "/assign/{id}",
    response_model=CourseResponse
)
def update_course(
    id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db)
):

    existed_course = db.query(Courses).filter(
        Courses.course_id == id
    ).first()

    if existed_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course ID {id} not found"
        )

    existed_course.course = course.course

    db.commit()
    db.refresh(existed_course)

    return existed_course



@course_router.delete(
    "/assign/{id}"
)
def remove_course(
    id: int,
    db: Session = Depends(get_db)
):

    existed_course = db.query(Courses).filter(
        Courses.course_id == id
    ).first()

    if existed_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course ID {id} not found"
        )

    db.delete(existed_course)
    db.commit()

    return {
        "message": "Course removed successfully",
        "course_id": id
    }