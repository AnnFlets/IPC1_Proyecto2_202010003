"""
Clase que contendrá una lista de álbumes y métodos para agregar
un álbum y para mostrar todos los álbumes agregados
"""

class Album:

    def __init__(self, id, name, created_at):
        self._id = id
        self._name = name
        self._created_at = created_at
        self._estampitas = []

    # Métodos Get
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def created_at(self):
        return self._created_at

    @property
    def estampitas(self):
        return self._estampitas

    # Método que busca y retorna un álbum por medio del id
    def devolver_album(id, albumes):
        for album_buscado in albumes:
            if album_buscado.id == id:
                return album_buscado
        return None

    # Método que comprueba que no existan álbumes duplicados tanto en id como en name
    def verificar_album_duplicado(id, name, albumes):
        album_duplicado = []
        if len(albumes) > 0:
            for album_verificar in albumes:
                if album_verificar.id == id or album_verificar.name == name:
                    album_duplicado.append(album_verificar)
            if len(album_duplicado) > 0:
                return True
            else:
                return False
        else:
            return False

    # Métodos que comprueban que los atributos no sean únicamente espacios
    def verificar_info_vacia_id(id):
        for letra in id:
            if not (letra == " "):
                return False
        return True

    def verificar_info_vacia_name(name):
        for letra in name:
            if not (letra == " "):
                return False
        return True

    def verificar_info_vacia_created_at(created_at):
        for letra in created_at:
            if not (letra == " "):
                return False
        return True

    # Método que comprueba si una estampa está duplicada
    def verificar_estampita_duplicada(id_estampita, album):
        for estampita in album.estampitas:
            if estampita['id'] == id_estampita:
                print("Estampita duplicada: " + estampita['id'])
                return True
        return False

    # Método que devuelve el id del grupo al que pertenece una estampa
    def devolver_id_grupo_estampita(estampitas):
        contador = 0
        id_estampa = ''
        for letra in estampitas['id']:
            if contador < 3:
                id_estampa += letra
            contador += 1
        return id_estampa