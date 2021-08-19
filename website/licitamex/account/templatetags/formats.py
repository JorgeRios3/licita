from django import template

register = template.Library()

@register.filter
def format_urls(urls):
    chain=""
    for key in urls.keys():
        if urls[key].strip() != "":
            chain+=f"<a href='{urls[key]}' target='_blank'>{key}</a><br>"
    return chain

@register.filter
def format_id_rows(val):
    return "r{}".format(val.split(".")[0])
