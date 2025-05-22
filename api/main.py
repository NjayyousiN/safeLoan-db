from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v1.courses.route import router as course_router
from v1.auth.route import router as auth_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(course_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")  
def read_root():
    return {"Hello": "World"}