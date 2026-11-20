# Student Management System API

A RESTful API built with **FastAPI**, **Pydantic v2**, and
**SQLAlchemy** for managing students and the courses assigned to them.

## Features

-   Create, retrieve, update, and delete students.
-   Retrieve all courses and a course by ID.
-   Assign courses to students.
-   Update and remove assigned courses.
-   Validate request and response data with Pydantic.
-   Model a one-to-many relationship between students and courses.
-   Explore and test endpoints through Swagger UI.

## Technology Stack

-   Python 3.12+
-   FastAPI
-   Uvicorn
-   Pydantic v2
-   SQLAlchemy
-   A database supported by your SQLAlchemy configuration

> The database engine and connection settings are defined in
> `app/database.py`. Install the appropriate database driver for the
> database configured there.

## Project Structure

The following is a suggested structure matching the imports used in the
routers. Adjust it if your actual folders differ.

``` text
StudentManagement/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── models.py
├── routers/
│   ├── __init__.py
│   ├── student_router.py
│   └── course_router.py
├── schemas/
│   ├── __init__.py
│   └── schema.py
├── .env                 # Optional; keep secrets out of version control
├── .gitignore
└── README.md
```

If your routers or schemas are inside `app/`, update the import paths
accordingly.

## Data Relationship

The project uses a **one-to-many** relationship:

-   One student can have multiple courses.
-   Each course belongs to one student.
-   `courses.stu_id` is a foreign key referencing `students.stu_id`.

The SQLAlchemy models use `relationship()` and `back_populates` to
connect the two sides of the relationship. The student relationship is
configured with `cascade="all, delete-orphan"`, so deleting a student
through the ORM also deletes that student's associated course records.

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/vijayaideveloper/Student-Management-API.git
cd Student-Management-API
```

### 2. Create and activate a virtual environment

Linux/macOS:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

``` powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic email-validator
```

Install the database driver required by your `app/database.py`
configuration. For example, for PostgreSQL with psycopg 3:

``` bash
pip install "psycopg[binary]"
```

If you use a different database, install its corresponding SQLAlchemy
driver instead.

## Database Configuration

Configure the SQLAlchemy engine and session in `app/database.py`. Keep
credentials in environment variables rather than committing passwords to
Git.

The application imports `Base`, `engine`, and `get_db` from this module.
Ensure your database server is running and the configured database
exists before starting the API.

The application creates tables at startup using:

``` python
Base.metadata.create_all(bind=engine)
```

For production projects, consider using Alembic migrations to manage
schema changes.

## Run the Application

From the project root, run the command that matches your `main.py`
location.

If `main.py` is `app/main.py`:

``` bash
uvicorn app.main:app --reload
```

If `main.py` is at the project root:

``` bash
uvicorn main:app --reload
```

The `--reload` option is intended for development.

## API Documentation

After starting the server, open:

-   Swagger UI: <http://127.0.0.1:8000/docs>
-   ReDoc: <http://127.0.0.1:8000/redoc>
-   OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

## API Endpoints

### Students

  Method   Endpoint                  Description
  -------- ------------------------- ---------------------
  GET      `/students/`              Get all students
  GET      `/students/{id}`          Get a student by ID
  POST     `/students/create`        Create a student
  PUT      `/students/update/{id}`   Update a student
  DELETE   `/students/delete/{id}`   Delete a student

### Courses

  Method   Endpoint                 Description
  -------- ------------------------ ------------------------------
  GET      `/courses/`              Get all courses
  GET      `/courses/{id}`          Get a course by ID
  POST     `/courses/assign`        Assign a course to a student
  PUT      `/courses/assign/{id}`   Update an assigned course
  DELETE   `/courses/assign/{id}`   Remove an assigned course

## Example Requests

Use Swagger UI, curl, or an API client to test the endpoints.

### Create a student

`POST /students/create`

``` json
{
  "register_no": "2026001",
  "name": "Vijay",
  "age": 22,
  "dept": "CSE",
  "year": 3,
  "email": "vijay@example.com",
  "phone_no": "9876543210",
  "city": "Salem",
  "state": "Tamil Nadu"
}
```

### Assign a course

`POST /courses/assign`

``` json
{
  "stu_id": 1,
  "course": "Python Programming"
}
```

Assign another course to the same student by sending another request
with the same `stu_id` and a different course name.

### Get a student and their courses

`GET /students/1`

The student response includes a `courses` array. For example:

``` json
{
  "stu_id": 1,
  "register_no": "2026001",
  "name": "Vijay",
  "age": 22,
  "dept": "CSE",
  "year": 3,
  "email": "vijay@example.com",
  "phone_no": "9876543210",
  "city": "Salem",
  "state": "Tamil Nadu",
  "courses": [
    {
      "course_id": 1,
      "stu_id": 1,
      "course": "Python Programming"
    },
    {
      "course_id": 2,
      "stu_id": 1,
      "course": "Machine Learning"
    }
  ]
}
```

The IDs and response data above are illustrative; actual values depend
on your database.

## Pydantic Schemas

The API uses Pydantic models to validate incoming request data and
serialize ORM objects in responses.

-   `StudentBase`: student input fields.
-   `StudentResponse`: student fields, the student ID, and the related
    courses.
-   `CourseBase` / `CourseCreate`: course assignment input.
-   `CourseUpdate`: fields accepted when updating a course.
-   `CourseResponse`: course output fields.

For Pydantic v2 ORM serialization, response schemas should use:

``` python
model_config = ConfigDict(from_attributes=True)
```

Make sure schema attribute names match the SQLAlchemy model. In this
project, the student primary key and course foreign key are named
`stu_id`.

## Error Handling

The API uses FastAPI's `HTTPException` to return appropriate HTTP
errors, including:

-   `404 Not Found` when a requested student or course does not exist.
-   `400 Bad Request` when a duplicate student registration number is
    detected, if that check is enabled in the router.
-   `422 Unprocessable Entity` when request data fails FastAPI/Pydantic
    validation.

## Development Notes

-   Do not commit database passwords, API keys, or other secrets.
-   Add `.venv/`, `.env`, and Python cache files to `.gitignore`.
-   Use database migrations when changing existing schemas.
-   Consider adding pagination and filtering for large student/course
    lists.
-   Consider adding authentication and authorization before exposing the
    API publicly.
-   Use `PATCH` for partial updates if you later need to update only
    selected fields.

## License

Add a license before distributing or publishing this project. If no
license is specified, all rights remain with the copyright holder.
