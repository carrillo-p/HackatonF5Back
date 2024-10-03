from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(64))
    name = Column(String(100))
    address = Column(String(255))
    phone = Column(String(20))
    profession = Column(String(100))
    gender = Column(Enum('masculino', 'femenino', 'intergenero', 'nc'))
    age = Column(Integer)
    is_mentor = Column(Boolean, default=False)
    wants_survey = Column(Boolean, default=False)
    wants_events = Column(Boolean, default=False)

    surveys = relationship("Survey", back_populates="user")

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tristeza = Column(Integer)
    pesimismo = Column(Integer)
    fracaso = Column(Integer)
    perdida_placer = Column(Integer)
    culpa = Column(Integer)
    castigo = Column(Integer)
    disconformidad = Column(Integer)
    autocritica = Column(Integer)
    suicidio = Column(Integer)
    llanto = Column(Integer)
    agitacion = Column(Integer)
    interes = Column(Integer)
    indeciso = Column(Integer)
    desvalorizacion = Column(Integer)
    energia = Column(Integer)
    irritabilidad = Column(Integer)
    concentracion = Column(Integer)
    cansancio = Column(Integer)
    sexo = Column(Integer)

    user = relationship("User", back_populates="surveys")