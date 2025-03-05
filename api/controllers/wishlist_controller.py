from flask import Blueprint, request, jsonify
from api.domain.services.wishlist import add_favorite, get_favorites
from api.controllers.auth import token_required

bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@bp.route('/', methods=['POST'])
@token_required
def add_to_favorites():
    data = request.json
    client_id = data.get('client_id')
    product_id = data.get('product_id')

    if not client_id or not product_id:
        return jsonify({'error': 'client_id e product_id são obrigatórios'}), 400

    try:
        add_favorite(client_id, product_id)
        return jsonify({'message': 'Produto adicionado aos favoritos'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Erro inesperado ao adicionar o produto'}), 500

@bp.route('/', methods=['GET'])
@token_required
def list_favorites():
    client_identifier = request.args.get('client_id') or request.args.get('email')

    if not client_identifier:
        return jsonify({'error': 'Informe o client_id ou o email'}), 400

    try:
        favorites = get_favorites(client_identifier)
        return jsonify({'wishlist': favorites}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        return jsonify({'error': 'Erro inesperado ao buscar favoritos'}), 500
