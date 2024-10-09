from flask import request, jsonify, Blueprint

from datetime import timedelta

from flask_jwt_extended import (
    get_jwt,
    jwt_required,
    create_access_token,
    )
from app import db
from models import User
from schemas import UserSchema, MinimalUserSchema

from werkzeug.security import (generate_password_hash,
                      check_password_hash,)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/users", methods=['POST', 'GET'])
@jwt_required()
def users():
    print(get_jwt())
    aditional_data=get_jwt()
    administrador = aditional_data.get('administrador')
    if request.method == 'POST':
        if administrador is True:
            data = request.get_json()
            username = data.get('nombre_usuario')
            password = data.get('password')

            password_hasheada = generate_password_hash(
                password = password,
                method = 'pbkdf2',
                salt_length = 8,
            )

            try:
                nuevoUsuario = User(username=username, password=password_hasheada)

                db.session.add(nuevoUsuario)
                db.session.commit()
                return jsonify({"message": "Usuario Creado"})
            except:
                return jsonify({"message": "Error al crear el usuario"})
        return jsonify(Mensaje = "usted no esta habilitado para crear usuario")
    if administrador is True:
        usuarios = User.query.all()
        return UserSchema().dump(usuarios, many=True)
    else:
        usuarios = User.query.all()
        return MinimalUserSchema().dump(usuarios, many=True)
    usuarios = User.query.all()
    return UserSchema().dump(usuarios, many =True)
    

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.authorization
    username = data.username
    password = data.password

    usuario = User.query.filter_by(username=username).first()

    if usuario and check_password_hash(pwhash=usuario.password, password=password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=10),
            additional_claims=dict(
                administrador = usuario.is_admin
            )
        )
        return jsonify({"mensaje":f"Token {access_token}"})
    return jsonify({"mensaje": "no logueado"})