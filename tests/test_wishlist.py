import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.infrastructure.extensions import db
from api.models.clients import Client
from api.models.wishlist import Wishlist
from api.models.products import Product
from api.domain.services.wishlist import add_favorite, get_favorites

class WishlistServiceTestCase(unittest.TestCase):
    def setUp(self):
        """Configuração inicial do Flask e banco de dados"""
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

    def test_add_favorite_success(self):
        """Testa adicionar um produto favorito com sucesso"""
        with self.app.app_context():
            client = Client(id=1, name="João da silva", email="joao@exemple.com")
            db.session.add(client)
            db.session.commit()

            product = Product(id="123", title="Produto Teste",
                              image="image.jpg", url="https://example.com",
                              price=123.45)

            db.session.add(product)
            db.session.commit()

            result = add_favorite(1, "123")
            self.assertTrue(result)

            wishlist_entry = Wishlist.query.filter_by(client_id=1, product_id="123").first()
            self.assertIsNotNone(wishlist_entry)

    def test_add_favorite_client_not_found(self):
        """Testa erro ao tentar adicionar um favorito para um cliente inexistente"""
        with self.app.app_context():
            with self.assertRaises(ValueError) as context:
                add_favorite(999, "123")
            self.assertEqual(str(context.exception), "Cliente não encontrado")

    def test_add_favorite_product_not_found(self):
        """Testa erro ao tentar adicionar um favorito para um produto inexistente"""
        with self.app.app_context():
            client = Client(id=1, name="João da silva", email="joao@exemple.com")
            db.session.add(client)
            db.session.commit()

            with self.assertRaises(ValueError) as context:
                add_favorite(1, "999")
            self.assertEqual(str(context.exception), "Produto não encontrado")

    @patch("requests.get")
    def test_add_favorite_product_from_api(self, mock_get):
        """Testa adicionar um produto vindo da API externa"""
        with self.app.app_context():
            client = Client(id=1, name="João da silva", email="joao@exemple.com")
            db.session.add(client)
            db.session.commit()

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": "999",
                "title": "Produto API",
                "image": "image_api.jpg",
                "url": "http://api.example.com",
                "brand": "Marca",
                "price": 100.0,
                "reviewScore": 4.5
            }
            mock_get.return_value = mock_response

            result = add_favorite(1, "999")
            self.assertTrue(result)

            product = Product.query.filter_by(id="999").first()
            self.assertIsNotNone(product)
            self.assertEqual(product.title, "Produto API")

    def test_get_favorites_success(self):
        """Testa recuperar lista de favoritos de um cliente"""
        with self.app.app_context():
            client = Client(id=1, name="João da silva", email="joao@exemple.com")
            product = Product(id="123", title="Produto Teste",
                              image="image.jpg", url="https://example.com",
                              price=123.45)

            db.session.add(client)
            db.session.add(product)
            db.session.commit()

            wishlist_entry = Wishlist(client_id=1, product_id="123")
            db.session.add(wishlist_entry)
            db.session.commit()

            favorites = get_favorites(1)
            self.assertEqual(len(favorites), 1)
            self.assertEqual(favorites[0]["title"], "Produto Teste")

    def test_get_favorites_by_email(self):
        """Testa recuperar favoritos usando o e-mail do cliente"""
        with self.app.app_context():
            client = Client(id=1, name="João da silva", email="joao@exemple.com")
            product = Product(id="123", title="Produto Teste",
                              image="image.jpg", url="https://example.com",
                              price=123.45)

            db.session.add(client)
            db.session.add(product)
            db.session.commit()

            wishlist_entry = Wishlist(client_id=1, product_id="123")
            db.session.add(wishlist_entry)
            db.session.commit()

            favorites = get_favorites("joao@exemple.com")
            self.assertEqual(len(favorites), 1)
            self.assertEqual(favorites[0]["title"], "Produto Teste")

    def test_get_favorites_client_not_found(self):
        """Testa erro ao buscar favoritos de um cliente inexistente"""
        with self.app.app_context():
            with self.assertRaises(ValueError) as context:
                get_favorites("notfound@example.com")
            self.assertEqual(str(context.exception), "Cliente não encontrado")

    def test_get_favorites_invalid_client_id(self):
        """Testa erro ao passar um ID de cliente inválido"""
        with self.app.app_context():
            with self.assertRaises(ValueError) as context:
                get_favorites("invalid_id")
            self.assertEqual(str(context.exception), "ID do cliente inválido")

if __name__ == "__main__":
    unittest.main()
