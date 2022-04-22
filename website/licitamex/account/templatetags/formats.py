from django import template
from ..models import UsuarioPermisos, CustomUser, Permiso

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


@register.filter
def empty_val(val):
    if val == None:
        return ""
    return val


@register.filter
def user_has_permission(usuario, permisos):
    cu = CustomUser.objects.get(pk=int(usuario))
    usuario_permisos = UsuarioPermisos.objects.filter(usuario=cu)
    print("viendo usuario jajaja ", usuario, permisos, usuario_permisos)
    for x in usuario_permisos:
        if x.permiso.permiso in permisos.split(","):
            return True
    return False
