from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(**user.dict(exclude={'password'}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_survey(db: Session, survey: schemas.SurveyCreate, user_id: int):
    db_survey = models.Survey(**survey.dict(), user_id=user_id)
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey