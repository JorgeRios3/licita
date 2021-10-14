from .models import UsuarioLicitaciones
from django.shortcuts import render, redirect, reverse
import json
from django.core import serializers
from datetime import datetime
from storages.backends.s3boto3 import S3Boto3Storage
import os
from django.http import JsonResponse
from .models import CustomUser


class MediaStorage(S3Boto3Storage):
    bucket_name = 'cotizacioneslicitamex'

def get_user_licitaciones(user_id):
    user = CustomUser.objects.get(pk=user_id)
    licitaciones = UsuarioLicitaciones.objects.filter(user=user)
    print(licitaciones)
    return licitaciones

def change_status(request):
    post_data = json.loads(request.body.decode("utf-8"))
    UsuarioLicitaciones.objects.filter(pk=post_data.get("id", 0)).update(status=post_data.get("status", ''))
    return render(request, 'account/dashboard.html', {"licitaciones":get_user_licitaciones(request.user.id)})

def add_cotizacion(request, id):
    try:
        file = request.FILES['document']
    except:
        licitacion = UsuarioLicitaciones.objects.filter(pk=id)
        serialized_obj = serializers.serialize('json', licitacion)
        ob_json = json.loads(serialized_obj)
        return render(request, 'account/licitacion.html', {"id":id, "licitacion":ob_json[0]["fields"]})
    print(file.name)
    print(file.size)
    file_directory_within_bucket = 'user_upload_files/{username}/cotizacion/{id}'.format(username=request.user.id, id=id)

        # synthesize a full file path; note that we included the filename
    file_path_within_bucket = os.path.join(
        file_directory_within_bucket,
        file.name
    )

    media_storage = MediaStorage()

    if not media_storage.exists(file_path_within_bucket): # avoid overwriting existing file
        media_storage.save(file_path_within_bucket, file)
        file_url = media_storage.url(file_path_within_bucket)

        licitacion = UsuarioLicitaciones.objects.filter(pk=id)
        licitacion = licitacion[0]
        licitacion.quotation = file_url
        licitacion.save()
        licitacion = UsuarioLicitaciones.objects.filter(pk=id)
        serialized_obj = serializers.serialize('json', licitacion)
        ob_json = json.loads(serialized_obj)
        return render(request, 'account/licitacion.html', {"id":id, "licitacion":ob_json[0]["fields"]})
    else:
        return JsonResponse({
            'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                filename=file_obj.name,
                file_directory=file_directory_within_bucket,
                bucket_name=media_storage.bucket_name
            ),
        }, status=400)


def licitacion(request, id):
    if request.method == "GET":
        licitacion = UsuarioLicitaciones.objects.filter(pk=id)
        serialized_obj = serializers.serialize('json', licitacion)
        ob_json = json.loads(serialized_obj)
        return render(request, 'account/licitacion.html', {"id":id, "licitacion":ob_json[0]["fields"]})
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        licitacion = UsuarioLicitaciones.objects.filter(pk=id)
        licitacion=licitacion[0]
        print(licitacion.comments)
        comentario = post_data.get("text", "")
        if comentario.strip() != "":
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = CustomUser.objects.get(pk=request.user.id)
            if licitacion.comments.get("comments", "") == "":
                licitacion.comments = {"comments":[{"date":fecha, "comment":comentario, "user":user.id}]}
            else:
                licitacion.comments["comments"].append({"date":fecha, "comment":comentario, "user":user.id})
        nombre = post_data.get("nombre", "")
        telefono = post_data.get("telefono", "")
        email = post_data.get("email", "")
        direccion = post_data.get("direccion", "")
        licitacion.datos_comprador={"nombre":nombre, "telefono":telefono, "email":email, "direccion":direccion}
        licitacion.save()
        licitacion = UsuarioLicitaciones.objects.filter(pk=id)
        serialized_obj = serializers.serialize('json', licitacion)
        ob_json = json.loads(serialized_obj)
        return render(request, 'account/licitacion.html', {"id":id, "licitacion":ob_json[0]["fields"]})





def delete_licitacion(request):
    post_data = json.loads(request.body.decode("utf-8"))
    licitacion = UsuarioLicitaciones.objects.filter(pk=post_data.get("id", 0))
    licitacion = licitacion[0]
    licitacion.delete()
    return render(request, 'account/dashboard.html', {"licitaciones":get_user_licitaciones(request.user.id)})


