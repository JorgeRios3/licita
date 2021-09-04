try:
    import json
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    import os
    import shutil
    import uuid
    import boto3
    from boto3.dynamodb.conditions import Key, Attr
    from datetime import datetime
    import datetime
    import time
    import hashlib



    print("All Modules are ok ...")

except Exception as e:

    print("Error in Imports ")

#dynamo = boto3.resource('dynamodb', region_name='us-west-2')
dynamodb = boto3.client('dynamodb', region_name='us-west-2')

def process_table(table):
    rows = table.find_elements_by_class_name("rich-table-firstrow")
    licitaciones_actuales = dynamodb.scan(TableName='licitaciones', ProjectionExpression="licitacion, tipo", FilterExpression='entidad= :entidad', ExpressionAttributeValues= {":entidad":{"S":"Jalisco"} })
    lista_auxiliar = []
    #este for es para agregar nuevas licitaciones a dynamodb validando contra los actuales en dynamodb
    for i,row in enumerate(rows):
        elements = row.find_elements_by_class_name("rich-table-cell")
        try:
            tipo = elements[1].text
        except:
            tipo = ""
        try:
            temp = str.splitlines(elements[2].text)
            solicitud = temp[0]
            licitacion = temp[1]
        except:
            solicitud = ""
            licitacion = ""
        try:
            temp = elements[3].text.split(" - ")
            grupo = temp[0]
            familia = temp[1]
        except:
            grupo = ""
            familia = ""
        try:
            dependencia = elements[4].text
        except:
            dependencia = ""
        try:
            publicacion = elements[5].text
        except:
            publicacion = ""
        try:
            limite = elements[6].text
        except:
            limite = ""
        try:
            texto=elements[8].text
            urls={f"{texto}": url}

        except:
            urls={}

        item = {
            "id":f"{datetime.datetime.now().timestamp()}",
            'licitacion': licitacion,
            'entidad': 'Jalisco',
            'tipo': tipo,
            'solicitud': solicitud,
            'grupo': grupo,
            'familia': familia,
            'dependencia': dependencia,
            'publicacion': publicacion,
            'limite': limite,
            'urls':urls,
            "descripcion": f"{tipo} {familia}"
        }
        lista_auxiliar.append(item)

        result = list(filter(lambda x: x["licitacion"]["S"]==item["licitacion"] and x["tipo"]["S"]==item["tipo"], licitaciones_actuales["Items"]))
        if i==4:
            if len(result) == 0:
                d_val = {
                    "id": {"S": item["id"]},
                    "licitacion": {"S": item["licitacion"]},
                    "entidad": {"S": item["entidad"]},
                    "tipo": {"S": item["tipo"]},
                    "solicitud": {"S": item["solicitud"]},
                    "grupo": {"S": item["grupo"]},
                    "familia": {"S": item["familia"]},
                    "dependencia": {"S": item["dependencia"]},
                    "publicacion": {"S": item["publicacion"]},
                    "limite": {"S": item["limite"]},
                    "urls": {"M": {f"{texto}": {"S": url}} },
                    "descripcion": {"S": item["descripcion"]}
                }
                print("agregando")
                dynamodb.put_item(TableName='licitaciones', Item=d_val)
                #llamada al server para avisar que hay una nueva licitacion

    #este for nos va a ayudar a que si en la pagina del gobierno borraron una licitacion nosotros la borremos de dynamo
    for item in licitaciones_actuales["Items"]:
        result = list(filter(lambda x: x["licitacion"] ==item["licitacion"]["S"] and item["tipo"]["S"]==x["tipo"] , lista_auxiliar))
        if len(result) == 0:
            print(item)
            print("hay que borrar")

    return

class WebDriver(object):

    def __init__(self):
        self.options = Options()
        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver

def check_changes(hash_value):
    response = dynamodb.query(TableName='states', Select='ALL_ATTRIBUTES', KeyConditionExpression='entidad = :nombre', ExpressionAttributeValues= { ":nombre":{"S":"Jalisco"}})
    print("viendo states reponse")
    print(response)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(response['Items']) == 0:
        dynamodb.put_item(TableName='states',Item={'entidad': {"S": 'Jalisco'}, 'actual': {"S":hash_value}, "fecha": {"S": fecha} })
        return True
    else:
        response = dynamodb.get_item(TableName='states', Key={'entidad': {"S":'Jalisco'}})
        current = response['Item']
        print("viendo si encontro uno")
        print(current)
        if current['actual']["S"] != hash_value:
            dynamodb.update_item(TableName='states',
                Key={'entidad': {"S": 'Jalisco'}},
                UpdateExpression="set actual=:r, fecha=:f",
                ExpressionAttributeValues={':r': {"S": hash_value}, ":f":{"S": fecha}}
            )
            return True

    return False


def lambda_handler(event, context):

    instance_ = WebDriver()
    driver = instance_.get()
    driver.get("https://encompras.jalisco.gob.mx/SJ3Kweb/secure/")
    time.sleep(5)
    iframe_ref = driver.find_elements_by_id("mainFrame")[0]
    driver.switch_to.frame(iframe_ref)
    table = driver.find_element_by_class_name("rich-table")
    hash_value = hashlib.sha224(table.text.encode()).hexdigest()
    if check_changes(hash_value):
        process_table(table)
    return True