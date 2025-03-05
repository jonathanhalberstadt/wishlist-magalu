import unittest
from flask import Flask
from api.infrastructure.extensions import db
from api.domain.services.clients import create_client, get_client, update_client, delete_client

class ClientServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Configuração inicial do Flask para testes"""
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True

        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        """Limpa o banco de dados após cada teste"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_client_success(self):
        """Testa a criação de um cliente com sucesso"""
        with self.app.app_context():
            response = create_client("John Doe", "john@example.com")
            self.assertEqual(response[1], 201)
            self.assertIn("Cliente criado com sucesso", response[0].json["mensagem"])

    def test_create_client_existing_email(self):
        """Testa tentativa de criar um cliente com e-mail já cadastrado"""
        with self.app.app_context():
            create_client("John Doe", "john@example.com")
            response = create_client("Jane Doe", "john@example.com")
            self.assertEqual(response[1], 400)
            self.assertIn("E-mail já cadastrado", response[0].json["erro"])

    def test_get_client_success(self):
        """Testa buscar um cliente existente"""
        with self.app.app_context():
            create_client("John Doe", "john@example.com")
            response = get_client("john@example.com")
            self.assertEqual(response[1], 200)
            self.assertEqual(response[0].json["name"], "John Doe")

    def test_get_client_not_found(self):
        """Testa buscar um cliente inexistente"""
        with self.app.app_context():
            response = get_client("notfound@example.com")
            self.assertEqual(response[1], 404)
            self.assertIn("Cliente não encontrado", response[0].json["erro"])

    def test_update_client_success(self):
        """Testa atualização de um cliente existente"""
        with self.app.app_context():
            create_client("John Doe", "john@example.com")
            response = update_client("john@example.com", {"name": "John Updated"})
            self.assertEqual(response[1], 200)
            self.assertIn("Cliente atualizado com sucesso", response[0].json["mensagem"])

    def test_update_client_not_found(self):
        """Testa tentativa de atualizar um cliente inexistente"""
        with self.app.app_context():
            response = update_client("notfound@example.com", {"name": "Test"})
            self.assertEqual(response[1], 404)
            self.assertIn("Cliente não encontrado", response[0].json["erro"])

    def test_delete_client_success(self):
        """Testa remover um cliente existente"""
        with self.app.app_context():
            create_client("John Doe", "john@example.com")
            response = delete_client("john@example.com")
            self.assertEqual(response[1], 200)
            self.assertIn("Cliente removido com sucesso", response[0].json["mensagem"])

    def test_delete_client_not_found(self):
        """Testa tentar remover um cliente inexistente"""
        with self.app.app_context():
            response = delete_client("notfound@example.com")
            self.assertEqual(response[1], 404)
            self.assertIn("Cliente não encontrado", response[0].json["erro"])

if __name__ == "__main__":
    unittest.main()
