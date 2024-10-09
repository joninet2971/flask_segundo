from app import ma
from models import User, Tipo, Marca, Vehiculo

from models import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    password =  ma.auto_field()
    is_admin = ma.auto_field()


class MinimalUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()

class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Marca

    username = ma.auto_field()

class TipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tipo

    username = ma.auto_field()

class VehiculosSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Vehiculo

    modelo = ma.auto_field()
    anio_fabricacion = ma.auto_field()
    precio = ma.auto_field()
    marca = ma.Nested(MarcaSchema)
    tipo = ma.Nested(TipoSchema)