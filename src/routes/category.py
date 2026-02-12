from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter()   # ✅ THIS MUST EXIST

@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return {"message": "List of categories"}
