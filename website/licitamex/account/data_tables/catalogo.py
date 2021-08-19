from account.models import CatalogoFiltros
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
