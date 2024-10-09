from flask import Blueprint

from models import Marca, Tipo, Vehiculo
from schemas import TipoSchema, MarcaSchema, VehiculosSchema

vehiculo_bp = Blueprint('vehiculos', __name__)

@vehiculo_bp.route('/marcas', methods=['GET'])
def marcas():
    marcas = Marca.query.all()
    return MarcaSchema.dump(marcas, many=True)

@vehiculo_bp.route('/tipos', methods=['GET'])
def tipos():
    tipos = Tipo.query.all()
    return TipoSchema.dump(tipos, many=True)

@vehiculo_bp.route('/vehiculos', methods=['GET'])
def vehiculos():
    vehiculos = Vehiculo.query.all()
    return VehiculosSchema.dump(vehiculos, many=True)
