from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash, verify_password
from schemas import SurveyCreate
from models import Survey

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def verificar_usuario(db: Session, username: str, password: str):
    user = get_user_by_email(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(**user.dict(exclude={'password'}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_survey(db: Session, survey: SurveyCreate, user_id: int):
    # Sumar todos los campos para calcular el nivel de depresión
    depresion_value = (
        survey.tristeza + survey.pesimismo + survey.fracaso +
        survey.perdida_placer + survey.culpa + survey.castigo +
        survey.disconformidad + survey.autocritica + survey.suicidio +
        survey.llanto + survey.agitacion + survey.interes +
        survey.indeciso + survey.desvalorizacion + survey.energia +
        survey.irritabilidad + survey.concentracion + survey.cansancio +
        survey.sexo
    )

    # Crear el objeto de encuesta con el valor de depresión calculado
    db_survey = Survey(
        user_id=user_id,
        tristeza=survey.tristeza,
        pesimismo=survey.pesimismo,
        fracaso=survey.fracaso,
        perdida_placer=survey.perdida_placer,
        culpa=survey.culpa,
        castigo=survey.castigo,
        disconformidad=survey.disconformidad,
        autocritica=survey.autocritica,
        suicidio=survey.suicidio,
        llanto=survey.llanto,
        agitacion=survey.agitacion,
        interes=survey.interes,
        indeciso=survey.indeciso,
        desvalorizacion=survey.desvalorizacion,
        energia=survey.energia,
        irritabilidad=survey.irritabilidad,
        concentracion=survey.concentracion,
        cansancio=survey.cansancio,
        sexo=survey.sexo,
        depresion=depresion_value  
    )

    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey