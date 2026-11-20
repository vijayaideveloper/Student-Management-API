from fastapi import FastAPI
from app.database import Base, engine
from routers.student_router import student_router
from routers.course_router import course_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Student Mangement System')


@app.get('/', tags=['Root'])

def get_root():

    return {
        "Its Worked Fine !"
    }

app.include_router(student_router)

app.include_router(course_router)