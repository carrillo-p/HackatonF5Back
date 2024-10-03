import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
import crud
import models
import schemas

class TestCRUD(unittest.TestCase):

    def setUp(self):
        # Crear una sesión mock de SQLAlchemy
        self.db = MagicMock(Session)
        
        # Datos de prueba
        self.user_data = schemas.UserCreate(email="test@example.com", password="password123")
        self.user = models.User(id=1, email=self.user_data.email, hashed_password="hashed_password")
        self.survey_data = schemas.SurveyCreate(title="Test Survey")

    def test_create_user(self):
        # Simula la creación de un usuario
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        
        user = crud.create_user(self.db, self.user_data)
        
        # Verifica que se haya llamado a los métodos adecuados
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        
        self.assertEqual(user.email, self.user_data.email)

    def test_get_user(self):
        # Simula que la consulta devuelve un usuario
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        
        user = crud.get_user(self.db, 1)
        
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, self.user.email)

    def test_get_user_by_email(self):
        # Simula que la consulta devuelve un usuario por correo
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        
        user = crud.get_user_by_email(self.db, "test@example.com")
        
        self.assertEqual(user.email, "test@example.com")

    def test_verificar_usuario_success(self):
        # Simula la verificación de usuario
        self.db.query.return_value.filter.return_value.first.return_value = self.user
        crud.verify_password = MagicMock(return_value=True)
        
        user = crud.verificar_usuario(self.db, "test@example.com", "password123")
        
        self.assertEqual(user.id, self.user.id)

    def test_verificar_usuario_failure(self):
        # Simula la verificación de usuario fallida
        self.db.query.return_value.filter.return_value.first.return_value = None
        
        user = crud.verificar_usuario(self.db, "wrong@example.com", "wrongpassword")
        
        self.assertIsNone(user)

    def test_create_survey(self):
        # Simula la creación de una encuesta
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        
        survey = crud.create_survey(self.db, self.survey_data, user_id=1)
        
        # Verifica que se haya llamado a los métodos adecuados
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        
        self.assertEqual(survey.title, self.survey_data.title)

if __name__ == '__main__':
    unittest.main()
