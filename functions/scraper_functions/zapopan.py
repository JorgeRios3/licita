from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import json
import requests

url = 'https://pagos.zapopan.gob.mx/PortalProveedores/InvitacionesGral.aspx'
dynamodb = boto3.client('dynamodb', region_name='us-west-2')



def process_table():
    rows = table.find_elements_by_id("tabla1")
    rows = table.find_elements_by_tag_name("tr")
    licitaciones_actuales = dynamodb.scan(TableName='licitaciones', ProjectionExpression="licitacion, id", FilterExpression='entidad= :entidad', ExpressionAttributeValues= {":entidad":{"S":"Zapopan"} })
    lista_auxiliar = []
    rows = rows[1:]
    for i,row in enumerate(rows):
        text = row.text
        if 'Fecha Cierre' in text:
            continue
        fields = row.find_elements_by_class_name("txtInfoTabla")
        try:
            requisicion = fields[0].text
        except:
            requisicion = ''
        try:
            invitacion = fields[1].text
        except:
            invitacion = ''
        try:
            descripcion = fields[2].text
        except:
            description = ''
        try:
            fecha_publicacion = fields[3].text
        except:
            fecha_publicacion = ''
        try:
            fecha_cierre = fields[4].text
        except:
            fecha_cierre = ''
        try:
            urls={}
            buttons = fields[5].find_elements_by_tag_name('a')
            for x in buttons:
                urls[x.text]=f"{url}#{x.get_attribute('id')}"
        except:
            urls = {}
        item = {
            "id":f"{datetime.datetime.now().timestamp()}",
            'licitacion': requisicion,
            'entidad': 'Zapopan',
            'invitacion': invitacion,
            'descripcion': descripcion,
            'publicacion': fecha_publicacion,
            'cierre': fecha_cierre,
            'urls': urls
        }
        durls = {}
        for key in urls.keys():
            durls[f"{key}"] = {"S": urls[f"{key}"]}    
        result = list(filter(lambda x: x["licitacion"]["S"]==item["licitacion"], licitaciones_actuales["Items"]))
        if len(result) == 0:
            d_val = {
                "id": {"S": item["id"]},
                "licitacion": {"S": item["licitacion"]},
                "entidad": {"S": item["entidad"]},
                "invitacion": {"S": item["invitacion"]},
                "publicacion": {"S": item["publicacion"]},
                "cierre": {"S": item["cierre"]},
                "urls": {"M": durls },
                "descripcion": {"S": item["descripcion"]}
            }
            print("agregando")
            dynamodb.put_item(TableName='licitaciones', Item=d_val)
            payload = json.dumps({'id': item["id"]})
            requests.post("https://consultalicitamex.com/add_licitacion", data=payload)
            #llamada al server para avisar que hay una nueva licitacion

    #este for nos va a ayudar a que si en la pagina del gobierno borraron una licitacion nosotros la borremos de dynamo
    for item in licitaciones_actuales["Items"]:
        result = list(filter(lambda x: x["licitacion"] ==item["licitacion"]["S"] and item["tipo"]["S"]==x["tipo"] , lista_auxiliar))
        if len(result) == 0:
            print("lo borro")
            payload = json.dumps({'id': item["id"]})
            dynamodb.delete_item(TableName='licitaciones', Key={"id":item["id"]})
            requests.post("https://consultalicitamex.com/remove_licitacion", data=payload)

    return


def check_changes(hash_value):
    response = dynamodb.query(TableName='states', Select='ALL_ATTRIBUTES', KeyConditionExpression='entidad = :nombre', ExpressionAttributeValues= { ":nombre":{"S":"Zapopan"}})
    print("viendo states reponse")
    print(response)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(response['Items']) == 0:
        dynamodb.put_item(TableName='states',Item={'entidad': {"S": 'Zapopan'}, 'actual': {"S":hash_value}, "fecha": {"S": fecha} })
        return True
    else:
        response = dynamodb.get_item(TableName='states', Key={'entidad': {"S":'Zapopan'}})
        current = response['Item']
        print("viendo si encontro uno")
        print(current)
        if current['actual']["S"] != hash_value:
            dynamodb.update_item(TableName='states',
                Key={'entidad': {"S": 'Zapopan'}},
                UpdateExpression="set actual=:r, fecha=:f",
                ExpressionAttributeValues={':r': {"S": hash_value}, ":f":{"S": fecha}}
            )
            return True

    return False


val = {"download.default_directory":"/Users/jorge.rios/dev/licitacion/licitamex/functions/scraper_functions"}
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_experimental_option("prefs", val)
driver = webdriver.Chrome('/Users/jorge.rios/Downloads/chromedriver', options=chrome_options)
driver.get(url)

table = driver.find_element_by_id("DataList1")
hash_value = hashlib.sha224(table.text.encode()).hexdigest()


#if check_changes(hash_value):
process_table()


driver.close()
driver.quit()
