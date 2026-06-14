from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    return round(weight_kg / ((height_cm / 100) ** 2), 2)

@router.post("/", response_model=schemas.ProgressOut, status_code=status.HTTP_201_CREATED)
def create_progress(item: schemas.ProgressCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    data = item.model_dump(); data["bmi"] = calculate_bmi(data["weight_kg"], data["height_cm"])
    new_item = models.Progress(**data, user_id=current_user.id)
    db.add(new_item); db.commit(); db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[schemas.ProgressOut])
def get_progress(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Progress).filter(models.Progress.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=schemas.ProgressOut)
def get_progress_record(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Progress).filter(models.Progress.id == item_id, models.Progress.user_id == current_user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Progress record not found")
    return item

@router.put("/{item_id}", response_model=schemas.ProgressOut)
def update_progress(item_id: int, item_data: schemas.ProgressCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Progress).filter(models.Progress.id == item_id, models.Progress.user_id == current_user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Progress record not found")
    data = item_data.model_dump(); data["bmi"] = calculate_bmi(data["weight_kg"], data["height_cm"])
    for key, value in data.items(): setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_progress(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Progress).filter(models.Progress.id == item_id, models.Progress.user_id == current_user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Progress record not found")
    db.delete(item); db.commit()
    return {"message": "Progress record deleted successfully"}
