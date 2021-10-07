try:
    import hashlib
    import boto3
    from boto3.dynamodb.conditions import Key, Attr
    from botocore.exceptions import ClientError

    from bs4 import BeautifulSoup
    import requests
    import datetime
    import json



    print("All Modules are ok ...")

except Exception as e:

    print("Error in Imports ")

url = 'https://www.triejal.gob.mx/convocatorias-licitaciones-publicas-2021'
page = requests.get(url)
soup = BeautifulSoup(page.content, features="html.parser")
dynamodb = boto3.client('dynamodb', region_name='us-west-2')



def process_table():
    table = soup.find('section', id='content')
    rows = table.find_all('p')
    licitaciones_actuales = dynamodb.scan(TableName='licitaciones', ProjectionExpression="licitacion, tipo, id", FilterExpression='entidad= :entidad', ExpressionAttributeValues= {":entidad":{"S":"triejal"} })
    lista_auxiliar = []
    for i,row in enumerate(rows):
        licitacion_url = row.find_all('a')
        page = requests.get(licitacion_url[0].get('href'))
        soup2 = BeautifulSoup(page.content, features="html.parser")
        wrapper = soup2.find('div', id='boxed-wrapper')
        section = wrapper.find('section', id="content")
        try:
            licitacion = row.text
        except:
            licitacion = ""
        try:
            base = licitacion_url[0].get('href')
        except:
            base = ""
        try:
            descripcion = descripcion = section.find('strong').text
        except:
            descripcion = ""
        try:
            entidad = "triejal"
        except:
            entidad = ""
        item = {
            "id":f"{datetime.datetime.now().timestamp()}",
            'licitacion': licitacion,
            'entidad': entidad,
            'descripcion': descripcion,
            'urls': {"convocatoria": f"{base}"}
        }
        lista_auxiliar.append(item)
        
        result = list(filter(lambda x: x["licitacion"]["S"]==item["licitacion"], licitaciones_actuales["Items"]))
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
            requests.post("https://consultalicitamex.com/add_licitacion", data=payload)
            #llamada al server para avisar que hay una nueva licitacion

    #este for nos va a ayudar a que si en la pagina del gobierno borraron una licitacion nosotros la borremos de dynamo
    for item in licitaciones_actuales["Items"]:
        result = list(filter(lambda x: x["licitacion"] ==item["licitacion"]["S"], lista_auxiliar))
        if len(result) == 0:
            print("lo borro")
            payload = json.dumps({'id': item["id"]})
            dynamodb.delete_item(TableName='licitaciones', Key={"id":item["id"]})
            requests.post("https://consultalicitamex.com/remove_licitacion", data=payload)
    return


def check_changes(hash_value):
    response = dynamodb.query(TableName='states', Select='ALL_ATTRIBUTES', KeyConditionExpression='entidad = :nombre', ExpressionAttributeValues= { ":nombre":{"S":"triejal"}})
    print("viendo states reponse")
    print(response)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(response['Items']) == 0:
        dynamodb.put_item(TableName='states',Item={'entidad': {"S": 'triejal'}, 'actual': {"S":hash_value}, "fecha": {"S": fecha} })
        return True
    else:
        response = dynamodb.get_item(TableName='states', Key={'entidad': {"S":'triejal'}})
        current = response['Item']
        print("viendo si encontro uno")
        print(current)
        print(hash_value)
        if current['actual']["S"] != hash_value:
            dynamodb.update_item(TableName='states',
                Key={'entidad': {"S": 'triejal'}},
                UpdateExpression="set actual=:r, fecha=:f",
                ExpressionAttributeValues={':r': {"S": hash_value}, ":f":{"S": fecha}}
            )
            return True

    return False


def lambda_handler(event, context):
    url = 'https://www.triejal.gob.mx/convocatorias-licitaciones-publicas-2021'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="html.parser")
    rows = soup.find_all('tr', class_='odd')
    rows = str(rows)
    hash_value = hashlib.sha224(rows.encode()).hexdigest()
    if check_changes(hash_value):
        process_table()
    return True