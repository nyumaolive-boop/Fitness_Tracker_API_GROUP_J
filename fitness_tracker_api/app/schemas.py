from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class WorkoutBase(BaseModel):
    title: str
    workout_type: str
    duration_minutes: int
    calories_burned: Optional[float] = None
    workout_date: date
class WorkoutCreate(WorkoutBase): pass
class WorkoutOut(WorkoutBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class ExerciseBase(BaseModel):
    name: str
    category: str
    sets: int
    reps: int
    weight_kg: Optional[float] = None
class ExerciseCreate(ExerciseBase): pass
class ExerciseOut(ExerciseBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class NutritionBase(BaseModel):
    meal_name: str
    calories: float
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    meal_date: date
class NutritionCreate(NutritionBase): pass
class NutritionOut(NutritionBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class ProgressBase(BaseModel):
    weight_kg: float
    height_cm: float
    notes: Optional[str] = None
    progress_date: date
class ProgressCreate(ProgressBase): pass
class ProgressOut(ProgressBase):
    id: int
    bmi: Optional[float] = None
    user_id: int
    class Config:
        from_attributes = True
