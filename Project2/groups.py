import json

"""
Clase que devuelve un diccionario de datos del
archivo JSON 'groups' y tiene métodos relacionados
al mismo
"""

class Groups:

    # Método que retorna una lista la información del archivo json 'groups'
    @staticmethod
    def obtener_info_grupos():
        with open('groups.json', 'r') as grupo:
            info_grupos = json.load(grupo)
        return info_grupos

    # Método que retorna una lista con los equipos pertenecientes a un grupo específico
    @staticmethod
    def obtener_info_grupo_especifico(id_group):
        info_grupo_seleccionado = []
        for grupo in Groups.obtener_info_grupos():
            if grupo['group'] == id_group:
                for teams in grupo['teams']:
                    info_grupo_seleccionado.append(teams)
        return info_grupo_seleccionado

grupos = Groups()

# Pruebas
if __name__ == '__main__':
    print(type(Groups.obtener_info_grupos()))
    print(Groups.obtener_info_grupos())
    print(Groups.obtener_info_grupo_especifico("a"))