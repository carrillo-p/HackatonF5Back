from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import crud, models, schemas, auth
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import PsychologistChatbot 
from auth import create_access_token, authenticate_user, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

pdf_paths = ["resources/dsm-5.pdf", "resources/relajacion.pdf"] # añadir /src si se van a ejecutar los tests
web_urls = ["https://www.psychologytoday.com/us/basics/depression", "https://www.nimh.nih.gov/health/find-help", "https://www.who.int/es/news-room/fact-sheets/detail/depression", "https://www.mayoclinic.org/diseases-conditions/depression/symptoms-causes/syc-20356007", "https://www.ncbi.nlm.nih.gov/books/NBK513238/", "https://www.cdc.gov/mentalhealth/depression/index.htm"]
chatbot = PsychologistChatbot(pdf_paths=pdf_paths)

# Modelo Pydantic para validar el input del usuario
class UserInput(BaseModel):
    message: str

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los headers
)

# Crear usuario (POST /users/)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Login y generación de token JWT (POST /login/)
@app.post("/login/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Crear encuesta (POST /surveys/)
@app.post("/surveys/", response_model=schemas.Survey)
async def create_survey(survey: schemas.SurveyCreate, user_id: int, db: Session = Depends(get_db)):
    # Aquí asumimos que el `user_id` es pasado por el front después de un login exitoso
    return crud.create_survey(db=db, survey=survey, user_id=user_id)

# Obtener datos del usuario autenticado (GET /users/me/)
@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(username: str, password: str, db: Session = Depends(get_db)):
    usuario = crud.verificar_usuario(db, username, password)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return usuario

@app.post("/chat/")
async def chat(user_input: UserInput):
    """
    Endpoint que recibe un mensaje de un usuario y devuelve la respuesta del chatbot psicólogo AI.
    """
    try:
        # Obtener la respuesta del chatbot
        response = chatbot.get_response(user_input.message)
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)