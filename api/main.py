from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas, auth
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# Login para obtener acceso (POST /login/)
@app.post("/login/")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    usuario = crud.verificar_usuario(db, user.username, user.password)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"success": True, "user_id": usuario.id}

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
