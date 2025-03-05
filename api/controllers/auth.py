import secrets
import time
from flask import Blueprint, request, jsonify

bp = Blueprint('auth', __name__, url_prefix='/auth')

active_tokens = {}

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    """Autentica um usuário e retorna um token válido por 10 minutos."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    token = secrets.token_hex(32)

    active_tokens[token] = time.time() + 600

    return jsonify({"access_token": token, "expires_in": 600}), 200

def token_required(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token é obrigatório"}), 401

        if token not in active_tokens or time.time() > active_tokens[token]:
            return jsonify({"error": "Token inválido ou expirado"}), 401

        return f(*args, **kwargs)

    decorated_function.__name__ = f.__name__
    return decorated_function
