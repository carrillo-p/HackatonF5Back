import unittest
from unittest.mock import patch, MagicMock
from auth import verify_password, get_password_hash, authenticate_user
import crud

class TestAuth(unittest.TestCase):

    @patch('auth.pwd_context.verify')
    def test_verify_password(self, mock_verify):
        # Simulamos el comportamiento de la función verify
        mock_verify.return_value = True
        self.assertTrue(verify_password("plain_password", "hashed_password"))
        mock_verify.assert_called_once_with("plain_password", "hashed_password")

    @patch('auth.pwd_context.hash')
    def test_get_password_hash(self, mock_hash):
        # Simulamos el comportamiento de la función hash
        mock_hash.return_value = "hashed_password"
        hashed = get_password_hash("password")
        self.assertEqual(hashed, "hashed_password")
        mock_hash.assert_called_once_with("password")

    @patch('crud.get_user_by_email')
    @patch('auth.verify_password')
    def test_authenticate_user_success(self, mock_verify_password, mock_get_user_by_email):
        # Simulamos que el usuario existe y la verificación de contraseña es correcta
        mock_user = MagicMock(hashed_password="hashed_password")
        mock_get_user_by_email.return_value = mock_user
        mock_verify_password.return_value = True

        db = MagicMock()  # Simulamos una sesión de base de datos
        user = authenticate_user(db, "test@example.com", "password")
        self.assertEqual(user, mock_user)

    @patch('crud.get_user_by_email')
    @patch('auth.verify_password')
    def test_authenticate_user_user_not_found(self, mock_verify_password, mock_get_user_by_email):
        # Simulamos que el usuario no existe
        mock_get_user_by_email.return_value = None

        db = MagicMock()  # Simulamos una sesión de base de datos
        user = authenticate_user(db, "test@example.com", "password")
        self.assertFalse(user)

    @patch('crud.get_user_by_email')
    @patch('auth.verify_password')
    def test_authenticate_user_invalid_password(self, mock_verify_password, mock_get_user_by_email):
        # Simulamos que el usuario existe pero la verificación de la contraseña falla
        mock_user = MagicMock(hashed_password="hashed_password")
        mock_get_user_by_email.return_value = mock_user
        mock_verify_password.return_value = False

        db = MagicMock()  # Simulamos una sesión de base de datos
        user = authenticate_user(db, "test@example.com", "password")
        self.assertFalse(user)

if __name__ == '__main__':
    unittest.main()
