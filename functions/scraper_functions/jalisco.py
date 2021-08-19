from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import hashlib
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime



url = 'https://encompras.jalisco.gob.mx/SJ3Kweb/secure/'
dynamo = boto3.resource('dynamodb', region_name='us-west-2')


def process_table():
    rows = table.find_elements_by_class_name("rich-table-firstrow")
    v_table = dynamo.Table('licitaciones')

    for row in rows:
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
            depencencia = ""
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

        v_table.put_item(Item=item)
        print('Registrando ' + licitacion)

    return


def check_changes(hash_value):
    s_table = dynamo.Table('states')
    response = s_table.query(KeyConditionExpression=Key('name').eq('jalisco'))

    if len(response['Items']) == 0:
        s_table.put_item(Item={'name': 'jalisco', 'current': hash_value})
        return True
    else:
        response = s_table.get_item(Key={'name': 'jalisco'})
        current = response['Item']
        if current['current'] != hash_value:
            s_table.update_item(
                Key={'name': 'jalisco'},
                UpdateExpression='SET #new_current = :val',
                ExpressionAttributeValues={':val': hash_value},
                ExpressionAttributeNames={'#new_current': 'current'}

            )
            return True

    return False


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome('/Users/jorge.rios/Downloads/chromedriver', options=chrome_options)
driver.get(url)
time.sleep(5)

iframe_ref = driver.find_elements_by_id("mainFrame")[0]
driver.switch_to.frame(iframe_ref)

table = driver.find_element_by_class_name("rich-table")
hash_value = hashlib.sha224(table.text.encode()).hexdigest()

#if check_changes(hash_value):
process_table()

driver.close()
driver.quit()
