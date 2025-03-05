from flask import Blueprint, request
from api.domain.services.clients import create_client, get_client, update_client, delete_client
from api.controllers.auth import token_required

bp = Blueprint('client', __name__, url_prefix='/client')

@bp.route("/", methods=["POST"])
@token_required
def register_client():
    data = request.json
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {"erro": "Nome e e-mail são obrigatórios"}, 400

    return create_client(name, email)

@bp.route("/<email>", methods=["GET"])
@token_required
def view_client(email):
    return get_client(email)

@bp.route("/<email>", methods=["PUT"])
@token_required
def edit_client(email):
    new_data = request.json

    if not new_data:
        return {"erro": "Dados para atualização são obrigatórios"}, 400

    return update_client(email, new_data)

@bp.route("/<email>", methods=["DELETE"])
@token_required
def remove_client(email):
    return delete_client(email)
