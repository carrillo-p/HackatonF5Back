import pytest
from fastapi.testclient import TestClient
from src.API_chatbot import app  # Asegúrate de que el nombre del archivo sea correcto

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat/", json={"message": "Hola, ¿cómo estás?"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_chat_endpoint_with_empty_message():
    response = client.post("/chat/", json={"message": ""})
    assert response.status_code == 200
    assert "response" in response.json()

def test_chat_endpoint_with_invalid_json():
    response = client.post("/chat/", data="Invalid JSON")
    assert response.status_code == 422 