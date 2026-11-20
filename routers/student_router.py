from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from schemas.schema import StudentBase, StudentResponse
from app.models import Students



student_router = APIRouter(prefix='/students', 
                           tags=['Manage Students'])


@student_router.get('/',
                    response_model=list[StudentResponse])

def get_students(db : Session = Depends(get_db)):
    students = db.query(Students).all()

    return students

@student_router.get('/{id}',
                    response_model=StudentResponse)

def get_student(stu_id : int,
                db : Session = Depends(get_db)):
    
    student = db.query(Students).filter(Students.stu_id == stu_id).first()

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Student found in this {stu_id}")

    return student



@student_router.post('/create',
                     response_model=StudentResponse,
                     status_code=status.HTTP_201_CREATED)

def create_student(student : StudentBase,
                   db : Session = Depends(get_db)):
    
    existing = db.query(Students).filter(
        Students.register_no==student.register_no).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Register number already exists"
        )
    
    new_student = Students(**student.model_dump())

    db.add(new_student)
    db.commit()

    db.refresh(new_student)

    return {
        "message" : "student created",
        "student id": new_student.stu_id
    }



@student_router.put('/update/{stu_id}',
                    response_model=StudentResponse,
                    status_code=status.HTTP_202_ACCEPTED)

def update_student(stu_id : int,
                   student : StudentBase,
                   db : Session = Depends(get_db)):

    existed_student = db.query(Students).filter(Students.stu_id == stu_id).first()

    if existed_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Student (id : {stu_id}) is Not Found in database")

    for key, value in student.model_dump().items():
        setattr(existed_student, key, value)


    db.commit()

    db.refresh(existed_student)

    return {
        "message" : "updated success",
        "student id" : existed_student.stu_id
    }
    

@student_router.delete('/delete/{stu_id}')

def delete_student(stu_id : int,
                   db : Session = Depends(get_db)):

    existed_student = db.query(Students).filter(Students.stu_id == stu_id).first()
    if existed_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Student (id : {stu_id}) is Not Found in database")

    db.delete(existed_student)
    db.commit()

    return {
        "message" : "deleted success",
        "student id": stu_id
    }