from fastapi import APIRouter



student_router = APIRouter(prefix='students', tags=['Manage Students API'])


@student_router.get('/')

def get_students():
    pass

@student_router.get('/{id}')

def get_student(id : int):
    pass

@student_router.post('/create')

def create_student():
    pass

@student_router.put('/update')

def update_student():
    pass

@student_router.delete('/delete')

def delete_student():
    pass