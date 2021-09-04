from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime

url = 'https://pagos.zapopan.gob.mx/PortalProveedores/InvitacionesGral.aspx'
dynamo = boto3.resource('dynamodb', region_name='us-west-2')



def process_table():
    rows = table.find_elements_by_id("tabla1")
    v_table = dynamo.Table('licitaciones')

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
        print(item)
        v_table.put_item(Item=item)
        #print('Registrando ' + requisicion)
        #print(i)

    return


def check_changes(hash_value):
    s_table = dynamo.Table('states')
    response = s_table.query(KeyConditionExpression=Key('name').eq('zapopan'))

    if len(response['Items']) == 0:
        s_table.put_item(Item={'name': 'zapopan', 'current': hash_value})
        return True
    else:
        response = s_table.get_item(Key={'name': 'zapopan'})
        current = response['Item']
        if current['current'] != hash_value:
            s_table.update_item(
                Key={'name': 'zapopan'},
                UpdateExpression='SET #new_current = :val',
                ExpressionAttributeValues={':val': hash_value},
                ExpressionAttributeNames={'#new_current': 'current'}

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


if check_changes(hash_value):
    process_table()


driver.close()
driver.quit()
