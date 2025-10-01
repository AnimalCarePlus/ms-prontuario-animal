from flask import Blueprint, jsonify, request
from .models import db, Animal, Consulta, Exame
from .auth import jwt_protected

api = Blueprint('api', __name__)

@api.route('/animais', methods=['POST'])
@jwt_protected
def criar_animal():
    data = request.get_json()
    animal = Animal(
        nome=data['nome'],
        tutor_nome=data['tutor_nome'],
        tutor_contato=data['tutor_contato']
    )
    db.session.add(animal)
    db.session.commit()
    return jsonify({'id': animal.id}), 201

@api.route('/animais/<int:id>', methods=['GET'])
@jwt_protected
def obter_animal(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'message': 'Animal não encontrado'}), 404

    consultas = [{
        'id': c.id,
        'data': c.data,
        'tipo': c.tipo,
        'status': c.status,
        'diagnostico': c.diagnostico,
        'tratamento': c.tratamento,
        'cirurgia': c.cirurgia,
        'peso': c.peso
    } for c in animal.consultas]

    exames = [{
        'id': e.id,
        'descricao': e.descricao,
        'imagem_url': e.imagem_url
    } for e in animal.exames]

    return jsonify({
        'id': animal.id,
        'nome': animal.nome,
        'status': animal.status,
        'tutor_nome': animal.tutor_nome,
        'tutor_contato': animal.tutor_contato,
        'consultas': consultas,
        'exames': exames
    })

@api.route('/animais/<int:id>/inativar', methods=['PUT'])
@jwt_protected
def inativar_animal(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'message': 'Animal não encontrado'}), 404
    animal.status = 'inativo'
    db.session.commit()
    return jsonify({'message': 'Animal inativado'}), 200

@api.route('/animais/<int:id>/exists', methods=['GET'])
@jwt_protected
def animal_existe(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'exists': False}), 404
    return jsonify({'exists': True, 'status': animal.status}), 200

@api.route('/animais/<int:id>/consultas', methods=['POST'])
@jwt_protected
def registrar_consulta(id):
    data = request.get_json()
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'message': 'Animal não encontrado'}), 404

    consulta = Consulta(
        data=data['data'],
        tipo=data['tipo'],
        status=data.get('status', 'agendada'),
        diagnostico=data.get('diagnostico'),
        tratamento=data.get('tratamento'),
        cirurgia=data.get('cirurgia'),
        peso=data.get('peso'),
        animal_id=id
    )
    db.session.add(consulta)
    db.session.commit()
    return jsonify({'id': consulta.id}), 201

@api.route('/animais/<int:id>/exames', methods=['POST'])
@jwt_protected
def registrar_exame(id):
    data = request.get_json()
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'message': 'Animal não encontrado'}), 404

    exame = Exame(
        descricao=data.get('descricao'),
        imagem_url=data.get('imagem_url'),
        animal_id=id
    )
    db.session.add(exame)
    db.session.commit()
    return jsonify({'id': exame.id}), 201


@api.route('/animais/<int:animal_id>', methods=['DELETE'])
@jwt_protected
def deletar_animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({'erro': 'Animal não encontrado'}), 404

    if animal.consultas or animal.exames:
        return jsonify({'erro': 'Animal possui histórico médico e não pode ser excluído. Altere o status para inativo.'}), 403

    db.session.delete(animal)
    db.session.commit()
    return jsonify({'mensagem': 'Animal excluído com sucesso'}), 200


@api.route('/animais/<int:id>/consultas', methods=['GET'])
@jwt_protected
def listar_consultas(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'message': 'Animal não encontrado'}), 404

    consultas = [{
        'id': c.id,
        'data': c.data,
        'tipo': c.tipo,
        'status': c.status,
        'diagnostico': c.diagnostico,
        'tratamento': c.tratamento,
        'cirurgia': c.cirurgia,
        'peso': c.peso
    } for c in animal.consultas]

    return jsonify({'consultas': consultas}), 200


@api.route('/animais/<int:id>/exames', methods=['GET'])
@jwt_protected
def listar_exames(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'message': 'Animal não encontrado'}), 404

    exames = [{
        'id': e.id,
        'descricao': e.descricao,
        'imagem_url': e.imagem_url
    } for e in animal.exames]

    return jsonify({'exames': exames}), 200


