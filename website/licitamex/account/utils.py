from django.conf import settings
from .models import CustomUser, Group
from django.shortcuts import render



def group_users(id):
    user = CustomUser.objects.get(pk=id)
    return CustomUser.objects.filter(group=user.group)




def compare_user(licitacion, user_licitaciones):
    val = list(filter(lambda x: x.licitacion_id==licitacion.get("id"), user_licitaciones))
    if val:
        licitacion["selected"]=True
    else:
        licitacion["selected"]=False
    return licitacion


def make_url(url):
    if settings.DEBUG:
        return f"http://127.0.0.1:8000/{url}"
    else:
        return f"https://consultalicitamex.com/{url}"



def account_is_active(view_func):
    def wrap(request, *args, **kwargs):
        print("simon", request.user.id)
        group = Group.objects.filter(pk=request.user.group.id)
        group = group[0]
        if group.plan_is_active:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, "account/suspended_account.html", {})
    return wrap


