from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserBase(BaseModel):
    email: str
    name: str
    address: str
    phone: str
    profession: str
    gender: str
    age: int
    is_mentor: bool = False
    wants_survey: bool = False
    wants_events: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class SurveyBase(BaseModel):
    tristeza: int
    pesimismo: int
    fracaso: int
    perdida_placer: int
    culpa: int
    castigo: int
    disconformidad: int
    autocritica: int
    suicidio: int
    llanto: int
    agitacion: int
    interes: int
    indeciso: int
    desvalorizacion: int
    energia: int
    irritabilidad: int
    concentracion: int
    cansancio: int
    sexo: int

class SurveyCreate(SurveyBase):
    pass

class Survey(SurveyBase):
    id: int
    user_id: int
    depresion: int  

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None