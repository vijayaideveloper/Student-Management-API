from fastapi import APIRouter



student_router = APIRouter(prefix='students', tags=['Manage Students API'])


@student_router.get('/')

def get_students():
    pass