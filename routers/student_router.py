from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Students, Courses



student_router = APIRouter(prefix='/students', tags=['Manage Students API'])


@student_router.get('/')

def get_students(db : Session = Depends(get_db)):
    students = db.query(Students).all()

    return {'students ok'}

@student_router.get('/{id}')

def get_student(stu_id : int,
                db : Session = Depends(get_db)):
    
    student = db.query(Students).filter(Students.stu_id == stu_id).first()

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Student found in this {stu_id}")

    return student



@student_router.post('/create')

def create_student():
    pass

@student_router.put('/update')

def update_student():
    pass

@student_router.delete('/delete')

def delete_student():
    pass