from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])

@router.post("/", response_model=schemas.NutritionOut, status_code=status.HTTP_201_CREATED)
def create_nutrition(item: schemas.NutritionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_item = models.Nutrition(**item.model_dump(), user_id=current_user.id)
    db.add(new_item); db.commit(); db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[schemas.NutritionOut])
def get_nutrition(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Nutrition).filter(models.Nutrition.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=schemas.NutritionOut)
def get_nutrition_record(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Nutrition).filter(models.Nutrition.id == item_id, models.Nutrition.user_id == current_user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Nutrition record not found")
    return item

@router.put("/{item_id}", response_model=schemas.NutritionOut)
def update_nutrition(item_id: int, item_data: schemas.NutritionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Nutrition).filter(models.Nutrition.id == item_id, models.Nutrition.user_id == current_user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Nutrition record not found")
    for key, value in item_data.model_dump().items(): setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_nutrition(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Nutrition).filter(models.Nutrition.id == item_id, models.Nutrition.user_id == current_user.id).first()
    if not item: raise HTTPException(status_code=404, detail="Nutrition record not found")
    db.delete(item); db.commit()
    return {"message": "Nutrition record deleted successfully"}
