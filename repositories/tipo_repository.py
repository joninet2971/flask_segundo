from app import db

from models import Tipo

class TipoRepository:
    def get_all(self):
        return Tipo.query.all()
    
    def create(self, nombre):
        nuevo_tipo = Tipo(nombre=nombre)
        db.session.add(nuevo_tipo)
        db.session.commit()
        return nuevo_tipo
