import os
import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from database import SQLALCHEMY_DATABASE_URL


class TestDatabase(unittest.TestCase):

    @patch("database.SessionLocal")
    def test_get_db(self, mock_session_local):
        # Configurar el mock para simular una sesión de base de datos
        mock_db = MagicMock(spec=Session)
        mock_session_local.return_value = mock_db
        
        db_generator = get_db()
        db_instance = next(db_generator)  # Obtiene la instancia de la base de datos
        
        self.assertEqual(db_instance, mock_db)
        
        # Verifica que se cierre la sesión después de usarla
        db_generator.close()  # Cierra el generador
        mock_db.close.assert_called_once()

    def test_database_url(self):
        # Prueba que la URL de la base de datos se construya correctamente
        expected_url = (
            f"mysql+pymysql://{os.getenv('DB_USERNAME')}:"
            f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        self.assertEqual(expected_url, SQLALCHEMY_DATABASE_URL)


if __name__ == '__main__':
    unittest.main()
