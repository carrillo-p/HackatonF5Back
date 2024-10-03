import streamlit as st
import requests
import json

# URL de la API
API_URL = "http://fastapi-app:8000/chat/"

# Función para enviar el mensaje a la API y obtener la respuesta
def get_chatbot_response(user_input):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "message": user_input
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Configuración de la página de Streamlit
st.set_page_config(page_title="Chatbot Psicólogo AI", page_icon="🤖")

st.title("Chatbot Psicólogo AI")

# Área de entrada de texto para el usuario
user_input = st.text_input("Escribe tu mensaje aquí:")

# Botón para enviar el mensaje
if st.button("Enviar"):
    if user_input:
        # Obtener la respuesta del chatbot
        response = get_chatbot_response(user_input)
        
        # Mostrar la respuesta
        st.text_area("Respuesta del Chatbot:", value=response, height=200, max_chars=None, key=None)
    else:
        st.warning("Por favor, ingresa un mensaje antes de enviar.")


st.markdown("---")
st.markdown("### Instrucciones de uso:")
st.markdown("1. Escribe tu mensaje en el campo de texto.")
st.markdown("2. Haz clic en el botón 'Enviar' para obtener una respuesta del chatbot.")
st.markdown("3. La respuesta del chatbot aparecerá en el área de texto debajo del botón.")