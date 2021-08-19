def compare_user(licitacion, user_licitaciones):
    val = list(filter(lambda x: x.licitacion_id==licitacion.get("id"), user_licitaciones))
    if val:
        licitacion["selected"]=True
    else:
        licitacion["selected"]=False
    return licitacion
