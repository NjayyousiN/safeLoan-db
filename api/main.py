from fastapi import FastAPI
from v1.courses.route import router as course_router
from v1.auth.route import router as auth_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(course_router)


@app.get("/")  
def read_root():
    return {"Hello": "World"}