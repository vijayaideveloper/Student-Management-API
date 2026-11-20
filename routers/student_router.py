from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.schema import StudentBase, StudentResponse
from app.models import Students, Courses



student_router = APIRouter(prefix='/students', tags=['Manage Students'])


@student_router.get('/')

def get_students(db : Session = Depends(get_db)):
    students = db.query(Students).all()

    return students

@student_router.get('/{id}')

def get_student(stu_id : int,
                db : Session = Depends(get_db)):
    
    student = db.query(Students).filter(Students.stu_id == stu_id).first()

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Student found in this {stu_id}")

    return student



@student_router.post('/create',
                     status_code=status.HTTP_201_CREATED)

def create_student(student : StudentBase,
                   db : Session = Depends(get_db)):
    
    new_student = Students(**student.model_dump())

    db.add(new_student)
    db.commit()

    db.refresh(new_student)

    return {
        "Successfully added" : new_student
    }

@student_router.put('/update/{id}',
                    status_code=status.HTTP_202_ACCEPTED)

def update_student(id : int,
                   student : StudentBase,
                   db : Session = Depends(get_db)):

    existed_student = db.query(Students).filter(Students.stu_id == id).first()

    if existed_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Student (id : {id}) is Not Found in database")

    existed_student.name = student.name
    existed_student.age = student.age
    existed_student.register_no = student.register_no
    existed_student.year = student.year
    existed_student.dept = student.dept
    existed_student.city = student.city
    existed_student.state = student.state
    existed_student.email = student.email
    existed_student.phone_no = student.phone_no

    db.commit()

    db.refresh(existed_student)

    return {
        "Updated Student" : existed_student
    }
    

@student_router.delete('/delete/{id}')

def delete_student(id : int,
                   db : Session = Depends(get_db)):

    existed_student = db.query(Students).filter(Students.stu_id == id).first()
    if existed_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Student (id : {id}) is Not Found in database")

    db.delete(existed_student)
    db.commit()

    return {
        "Deleted Successfull" : existed_student
    }