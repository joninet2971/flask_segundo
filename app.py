import bcrypt
import os
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import (
    JWTManager,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    create_access_token,
    )
from werkzeug.security import (generate_password_hash,
                      check_password_hash,
                      )

app = Flask(__name__)

# Configuracion de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI'
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY'
    )

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from models import Marca, Tipo, Vehiculo, User
from forms import MarcaForm, TipoForm
from services.marca_service import MarcaService
from services.tipo_service import TipoService
from repositories.marca_repository import MarcaRepository
from repositories.tipo_repository import TipoRepository

load_dotenv()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/users", methods=['POST', 'GET'])
@jwt_required()
def users():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('nombre_usuario')
        password = data.get('password')

        password_hasheada = generate_password_hash(
            password = password,
            method = 'pbkdf2',
            salt_length = 8,
        )
        print(password_hasheada)

        try:
            nuevoUsuario = User(username=username, password=password_hasheada)

            db.session.add(nuevoUsuario)
            db.session.commit()
            return jsonify({"message": "Usuario Creado"})
        except:
            return jsonify({"message": "Error al crear el usuario"})
    return jsonify({"usuario creado": "listado"})
    

@app.route("/login", methods=['POST'])
def login():
    data = request.authorization
    username = data.username
    password = data.password

    usuario = User.query.filter_by(username=username).first()

    if usuario and check_password_hash(pwhash=usuario.password, password=password):
        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=3)
        )
        return jsonify({"mensaje":f"Token {access_token}"})
    return jsonify({"mensaje": "no logueado"})


@app.route("/marca_list", methods=['POST', 'GET'])
def marcas():   
    marca_service = MarcaService(MarcaRepository())
    marcas = marca_service.get_all()

    formulario = MarcaForm()

    if request.method == 'POST':
        nombre=formulario.nombre.data
        marca_service.create(nombre)
        return redirect(url_for('marcas'))

    return render_template(
        'marca_list.html',
        marcas=marcas, 
        formulario=formulario,
    )

@app.route("/marca/<id>/vehiculos")
def vehiculos_por_marca(id):
    #vehiculos = Vehiculo.query.filter_by(marca_id=id)
    marca = Marca.query.get_or_404(id)
    vehiculos = marca.vehiculos
    return render_template(
        "vehiculos_by_marca.html",
        vehiculos=vehiculos,
        marca=marca
    )

@app.route("/marca/<id>/editar", methods=['GET', 'POST'])
def marca_editar(id):
    marca = Marca.query.get_or_404(id)

    if request.method == 'POST':
        marca.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('marcas'))

    return render_template(
        "marca_edit.html",
        marca=marca
    )

@app.route("/tipo_list", methods=['POST', 'GET'])
def tipos():
    tipo_service = TipoService(TipoRepository())
    tipos = tipo_service.get_all()

    formulario = TipoForm()

    if request.method == 'POST':
        nombre=formulario.nombre.data
        tipo_service.create(nombre)
        return redirect(url_for('tipos'))
    
    return render_template('tipo_list.html',
                           tipos=tipos,
                           formulario=formulario,
                           )


@app.route("/vehiculos_list", methods = ['POST', 'GET'])
def vehiculos():
    vehiculos = Vehiculo.query.all()
    marcas = Marca.query.all()
    tipos = Tipo.query.all()

    if request.method == 'POST':
        modelo = request.form['modelo']
        anio = request.form['anio_fabricacion']
        precio = request.form['precio']
        marca = request.form['marca']
        tipo = request.form['tipo']
        vehiculo_nuevo = Vehiculo(
            modelo=modelo,
            anio_fabricacion=anio,
            precio=precio,
            marca_id=marca,
            tipo_id=tipo,
        )
        db.session.add(vehiculo_nuevo)
        db.session.commit()
        return redirect(url_for('vehiculos'))

    return render_template(
        'vehiculos_list.html',
        vehiculos=vehiculos,
        marcas=marcas,
        tipos=tipos,
    )

if __name__ == "__main__":
    app.run(
    host="0.0.0.0",
    port=5005,
    debug=True,
    )