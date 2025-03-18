import json
import os
import requests
from api.infrastructure.extensions import db
from api.models.clients import Client
from api.models.wishlist import Wishlist
from api.models.products import Product

API_URL = "http://challenge-api.luizalabs.com/api/product/{}"
CACHE_FILE = "cache.json"

def load_cache():
    """Carrega os produtos do cache.json para caso a api não responda"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def add_favorite(client_id, product_id):
    """Adiciona um produto aos favoritos, verificando no banco, API externa e cache"""

    client = db.session.query(Client).filter_by(id=client_id).first()
    if not client:
        raise ValueError("Cliente não encontrado")

    wishlist_entry = db.session.query(Wishlist).filter_by(client_id=client_id,
                                                          product_id=product_id).first()
    if wishlist_entry:
        raise ValueError("Produto já está na lista de favoritos")

    product = db.session.query(Product).filter_by(id=product_id).first()

    if not product:
        response = requests.get(API_URL.format(product_id), timeout=2, verify=False) # nosec B501

        if response.status_code == 200:
            product_data = response.json()
        else:
            cache = load_cache()
            product_data = next((p for p in cache.values() if p["id"] == product_id), None)

        if not product_data:
            raise ValueError("Produto não encontrado")

        product = Product(
            id=product_id,
            title=product_data.get('title'),
            image=product_data.get('image'),
            url=product_data.get('url'),
            brand=product_data.get('brand'),
            price=product_data.get('price') or 0.0,
            review_score=product_data.get('reviewScore'),
        )
        db.session.add(product)
        db.session.commit()

    wishlist_entry = Wishlist(client_id=client_id, product_id=product_id)
    db.session.add(wishlist_entry)
    db.session.commit()

    return True

def get_favorites(client_identifier):
    """Retorna a lista de favoritos do cliente pelo ID ou pelo e-mail"""

    if "@" in str(client_identifier):
        client = db.session.query(Client).filter_by(email=client_identifier).first()
    else:
        try:
            client_id = int(client_identifier)  # Tenta converter para inteiro
            client = db.session.query(Client).filter_by(id=client_id).first()
        except ValueError:
            raise ValueError("ID do cliente inválido")  # Se falhar, o ID é inválido

    if not client:
        raise ValueError("Cliente não encontrado")

    favorites = (
        db.session.query(Product)
        .join(Wishlist, Product.id == Wishlist.product_id)
        .filter(Wishlist.client_id == client.id)
        .all()
    )

    return [{'id': p.id, 'title': p.title, 'image': p.image, 'url': p.url} for p in favorites]
