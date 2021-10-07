import hashlib
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from bs4 import BeautifulSoup
import requests
import datetime
import json

url = 'https://www.siapa.gob.mx/transparencia/licitaciones-estatales-y-federales'
page = requests.get(url)
soup = BeautifulSoup(page.content, features="html.parser")
dynamodb = boto3.client('dynamodb', region_name='us-west-2')



def process_table():
    table = soup.find('div', class_='field-items')
    rows = table.find_all('a')
    licitaciones_actuales = dynamodb.scan(TableName='licitaciones', ProjectionExpression="licitacion, tipo, id, descripcion", FilterExpression='entidad= :entidad', ExpressionAttributeValues= {":entidad":{"S":"SIAPA"} })
    lista_auxiliar = []

    for x in rows:
        print(x.text)
        url = "https://www.siapa.gob.mx/"+x.get("href")
        page = requests.get(url)
        content = BeautifulSoup(page.content, features="html.parser")
        licitaciones = content.find('div', class_="field-items")
        try:
            even = licitaciones.find_all('div', class_="field-item even")
            odd = licitaciones.find_all('div', class_="field-item odd")
        except:
            even = []
            odd = []
        valores = even+odd
        for row in valores:
            print("intentando")
            valor = row.find('a')
            try:
                licitacion = ""
            except:
                licitacion = ""
            try:
                base = valor.get("href")
            except:
                base = ""
            try:
                descripcion = valor.text
            except:
                descripcion = ""
            try:
                entidad = "SIAPA"
            except:
                entidad = ""
            item = {
                "id":f"{datetime.datetime.now().timestamp()}",
                'licitacion': licitacion,
                'entidad': entidad,
                'descripcion': descripcion,
                'urls': {"convocatoria": f"{base}"}
            }
            print(item)
            if item["descripcion"] != "":
                lista_auxiliar.append(item)
                result = list(filter(lambda x: x["descripcion"]["S"]==item["descripcion"], licitaciones_actuales["Items"]))
                if len(result) == 0:
                    print("agregando ")
                    d_val = {
                        "id": {"S": item["id"]},
                        "licitacion": {"S": item["licitacion"]},
                        "entidad": {"S": item["entidad"]},
                        "urls": {"M": {"convocatoria":{"S":item["urls"]["convocatoria"]}} },
                        "descripcion": {"S": item["descripcion"]}
                    }
                    dynamodb.put_item(TableName='licitaciones', Item=d_val)
                    payload = json.dumps({'id': item["id"]})
                    requests.post("http://127.0.0.1:8000/add_licitacion", data=payload)
                #llamada al server para avisar que hay una nueva licitacion

    #este for nos va a ayudar a que si en la pagina del gobierno borraron una licitacion nosotros la borremos de dynamo
    for item in licitaciones_actuales["Items"]:
        result = list(filter(lambda x: x["licitacion"] ==item["licitacion"]["S"], lista_auxiliar))
        if len(result) == 0:
            print("lo borro")
            payload = json.dumps({'id': item["id"]})
            dynamodb.delete_item(TableName='licitaciones', Key={"id":item["id"]})
            requests.post("http://127.0.0.1:8000/remove_licitacion", data=payload)
    return
        


def check_changes(hash_value):
    response = dynamodb.query(TableName='states', Select='ALL_ATTRIBUTES', KeyConditionExpression='entidad = :nombre', ExpressionAttributeValues= { ":nombre":{"S":"SIAPA"}})
    print("viendo states reponse")
    print(response)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(response['Items']) == 0:
        dynamodb.put_item(TableName='states',Item={'entidad': {"S": 'SIAPA'}, 'actual': {"S":hash_value}, "fecha": {"S": fecha} })
        return True
    else:
        response = dynamodb.get_item(TableName='states', Key={'entidad': {"S":'SIAPA'}})
        current = response['Item']
        print("viendo si encontro uno")
        print(current)
        print(hash_value)
        if current['actual']["S"] != hash_value:
            dynamodb.update_item(TableName='states',
                Key={'entidad': {"S": 'SIAPA'}},
                UpdateExpression="set actual=:r, fecha=:f",
                ExpressionAttributeValues={':r': {"S": hash_value}, ":f":{"S": fecha}}
            )
            return True

    return False



if __name__ == "__main__":
    process_table()





