from flask import jsonify
from api.infrastructure.extensions import db
from api.models.clients import Client

def create_client(name, email):
    """Cria um novo cliente no banco."""
    existing_client = Client.query.filter_by(email=email).first()

    if existing_client:
        return jsonify({"erro": "E-mail já cadastrado"}), 400

    client = Client(name=name, email=email)
    db.session.add(client)
    db.session.commit()

    return jsonify({"mensagem": "Cliente criado com sucesso"}), 201

def get_client(email):
    """Busca um cliente pelo e-mail."""
    client = Client.query.filter_by(email=email).first()

    if not client:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({
        "id": client.id,
        "name": client.name,
        "email": client.email
    }), 200

def update_client(email, new_data):
    """Atualiza o nome de um cliente pelo e-mail."""
    client = Client.query.filter_by(email=email).first()

    if not client:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    if "name" in new_data:
        client.name = new_data["name"]
        db.session.commit()
        return jsonify({"mensagem": "Cliente atualizado com sucesso"}), 200

    return jsonify({"erro": "Nenhum campo válido para atualização"}), 400

def delete_client(email):
    """Remove um cliente pelo e-mail."""
    client = Client.query.filter_by(email=email).first()

    if not client:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({"mensagem": "Cliente removido com sucesso"}), 200
