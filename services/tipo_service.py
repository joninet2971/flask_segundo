from repositories.tipo_repository import TipoRepository

class TipoService:
    def __init__(self, tipo_repository: TipoRepository):
        self._tipo_repository = tipo_repository

    def get_all(self):
        return self._tipo_repository.get_all()
    
    def create(self, nombre):
        return self._tipo_repository.create(nombre)
