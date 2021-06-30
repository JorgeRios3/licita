from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
import boto3
from boto3.dynamodb.conditions import Key, Attr

url = 'https://pagos.zapopan.gob.mx/PortalProveedores/InvitacionesGral.aspx'
dynamo = boto3.resource('dynamodb', region_name='us-west-2')


def process_table():
    rows = table.find_elements_by_id("tabla1")
    v_table = dynamo.Table('licitaciones')

    for row in rows:
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
            publicacion = fields[3].text
        except:
            publicacion = ''
        try:
            cierre = fields[4].text
        except:
            cierre = ''

        item = {
            'licitacion': requisicion,
            'entidad': 'Zapopan',
            'invitacion': invitacion,
            'descripcion': descripcion,
            'publicacion': publicacion,
            'cierre': cierre
        }

        v_table.put_item(Item=item)
        print('Registrando ' + requisicion)

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


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)
driver.get(url)

table = driver.find_element_by_id("DataList1")
hash_value = hashlib.sha224(table.text.encode()).hexdigest()


if check_changes(hash_value):
    process_table()


driver.close()
driver.quit()
