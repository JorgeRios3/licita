import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
from fuzzywuzzy import fuzz


def fetch_items_table(table=None, attr=None):
    if table != None:
        if attr == None or attr.strip() == "":
            table = dynamodb.Table(table)
            return table.scan()
        else:
            table = dynamodb.Table(table)
            items = table.scan()["Items"]
            searched_items = list(filter(lambda x:fuzz.partial_ratio(attr.lower(), x.get("descripcion", "").lower()) > 70, items))
            print(searched_items)
            print(len(searched_items))
            return {"Items": searched_items}
    else:
        return []



