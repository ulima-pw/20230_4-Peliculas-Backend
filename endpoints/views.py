from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import Categoria

# /endpoints/login
@csrf_exempt
def login(request):
    if request.method == "POST":
        dictDataRequest = json.loads(request.body)
        usuario = dictDataRequest["usuario"]
        password = dictDataRequest["password"]

        # TODO: Consultar a base de datos
        if usuario == "pw" and password == "123":
            # Correcto
            dictOk = {
                "error": ""
            }
            return HttpResponse(json.dumps(dictOk))
        else:
            # Error login
            dictError = {
                "error": "Error en login"
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)


def obtenerPeliculas(request):
    if request.method == "GET":
        categoria = request.GET.get("categoria")

        if categoria == None:
            dictError = {
                "error": "Debe enviar una categoria como query paremeter."
            }
            strError = json.dumps(dictError)
            return HttpResponse(strError)

        peliculas = [
            {
                "id": 1,
                "nombre": "Avatar 2",
                "url": "https://i.blogs.es/6b43d1/avatar-edicion-especial-cartel/450_1000.jpg",
                "categoria": 1
            }, {
                "id": 2,
                "nombre": "El gato con botas",
                "url": "https://www.universalpictures-latam.com/tl_files/content/movies/puss_in_boots_2/posters/01.jpg",
                "categoria": 2
            }, {
                "id": 3,
                "nombre": "Transformer, el despertar de las bestias",
                "url": "https://es.web.img3.acsta.net/pictures/22/12/02/09/33/5399733.jpg",
                "categoria": 3
            }
        ]

        peliculasFiltradas = []
        if categoria == "-1":
            # No se debe filtrar nana
            peliculasFiltradas = peliculas
        else :
            for p in peliculas:
                if p["categoria"] == int(categoria):
                    peliculasFiltradas.append(p)
        
        # TODO: Consultas a bd
        dictResponse = {
            "error": "",
            "peliculas": list(peliculasFiltradas)
        }
        strResponse = json.dumps(dictResponse)
        return HttpResponse(strResponse)
    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)


def obtenerCategorias(request):
    if request.method == "GET":
        listaCategoriasQuerySet = Categoria.objects.filter(estado="A")
        listaCategorias = []
        for c in listaCategoriasQuerySet:
            listaCategorias.append({
                "id" : c.id,
                "nombre" : c.nombre
            })

        dictOK = {
            "error" : "",
            "categorias" : listaCategorias
        }
        return HttpResponse(json.dumps(dictOK))

    else:
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

"""
Path: /endpoints/categorias/crear POST
Request:
{
    "nombre" : "...",
    "estado" : "A"
}
Response:
{
    "error" : ""
}
"""
@csrf_exempt
def registrarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    dictCategoria = json.loads(request.body)
    nombre = dictCategoria["nombre"]
    estado = dictCategoria["estado"]

    cat = Categoria(nombre=nombre, estado=estado)
    cat.save() # Registra en la bd la nueva categoria

    dictOK = {
        "error" : ""
    }
    return HttpResponse(json.dumps(dictOK))

"""
Path: /endpoints/categorias/modificar POST
Request:
{
    "id" : 1,
    "nombre"? : "...",
    "estado"? : "A"
}
Response:
{
    "error" : ""
}
"""
@csrf_exempt
def modificarCategoria(request):
    if request.method != "POST":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)
    
    dictCategoria = json.loads(request.body)

    identificador = dictCategoria["id"]
    cat = Categoria.objects.get(pk=identificador) # Obtenemos cat de bd

    if dictCategoria.get("nombre") != None:
        cat.nombre = dictCategoria.get("nombre")

    if dictCategoria.get("estado") != None:
        cat.estado = dictCategoria.get("estado")

    cat.save() # Se modifica la bd

    dictOK = {
        "error" : ""
    }
    return HttpResponse(json.dumps(dictOK))


def eliminarCategoria(request):
    if request.method != "GET":
        dictError = {
            "error": "Tipo de peticion no existe"
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    idCategoria = request.GET.get("id")
    
    if idCategoria == None:
        dictError = {
            "error": "Debe enviar un id de categoria para eliminarla."
        }
        strError = json.dumps(dictError)
        return HttpResponse(strError)

    cat = Categoria.objects.get(pk=idCategoria) # Obtengo categoria de la bd
    cat.delete()  # elimino categoria de la bd

    dictOK = {
        "error" : ""
    }
    return HttpResponse(json.dumps(dictOK))