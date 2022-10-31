from flask import Flask, jsonify, request
from info_album.album import Album
from info_equipos.teams import equipos
from groups import grupos
import random

"""
Clase que contendrá todas las rutas a las que el usuario puede acceder
para obtener información o realizar alguna acción específica
"""

app = Flask(__name__)
albumes = []
id_teams = equipos.devolver_id_equipos()

@app.route('/')
def index():
    return {"msg": "Funciona :D"}, 200

# Obtener álbumes creados
@app.route('/api/album', methods=['GET'])
def obtener_lista_albumes():
    album_existentes = []
    for album in albumes:
        album_existentes.append({"id": album.id, "name": album.name, "created_at": album.created_at})
    return jsonify(album_existentes), 200

# Crear un álbum
@app.route('/api/album', methods=['POST'])
def crear_album():
    try:
        if not(request.json['id'] == "" or request.json['name'] == "" or request.json['created_at'] == "") \
                and not(Album.verificar_info_vacia_id(request.json['id'])) \
                and not(Album.verificar_info_vacia_name(request.json['name'])) \
                and not(Album.verificar_info_vacia_created_at(request.json['created_at'])):
            if not (Album.verificar_album_duplicado(request.json['id'], request.json['name'], albumes)):
                albumes.append(Album(request.json['id'], request.json['name'], request.json['created_at']))
                return {"msg": "Album creado con exito"}, 200
            else:
                return {"msg": "Error, album duplicado"}, 400
        else:
            return {"msg": "Error, existen campos vacíos"}, 400
    except:
        return {"msg": "Error, faltan campos a ingresar"}, 400

# Abrir un sobre con 6 estampas aleatorias
@app.route('/api/album/<id_album>/stamp', methods=['POST'])
def abrir_sobre_estampitas(id_album):
    album_seleccionado = Album.devolver_album(id_album, albumes)
    if not(album_seleccionado == None):
        id_equipo = []
        estampitas_aleatoria = []
        for i in range(6):
            id_equipo.append(id_teams[random.randint(0, len(id_teams) - 1)])
        for team in id_equipo:
            stamps = equipos.devolver_estampitas(team)
            estampita_aleatoria = stamps[random.randint(0, len(stamps) - 1)]
            estampitas_aleatoria.append(estampita_aleatoria)
            if len(album_seleccionado.estampitas) > 0:
                if not(Album.verificar_estampita_duplicada(estampita_aleatoria['id'], album_seleccionado)):
                    album_seleccionado.estampitas.append(estampita_aleatoria)
            else:
                album_seleccionado.estampitas.append(estampita_aleatoria)
            continue
        return jsonify(estampitas_aleatoria), 200
    else:
        return {"msg": "Error, album no encontrado"}, 404

# Filtrar las estampas de un álbum por un grupo determinado
@app.route('/api/album/<id_album>/stamps/group/<id_group>', methods=['GET'])
def filtrar_estampitas_grupo(id_album, id_group):
    filtro_grupo = []
    filtro_grupo_devolver = []
    album_seleccionado = Album.devolver_album(id_album, albumes)
    if not(album_seleccionado == None):
        if len(grupos.obtener_info_grupo_especifico(id_group)) > 0:
            for id_team in grupos.obtener_info_grupo_especifico(id_group):
                for name_team in equipos.devolver_info_equipo_especifico(id_team):
                    estampitas_grupo = []
                    for estampitas in album_seleccionado.estampitas:
                        if Album.devolver_id_grupo_estampita(estampitas) == id_team:
                            estampitas_grupo.append({"id": estampitas['id'], "name": estampitas['name'],
                                                     "isPlayer": estampitas['isPlayer']})
                    filtro_grupo.append({"id": id_team, "name": name_team["name"], "elements": estampitas_grupo})
            for estampita_grupo in filtro_grupo:
                if len(estampita_grupo['elements']) > 0:
                    filtro_grupo_devolver.append(estampita_grupo)
            return jsonify(filtro_grupo_devolver), 200
        else:
            return {"msg": "Error, grupo no encontrado"}, 404
    else:
        return {"msg": "Error, album no encontrado"}, 404

# Filtrar las estampas de un álbum por un país determinado
@app.route('/api/album/<id_album>/stamps/country/<id_country>', methods=['GET'])
def filtrar_estampitas_pais(id_album, id_country):
    filtro_pais = []
    country_name = ''
    album_seleccionado = Album.devolver_album(id_album, albumes)
    if not (album_seleccionado == None):
        if equipos.buscar_pais(id_country):
            for pais in equipos.devolver_info_equipo_especifico(id_country):
                country_name = pais['name']
            estampitas_pais = []
            for estampitas in album_seleccionado.estampitas:
                if Album.devolver_id_grupo_estampita(estampitas) == id_country:
                    estampitas_pais.append({"id": estampitas['id'], "name": estampitas['name'],
                                            "isPlayer": estampitas['isPlayer']})
            filtro_pais.append({"id": id_country, "name": country_name, "elements": estampitas_pais})
            return jsonify(filtro_pais), 200
        else:
            return {"msg": "Error, pais no encontrado"}, 404
    else:
        return {"msg": "Error, album no encontrado"}, 404


# Pruebas
# Mostrar la información de todas las estampitas conseguidas en un álbum determinado
@app.route('/api/album/<id_album>', methods=['GET'])
def ver_estampitas(id_album):
    album_seleccionado = Album.devolver_album(id_album, albumes)
    if not(album_seleccionado == None):
        return jsonify(album_seleccionado.estampitas), 200
    else:
        return {"msg": "Error, album no encontrado"}, 404

if __name__ == '__main__':
    app.run(debug=True)