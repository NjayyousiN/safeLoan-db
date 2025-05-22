from fastapi import Depends, Response, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Student
from db.CRUD import create_student
from utils.jwt_utils import create_tokens, set_auth_cookies, get_current_user
from utils.hashing_pass import verify_password, hash_password
from schemas.auth import UserLogin, UserResponse, UserCreate
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK) 
async def login(
    user: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
): 
    user_db = db.query(Student).filter(Student.email == user.email).first()
    if not user or not verify_password(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token, refresh_token = create_tokens({"sub": user.email})
    set_auth_cookies(response, access_token, refresh_token)

    return UserResponse(
        id=user_db.id,
        email=user_db.email,
        name=user_db.name
    )

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
): 
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    response: Response,
    db: Session = Depends(get_db),
): 
    existing_user = db.query(Student).filter(Student.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    # Hash the password before storing it
    hashed_password = hash_password(user.password)

    new_user = create_student(
        db=db,
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    # Set auth cookies
    access_token, refresh_token = create_tokens({"sub": new_user.email})
    set_auth_cookies(response, access_token, refresh_token)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name

    )

# Create a protected route to get user info
# @router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
# async def get_current_user(
#     user: UserResponse = Depends(get_current_user),
# ): 
#     return user

