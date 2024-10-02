from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.chatbot import PsychologistChatbot  # Importar la clase desde chatbot.py

# Crear una instancia de FastAPI
app = FastAPI()

# Crear una instancia del chatbot psicólogo
chatbot = PsychologistChatbot()

# Modelo Pydantic para validar el input del usuario
class UserInput(BaseModel):
    message: str

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

# Punto de entrada principal para ejecutar el servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)