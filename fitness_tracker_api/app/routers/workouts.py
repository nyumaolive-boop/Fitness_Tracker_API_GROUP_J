from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post("/", response_model=schemas.WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_workout = models.Workout(**workout.model_dump(), user_id=current_user.id)
    db.add(new_workout); db.commit(); db.refresh(new_workout)
    return new_workout

@router.get("/", response_model=List[schemas.WorkoutOut])
def get_workouts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Workout).filter(models.Workout.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/{workout_id}", response_model=schemas.WorkoutOut)
def get_workout(workout_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id, models.Workout.user_id == current_user.id).first()
    if not workout: raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.put("/{workout_id}", response_model=schemas.WorkoutOut)
def update_workout(workout_id: int, workout_data: schemas.WorkoutCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id, models.Workout.user_id == current_user.id).first()
    if not workout: raise HTTPException(status_code=404, detail="Workout not found")
    for key, value in workout_data.model_dump().items(): setattr(workout, key, value)
    db.commit(); db.refresh(workout)
    return workout

@router.delete("/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id, models.Workout.user_id == current_user.id).first()
    if not workout: raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout); db.commit()
    return {"message": "Workout deleted successfully"}
