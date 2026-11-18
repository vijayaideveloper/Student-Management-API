from fastapi import FastAPI


app = FastAPI(title='Student Mangement System')


@app.get('/', tags=['Root'])

def get_root():

    return {
        "Its Worked Fine !"
    }