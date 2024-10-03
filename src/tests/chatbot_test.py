import pytest
from src.chatbot import PsychologistChatbot

@pytest.fixture
def chatbot():
    return PsychologistChatbot()

def test_get_response(chatbot):
    response = chatbot.get_response("Hola, ¿cómo estás?")
    assert isinstance(response, str)
    assert len(response) > 0

def test_get_response_with_empty_message(chatbot):
    response = chatbot.get_response("")
    assert isinstance(response, str)
    assert len(response) > 0

def test_get_response_with_special_characters(chatbot):
    response = chatbot.get_response("!@#$%^&*()")
    assert isinstance(response, str)
    assert len(response) > 0