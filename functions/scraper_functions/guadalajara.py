#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import hashlib
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from bs4 import BeautifulSoup
import requests
import datetime

url = 'https://transparencia.guadalajara.gob.mx/licitaciones2021'
page = requests.get(url)
soup = BeautifulSoup(page.content, features="lxml")
dynamo = boto3.resource('dynamodb', region_name='us-west-2')


def process_table():
    rows = soup.find_all('tr', class_='odd')
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

            urls = row.find_all('a')

            try:
                base = urls[0].get('href')
            except:
                base = ''
            try:
                convocatoria = urls[1].get('href')
            except:
                convocatoria = ''
            try:
                fallo = urls[2].get('href')
            except:
                fallo = ''

            urls={}

            item = {
                "id":f"{datetime.datetime.now().timestamp()}",
                'licitacion': licitacion,
                'entidad': 'Guadalajara',
                'descripcion': descripcion.replace('“', "").replace('"',"").replace("\n", ""),
                'urls': {"base": base, "convocatoria": convocatoria, "fallo": fallo}
            }
            v_table.put_item(Item=item)
            print(item)
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


#hash_value = hashlib.sha224(soup).hexdigest()
#if check_changes(hash_value):
#    process_table()

if __name__ == "__main__":
    process_table()
