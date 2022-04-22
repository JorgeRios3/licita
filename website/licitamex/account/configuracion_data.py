from django.conf import settings
from .models import CustomUser, Group,UsuarioPermisos,Permiso, GrupoFiltros
from .forms import NewUserForm




def data_configuracion(request):
    is_admin=False
    user = CustomUser.objects.get(pk=request.user.id)
    usuario_filtros = GrupoFiltros.objects.filter(group=user.group.id)
    form = NewUserForm()
    user = CustomUser.objects.get(pk=request.user.id)
    usuarios = CustomUser.objects.filter(group=user.group)
    user = CustomUser.objects.filter(pk=request.user.id)
    group = Group.objects.filter(pk=user[0].group.id)
    permisos_usuarios = UsuarioPermisos.objects.filter(group=user[0].group)
    admin = group[0].admin_user
    permisos_usuarios_without_admin = list(filter(lambda x: (x.id != admin), permisos_usuarios)) 
    print(permisos_usuarios_without_admin)
    permisos = Permiso.objects.all()
    if int(group[0].admin_user) == int(request.user.id):
        is_admin=True
    print("viendo group ", group[0].admin_user)
    usuarios_without_admin = list(filter(lambda x: (x.id != admin), usuarios))
    return {"filtros":usuario_filtros, 
    "form":form, "usuarios":usuarios_without_admin, "group":group[0], 
    "is_admin":is_admin, "permisos_usuarios":permisos_usuarios_without_admin, "permisos":permisos}