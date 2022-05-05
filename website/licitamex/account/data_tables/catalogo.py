from account.models import CatalogoFiltros, Permiso
import csv
import os

def probando(uno, dos):
    route = os.getcwd()
    with open(f'{route}/account/data_tables/catalogoarticulos.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            cf=CatalogoFiltros()
            cf.grupo = row[0].strip()
            cf.familia = row[1].strip()
            cf.articulo = row[2].strip()
            cf.save()
    print("termino de agregar los valores")


def aqui(uno, dos):
    permisos = [{"label":"permisos administrador", "permiso":"administrador"},
    {"label":"permisos gerente", "permiso":"gerente"},
    {"label":"actualizar estatus licitacion", "permiso":"actualizarEstatusLicitacion"},
    {"label":"Editar Filtros", "permiso":"editarFiltros"},
    {"label":"Editar Detalle Licitacion", "permiso":"editarDetalleLicitacion"}]
    for x in permisos:
        p = Permiso()
        p.nombre=x["label"]
        p.permiso=x["permiso"]
        p.save()

