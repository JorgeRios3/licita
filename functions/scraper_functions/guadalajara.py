from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
import boto3
from boto3.dynamodb.conditions import Key, Attr


url = 'https://transparencia.guadalajara.gob.mx/licitaciones2021'
dynamo = boto3.resource('dynamodb', region_name='us-west-2')


def process_table():
    rows = table.find_elements_by_class_name("odd")
    v_table = dynamo.Table('licitaciones')

    for row in rows:
        line = row.text
        text = line.split(' ')
        if 'LPL' in text:
            idx = text.index('LPL')
            try:
                licitacion = text[idx] + ' ' + text[idx+1]
            except:
                licitacion = ''
            try:
                descripcion = ' '.join(text[idx+2:])
            except:
                descripcion = ''

            urls = row.find_elements_by_tag_name('a')

            try:
                base = urls[0].get_attribute("href")
            except:
                base = ''
            try:
                convocatoria = urls[1].get_attribute("href")
            except:
                convocatoria = ''
            try:
                fallo = urls[2].get_attribute("href")
            except:
                fallo = ''

            item = {
                'licitacion': licitacion,
                'entidad': 'Guadalajara',
                'descripcion': descripcion,
                'base': base,
                'convocatoria': convocatoria,
                'fallo': fallo
            }

            v_table.put_item(Item=item)
            print('Registrando ' + licitacion)

    return


def check_changes(hash_value):
    s_table = dynamo.Table('states')
    response = s_table.query(
        KeyConditionExpression=Key('name').eq('guadalajara'))

    if len(response['Items']) == 0:
        s_table.put_item(Item={'name': 'guadalajara', 'current': hash_value})
        return True
    else:
        response = s_table.get_item(Key={'name': 'guadalajara'})
        print(response)
        current = response['Item']
        if current['current'] != hash_value:
            s_table.update_item(
                Key={'name': 'guadalajara'},
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

table = driver.find_element_by_class_name("table")
hash_value = hashlib.sha224(table.text.encode()).hexdigest()


if check_changes(hash_value):
    print('test')
#process_table()

driver.close()
driver.quit()
